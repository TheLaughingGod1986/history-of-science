# Professional Voice Clone audit

## Finding

The Professional Voice Clone is a separate voice from the previous
`Ben Orbit Narrator` Instant Voice Clone. ElevenLabs currently displays the
Professional Clone under the generic name
`My Professional Voice Cloneitled voice`.

The settings present when the voice was opened were:

- speed 1.13
- stability 0.77
- similarity 0.53
- style exaggeration 0.40
- speaker boost on

Those settings favour speed and consistency over a natural documentary
performance and are likely to contribute to the robotic quality.

## Tuned test

The controlled test uses:

- Eleven Multilingual v2
- speed 0.93
- stability 0.55
- similarity 0.80
- style exaggeration 0.08
- speaker boost on
- MP3 44.1 kHz, 128 kbps source download

Test duration: 13.27 seconds.

The original test remains untouched. Two non-destructive post-processing
comparisons were created:

- `pvc_natural_test_v01_clean-gentle.mp3`
- `pvc_natural_test_v01_clean-strong.mp3`

The gentle version should be the default candidate. The stronger version is
only a diagnostic option because excessive denoising can remove breath and
natural vocal texture.

## Noise observation

The generated source has an overall measured noise floor of approximately
-40.5 dBFS. Quiet-frame analysis shows low-frequency energy near mains-hum
territory plus other narrow components. This does not prove the original
training recording is the sole cause, but it supports a listening comparison
before generating the full narration.

If hum remains clearly audible after the tuned settings and gentle cleaning,
the durable fix is to retrain the Professional Voice Clone from clean source
audio rather than applying increasingly aggressive processing to every
generation.

## Full-section cleanup check

The first five-minute Professional Voice Clone section had a measured noise
floor of approximately -44.4 dBFS. A new non-destructive gentle master applies:

- 68 Hz high-pass filtering;
- narrow reductions at 100 Hz and 200 Hz;
- seven-decibel adaptive spectral noise reduction;
- a 15.5 kHz low-pass filter;
- restrained documentary loudness normalisation.

The cleaned section measures approximately -57.2 dBFS at the noise floor,
around 13 dB quieter than the source. The raw generation remains untouched.

Comparison files:

- `aliens_vo_raw_35s_comparison.mp3`
- `aliens_vo_clean_35s_comparison.mp3`

Full cleaned files:

- `aliens_vo_bold-v05_section-01_pvc_clean-gentle_v02.wav`
- `aliens_vo_bold-v05_section-01_pvc_clean-gentle_v02.mp3`
