# HOS 009 music price evidence — 19 November 2026

Retrieved 19 November 2026. Public pages only. No account GET, no login, no generation, no spend, and no change to billing settings.

Activation stays closed. A subscription-credit maximum of 3,000 and a cash charge of GBP 0 are not both established for one 180-second `music_v2` request.

## Published tariff, not an enforceable bound

Product pricing, <https://elevenlabs.io/pricing>:

> How many credits does each product use?
>
> All products draw from one shared monthly credit pool, so the same credits can be spent on any of them and using one leaves fewer for the others. Approximate credit costs are: Text to Speech 1 credit per character; Speech to Text 330 credits per minute; Eleven Music 900 credits per minute; Sound Effects 200 credits per generation; Voice Changer and Voice Isolator 1,000 credits per minute; and Dubbing 2,000 credits per minute (automatic with watermark), 3,000 (automatic without watermark), 5,000 (Dubbing Studio with watermark) or 10,000 (Dubbing Studio without watermark).

> Is there a limit on how many credits I can use in a single request?
>
> Yes. There is a maximum number of credits that can be used in a single generation request. The limit depends on whether you are on the Free tier or a paid subscription.

Three minutes at the labelled approximate rate is 2,700 credits. The page calls that rate approximate. It does not name `music_v2`, `music_length_ms=180000`, `force_instrumental`, or `output_format=mp3_44100_128`. It does not give the single-request maximum as a number.

API pricing, <https://elevenlabs.io/pricing/api>:

> What are the per-product API rates?
>
> API usage is billed in US dollars, not credits. Text to Speech $0.08 per 1,000 characters (multilingual models) or $0.04 (Flash/Turbo). Speech to Text $0.20 per hour (Scribe) or $0.22 per hour (Scribe realtime), with keyterm prompting $0.05 per hour and transcript editing $0.07 per hour. Eleven Music $0.15 per minute. Voice Changer and Voice Isolator $0.12 per minute. Sound Effects $0.12 per minute. Dubbing $0.33 per minute (automatic with watermark), $0.50 (automatic without watermark) or $0.50 (Dubbing Studio). Prices exclude taxes.

> How is usage metered?
>
> Text to Speech is billed per character. Speech to Text is billed per audio minute. Music and Sound Effects are billed per generation. Dubbing is billed per source audio minute.

The same page prices Music at $0.15 and shows a five-minute duration limit. Three minutes at that cash rate is $0.45. That is not GBP 0. The FAQ states the API unit is US dollars, not credits.

The compose reference, <https://elevenlabs.io/docs/api-reference/music/compose>, lists `POST /v1/music`, `model_id` values including `music_v2`, and `music_length_ms` from 3,000 to 600,000. It does not state a credit price or a character-meter mapping.

## What these pages do not prove

The two pricing pages do not agree on the unit. Neither page states all of the following for this exact request:

1. The subscription-credit integer charged for `POST /v1/music` with `model_id=music_v2`, `music_length_ms=180000`, `force_instrumental=true` and `output_format=mp3_44100_128`.
2. The numeric maximum credits one paid-plan generation may consume. The product FAQ says a maximum exists and does not give it.
3. How `character_count` on `GET /v1/user/subscription` moves for that charge. No public ratio is stated.
4. That the same request creates no cash invoice, in GBP or USD, while subscription credits remain and overage is off. The API FAQ says API usage is billed in US dollars, not credits.

## Historical figures that are not a guarantee

One earlier 180-second take moved 2,475 credits, and the character meter moved by the same 2,475 (43,725 minus 41,250). A published 900-credit minute is 2,700 for three minutes. A recorded margin on that take is 2,970. Those numbers describe that take. They are not a current price, and they are not used here as one.

The three subscription names `bfcm_2026_offer`, `creator_arm_price` and `is_annual_four_months_subscriber` are still untyped on the public pages. A nested value still refuses. No account call was made to learn the type.

## No-spend route for the elected Chief

Do not activate this flight and do not request an account read to discover the price.

- Do not generate a wonder cue.
- Do not reuse `hos_009_wonder_v01.mp3` (`95dfe11d7c21c9347e9b962ef2f9ecd35116f2fce60df6f123578c11a1debaf0`). It failed the reuse gate.
- Do not reuse `hos_009_wonder_v02.mp3` (`b38ae8922e8d633b9f085a8bb9634c96d889a9293fcab277f7a3a23f4839d148`). It failed the listening review.
- Do not loop, stretch or re-encode `hos_009_teach_v01.mp3` (`4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1`) across the opening. The teach cue does not cover 0–175.28s, and the earlier ruling already forbids that repair.
- Keep the long assembly and the Shorts held. Do not schedule the film.

There is no existing score file that can fill the opening inside the rules. The route is to leave that opening unscored and keep the film unscheduled until a later scope has a proven price and its own allowance. This file does not open that allowance. The J3043/J3045 allowance stays closed.
