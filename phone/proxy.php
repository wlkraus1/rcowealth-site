<?php
// Stable IONOS-hosted proxy for the Rae & Co Twilio phone assistant.
// Twilio should call https://rcowealth.com/phone/voice.php.
// This forwards to the current Mac phone-agent public tunnel while keeping
// Twilio's configured webhook stable.

function phone_proxy_config(): array {
    $cfg = require __DIR__ . '/config.php';
    $base = rtrim((string)($cfg['upstream_base_url'] ?? ''), '/');
    if ($base === '') {
        phone_proxy_twiml_error('Phone bridge upstream is not configured.');
    }
    return [
        'base' => $base,
        'timeout' => (int)($cfg['proxy_timeout_seconds'] ?? 20),
    ];
}

function phone_proxy_target_path(): string {
    $script = basename((string)($_SERVER['SCRIPT_NAME'] ?? 'voice.php'));
    $map = [
        'voice.php' => '/voice',
        'listen.php' => '/listen',
        'respond.php' => '/respond',
        'poll.php' => '/poll',
        'health.php' => '/health',
        'elevenlabs.php' => '/v1/elevenlabs',
    ];
    return $map[$script] ?? '/voice';
}

function phone_proxy_twiml_error(string $message) {
    http_response_code(200);
    header('Content-Type: text/xml; charset=UTF-8');
    $safe = htmlspecialchars($message, ENT_XML1 | ENT_QUOTES, 'UTF-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>';
    echo '<Response><Say voice="Polly.Matthew">I am sorry, the phone assistant is temporarily unavailable. '.$safe.'</Say><Hangup/></Response>';
    exit;
}

function phone_proxy_rewrite_twiml(string $response): string {
    // The Mac phone agent emits TwiML paths relative to its own origin:
    // /respond, /listen, /poll, /voice. Once Twilio enters through IONOS,
    // those must stay inside the hidden /phone/*.php proxy endpoints.
    $replacements = [
        'action="/respond"' => 'action="/phone/respond.php"',
        "action='/respond'" => "action='/phone/respond.php'",
        'action="/listen"' => 'action="/phone/listen.php"',
        "action='/listen'" => "action='/phone/listen.php'",
        'action="/voice"' => 'action="/phone/voice.php"',
        "action='/voice'" => "action='/phone/voice.php'",
        '>/listen<' => '>/phone/listen.php<',
        '>/voice<' => '>/phone/voice.php<',
        '>/respond<' => '>/phone/respond.php<',
        '>/poll?' => '>/phone/poll.php?',
        'url="/v1/elevenlabs' => 'url="/phone/elevenlabs.php',
        "url='/v1/elevenlabs" => "url='/phone/elevenlabs.php",
    ];
    return strtr($response, $replacements);
}

function phone_proxy_emit_response(int $status, string $contentType, string $response) {
    if (stripos($contentType, 'xml') !== false || strpos($response, '<Response') !== false) {
        $response = phone_proxy_rewrite_twiml($response);
        $contentType = 'text/xml; charset=UTF-8';
    }
    http_response_code($status >= 200 && $status < 500 ? $status : 200);
    header('Content-Type: ' . ($contentType !== '' ? $contentType : 'text/xml; charset=UTF-8'));
    echo $response;
    exit;
}

function phone_proxy_request() {
    $cfg = phone_proxy_config();
    $path = phone_proxy_target_path();
    $query = (string)($_SERVER['QUERY_STRING'] ?? '');
    $url = $cfg['base'] . $path . ($query !== '' ? '?' . $query : '');

    $method = strtoupper((string)($_SERVER['REQUEST_METHOD'] ?? 'POST'));
    $body = file_get_contents('php://input');
    if ($body === false) {
        $body = '';
    }

    // Prefer cURL if available. IONOS PHP commonly enables it.
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => false,
            CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_CONNECTTIMEOUT => 8,
            CURLOPT_TIMEOUT => max(10, $cfg['timeout']),
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => [
                'Content-Type: ' . ((string)($_SERVER['CONTENT_TYPE'] ?? 'application/x-www-form-urlencoded')),
                'X-Rae-Proxy: ionos-phone-bridge',
            ],
        ]);
        if ($method !== 'GET' && $method !== 'HEAD') {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }
        $response = curl_exec($ch);
        $errno = curl_errno($ch);
        $error = curl_error($ch);
        $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $ctype = (string)curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
        curl_close($ch);

        if ($errno !== 0 || $response === false || $status >= 500 || trim((string)$response) === '') {
            phone_proxy_twiml_error('Upstream bridge did not answer.');
        }
        phone_proxy_emit_response($status, $ctype, (string)$response);
    }

    // Fallback for PHP installations without cURL.
    $opts = [
        'http' => [
            'method' => $method,
            'header' => "Content-Type: " . ((string)($_SERVER['CONTENT_TYPE'] ?? 'application/x-www-form-urlencoded')) . "\r\nX-Rae-Proxy: ionos-phone-bridge\r\n",
            'content' => ($method !== 'GET' && $method !== 'HEAD') ? $body : '',
            'timeout' => max(10, $cfg['timeout']),
            'ignore_errors' => true,
        ],
    ];
    $response = @file_get_contents($url, false, stream_context_create($opts));
    if ($response === false || trim($response) === '') {
        phone_proxy_twiml_error('Upstream bridge did not answer.');
    }
    header('Content-Type: text/xml; charset=UTF-8');
    echo phone_proxy_rewrite_twiml($response);
    exit;
}
