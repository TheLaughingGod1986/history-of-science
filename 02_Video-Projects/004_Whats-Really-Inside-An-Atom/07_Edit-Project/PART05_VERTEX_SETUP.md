# Part 05 — Vertex AI Veo setup (Ben Free Trial test)

**Status (28 Sep 2026 evening):** `gcloud` installed on Mini. **ADC not yet authorized** — needs Ben browser sign-in. No Vertex mint until ADC + project are set.

## Why stop

`gcloud auth application-default login` requires Google account consent in a browser. Agent must not work around that.

## What Ben must do (exact clicks)

On the **Mac mini** (Terminal, History of Science checkout):

1. Open Terminal.
2. Run:
   ```bash
   export PATH="/opt/homebrew/bin:$PATH"
   gcloud auth application-default login
   ```
3. Browser opens (or prints a URL — open it).
4. Sign in as the Google account that owns the **Orbit API** billing / Gemini key project (same GCP project as the AI Studio key).
5. Click **Allow** / consent for Application Default Credentials (Cloud Platform scope).
6. Return to Terminal; confirm it says credentials saved.
7. Set the project id (replace with the real Orbit / History of Science project id):
   ```bash
   gcloud config set project YOUR_GCP_PROJECT_ID
   gcloud services enable aiplatform.googleapis.com --project=YOUR_GCP_PROJECT_ID
   ```
   Or add to the Part 05 / Periodic Table `.env` (no keys in chat):
   ```
   GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
   GOOGLE_CLOUD_LOCATION=us-central1
   ```
8. Tell the agent to resume the **ONE Fast Vertex test** (`09_one_rung_each` — plate 08 is Quality glow).

## Mint command (after auth — agent will run this)

```bash
cd "/Users/benjaminoats/YouTube/History Of Science"
.venv_hos_veo/bin/python \
  02_Video-Projects/004_Whats-Really-Inside-An-Atom/07_Edit-Project/_mint_part05_flow_cdp_v01.py \
  --vertex-test 09_one_rung_each
```

- Models: Fast `veo-3.1-fast-generate-001` · Quality `veo-3.1-generate-001`
- Region: `us-central1`
- Log: `path=vertex` per plate
- **ONE plate only** until Ben confirms Free Trial £225 applied in Cloud Billing (~24h)

## Do not

- Do not mint further Vertex plates before billing confirm
- Do not print keys / tokens / ADC JSON
- Tomorrow 08:30 continues remaining plates on AI Studio prepay after Ben top-up
