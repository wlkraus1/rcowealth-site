# Phone TwiML front door

Static IONOS-hosted TwiML used as the stable Twilio voice webhook.

Twilio should point to:

`https://rcowealth.com/phone/voice.xml`

The XML keeps `https://rcowealth.com/phone/voice.xml` as Twilio's stable front door while handing speech callbacks to the current Mac phone-agent backend. When the backend tunnel rotates, update the absolute backend URL in `voice.xml` and `listen.xml`, redeploy, and leave Twilio unchanged.
