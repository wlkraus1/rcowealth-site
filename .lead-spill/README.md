# Lead spill

Written **only** when `lead.php` could not send the notification email. Each line
is one enquiry that reached the site and did not reach the inbox.

If this file is not empty, mail from the webspace is broken — fix that first, then
enter the leads by hand and empty the file. It is not a queue anything drains
automatically, on purpose: a silent auto-drain would hide the mail failure that
put them here.
