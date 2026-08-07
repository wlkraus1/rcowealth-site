<?php
/**
 * Website lead intake for rcowealth.com.
 *
 * Replaces the Salesforce Web-to-Lead endpoint every form on this site posted to.
 * The CRM (FSC) now runs on a machine that is not reachable from the internet and
 * is a laptop that sleeps, so it cannot be the thing a public form posts to: a
 * lead submitted while it is asleep would be lost, and lost silently, which is
 * worse than the problem being solved.
 *
 * So this file is the always-on part. It does two things and stores nothing:
 *
 *   1. Emails the lead to the firm, in a format the CRM can parse. That email is
 *      the DURABLE QUEUE — it waits in the mailbox for as long as it takes, and
 *      the CRM ingests it whenever the Mac is next awake. Nothing is lost if the
 *      Mac is off for a week.
 *   2. Notifies Tyler immediately, so he knows he has a lead without waiting for
 *      the CRM to pick it up.
 *
 * The CRM pulls; it is never pushed to. That is the whole reason this works
 * without exposing the firm's client book to the internet.
 *
 * NO CLIENT DATA IS WRITTEN TO DISK on the happy path. The only exception is a
 * last-resort spill file if the mail call itself fails, because losing a real
 * prospect silently is the one outcome worth writing PII to disk to avoid — and
 * that directory denies all web access.
 */

declare(strict_types=1);

const FIRM_INBOX      = 'info@rcowealth.com';
const FROM_ADDRESS    = 'website@rcowealth.com';
const DEFAULT_RETURN  = '/thank-you.html';
const RATE_MAX        = 5;          // submissions per IP
const RATE_WINDOW     = 3600;       // per hour
const SPILL_DIR       = __DIR__ . '/.lead-spill';
// Optional. If this file exists it must contain JSON {"token": "...", "chat_id": "..."}.
// Deliberately NOT in git and never required: without it, the notification is the
// email itself, and a bot token does not sit on a public webserver for no reason.
const TELEGRAM_CONFIG = __DIR__ . '/.telegram.json';

/** Same-origin only. An open redirect on a financial firm's site is a phishing gift. */
function safe_return(string $candidate): string {
    if ($candidate === '') return DEFAULT_RETURN;
    $parts = parse_url($candidate);
    if ($parts === false) return DEFAULT_RETURN;
    if (!isset($parts['host'])) return strpos($candidate, '/') === 0 ? $candidate : DEFAULT_RETURN;
    $host = strtolower($parts['host']);
    return ($host === 'rcowealth.com' || $host === 'www.rcowealth.com') ? $candidate : DEFAULT_RETURN;
}

function finish(string $return) {
    header('Location: ' . safe_return($return), true, 303);
    exit;
}

function field(string $name, int $max = 500): string {
    $v = $_POST[$name] ?? '';
    if (!is_string($v)) return '';
    // Newlines out of header-bound values, always: a name carrying \r\n is how a
    // form becomes an open mail relay.
    $v = str_replace(["\r", "\n", "\0"], ' ', $v);
    return trim(mb_substr($v, 0, $max));
}

$return = (string) ($_POST['retURL'] ?? DEFAULT_RETURN);

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    finish(DEFAULT_RETURN);
}

// Honeypot. Three names because three systems disagree about what to call it:
// Salesforce's Web-to-Lead convention is website_url, this site's own markup uses
// it too, and the CRM checks website/fax. A bot fills every input it finds.
foreach (['website_url', 'website', 'fax'] as $trap) {
    if (trim((string) ($_POST[$trap] ?? '')) !== '') {
        finish($return);   // a plain success: telling a bot which check caught it teaches it to pass
    }
}

// Per-IP rate limit. Only a HASH of the address is stored, and only a counter —
// a visitor's IP is not something this file needs to keep in readable form.
$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '');
$bucketFile = sys_get_temp_dir() . '/rco-lead-' . substr(hash('sha256', $ip . '|rcowealth'), 0, 24);
$hits = [];
if (is_readable($bucketFile)) {
    $decoded = json_decode((string) file_get_contents($bucketFile), true);
    if (is_array($decoded)) $hits = $decoded;
}
$now = time();
$hits = array_values(array_filter($hits, function ($t) use ($now) { return is_int($t) && $now - $t < RATE_WINDOW; }));
if (count($hits) >= RATE_MAX) {
    finish($return);   // quiet: a rate-limit page tells a script exactly what to tune
}
$hits[] = $now;
@file_put_contents($bucketFile, json_encode($hits), LOCK_EX);

