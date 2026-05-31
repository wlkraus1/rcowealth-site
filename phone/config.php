<?php
// Rae & Co stable Twilio phone bridge proxy config.
// This file intentionally contains no secrets. The upstream is the current
// public tunnel to the local Mac phone agent. Twilio calls the stable IONOS
// URL; IONOS forwards to this upstream.
return [
    'upstream_base_url' => 'https://spokesman-skin-paso-annually.trycloudflare.com',
    'proxy_timeout_seconds' => 20,
];