$first = field('first_name', 80) ?: field('firstName', 80);
$last  = field('last_name', 80)  ?: field('lastName', 80);
$email = field('email', 160);
$phone = field('phone', 40);

// A submission with neither a name nor an email is not a lead anyone can act on.
if ($first === '' && $last === '' && $email === '') {
    finish($return);
}

$message = (string) ($_POST['description'] ?? $_POST['message'] ?? '');
$message = trim(mb_substr(str_replace("\0", '', $message), 0, 4000));

$fields = [
    'first_name'   => $first,
    'last_name'    => $last,
    'email'        => $email,
    'phone'        => $phone,
    'company'      => field('company', 120),
    'lead_source'  => field('lead_source', 80),
    'campaign'     => field('00NbV000003RzSl', 120),
    'source_detail'=> field('00Nfn0000089jHR', 120),
    'next_step'    => field('preferred_next_step_display', 120),
    'page'         => field('page', 200) ?: (string) ($_SERVER['HTTP_REFERER'] ?? ''),
    'submitted_at' => gmdate('c'),
];

$name = trim($first . ' ' . $last);
if ($name === '') $name = $email;

// The body the CRM parses. Deliberately a flat, delimited block rather than JSON:
// a mail client that wraps or re-encodes a long JSON line breaks the parse, and a
// human reading this on a phone can still see exactly what came in.
$lines = ["--- FSC LEAD ---"];
foreach ($fields as $k => $v) {
    $lines[] = $k . ': ' . $v;
}
$lines[] = "--- MESSAGE ---";
$lines[] = $message;
$lines[] = "--- END FSC LEAD ---";
$body = implode("\n", $lines) . "\n";

$subject = '[FSC-LEAD] ' . ($name !== '' ? $name : 'Website enquiry');
if ($fields['lead_source'] !== '') $subject .= ' — ' . $fields['lead_source'];

$headers = [
    'From: Rae & Co Website <' . FROM_ADDRESS . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-FSC-Lead: 1',
];
// Reply-To only when the address is real, so hitting reply in the inbox goes to
// the prospect rather than to a header a bot chose.
if ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $headers[] = 'Reply-To: ' . $email;
}

$sent = @mail(FIRM_INBOX, $subject, $body, implode("\r\n", $headers));

if (!$sent) {
    // The one case worth writing a prospect's details to disk: mail failed, and the
    // alternative is a real enquiry disappearing with nobody aware it existed. The
    // directory denies web access (see .lead-spill/.htaccess) and this is meant to
    // be drained by hand and emptied.
    if (!is_dir(SPILL_DIR)) @mkdir(SPILL_DIR, 0700, true);
    @file_put_contents(
        SPILL_DIR . '/leads.jsonl',
        json_encode(['at' => gmdate('c'), 'fields' => $fields, 'message' => $message]) . "\n",
        FILE_APPEND | LOCK_EX
    );
}

// Instant notification, if a token has been placed on the server. Failure here is
// never allowed to affect the visitor: the email is the record, this is the nudge.
if (is_readable(TELEGRAM_CONFIG)) {
    $cfg = json_decode((string) file_get_contents(TELEGRAM_CONFIG), true);
    if (is_array($cfg) && !empty($cfg['token']) && !empty($cfg['chat_id'])) {
        $text = "🚨 New website lead\n" . $name
            . ($phone !== '' ? "\n" . $phone : '')
            . ($email !== '' ? "\n" . $email : '')
            . ($fields['lead_source'] !== '' ? "\n" . $fields['lead_source'] : '')
            . ($sent ? '' : "\n⚠️ the notification email FAILED to send — check the spill file");
        $ch = curl_init('https://api.telegram.org/bot' . $cfg['token'] . '/sendMessage');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 6,
            CURLOPT_POSTFIELDS => http_build_query(['chat_id' => $cfg['chat_id'], 'text' => $text]),
        ]);
        @curl_exec($ch);
        @curl_close($ch);
    }
}

finish($return);
