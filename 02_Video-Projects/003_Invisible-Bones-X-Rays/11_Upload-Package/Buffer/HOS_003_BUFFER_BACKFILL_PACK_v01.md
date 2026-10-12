# HOS 003 X-rays: Buffer backfill pack v01 (TikTok + IG Reels)

Status: DRAFT for UAT. Drafted by Showrunner 5 Oct 2026 12:00 London. Ben GO on scheduling 11:58 (one-time look done). UAT PASS = CoS green. Nothing is scheduled yet.
Route: Buffer API with BUFFER_HOS_API_KEY only (org 6431f03385378b838b780157). Never the Orbit Buffer connector. YouTube stays in Studio.
Channels: TikTok @historyofscienceyt 6ac381bc6a5c39ccb61dd8aa, Instagram (Reels) 6ac36d3c6a5c39ccb61d3b5f. No Facebook post in this pack.

## Schedule (Europe/London, one a day at 11:30; TikTok and Reels go out together)
| Day | Short | YouTube (live) |
|---|---|---|
| Tue 6 Oct 11:30 | S1 | oowAOWTBoq0 |
| Wed 7 Oct 11:30 | S2 | xvanpsLeADE |
| Thu 8 Oct 11:30 | S3 | zI_eD3vFWmE |
Start date set by CoS: Tue 6 Oct (Ben GO on scheduling 5 Oct 11:58, his one-time look). After UAT PASS, it is green from CoS.

## Masters (clean files, the UAT-passed originals, NOT YouTube downloads)
Folder: 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/ (an identical copy is in iCloud HOS UAT/)
- S1 hos_003_s1_cardboard_glow_v01.mp4, sha256 a06967893af11465bdd6571011e92ad140e559c2fb14cd4a27f6c9e30d72aded
- S2 hos_003_s2_bones_no_knife_v01.mp4, sha256 3bb67af65c87c969fe35c5017ff1b3063d486277925fbb27b4fbf1a550707492
- S3 hos_003_s3_bertha_ring_v01.mp4, sha256 911f546882c2164ca663bf1a01348c63b14b804b2357969dbc7fe288475a54c7
All three are 1080x1920, h264/aac, 24 fps, 24.0 s. First and last frames are in hos_003_buffer_frames_first_last_v01.jpg. There's no end card, no subscribe graphic, and no "watch on YouTube" card.

## Captions
The first line is the locked Short title, word for word. Neither TikTok nor IG makes caption links clickable, so the captions name the film and give no URL.

### S1 (Tue 6 Oct)
TikTok:
How X-rays Were Discovered by Accident
A covered tube. A cardboard screen that should have stayed dark, and glowed anyway. That accident is how X-rays began.
Full film: "How Did We Discover X-rays?" on History of Science, YouTube.
#xrays #historyofscience #science #röntgen #sciencetok

IG Reels:
How X-rays Were Discovered by Accident
A covered tube. A cardboard screen that should have stayed dark, and glowed anyway. That accident is how X-rays began.
The full story is on our YouTube channel, History of Science.
#xrays #historyofscience #sciencehistory #röntgen #physics

### S2 (Wed 7 Oct)
TikTok:
How did Röntgen see bones without cutting
Soft tissue fades. Bone holds. Röntgen saw a living skeleton without a knife.
Full film: "How Did We Discover X-rays?" on History of Science, YouTube.
#xrays #historyofscience #science #röntgen #sciencetok

IG Reels:
How did Röntgen see bones without cutting
Soft tissue fades. Bone holds. Röntgen saw a living skeleton without a knife.
The full story is on our YouTube channel, History of Science.
#xrays #historyofscience #sciencehistory #röntgen #anatomy

### S3 (Thu 8 Oct)
TikTok:
The first X-ray showed a wedding ring
The first X-ray proof was Bertha Röntgen's hand: her bones, and the darker shadow of her wedding ring.
Full film: "How Did We Discover X-rays?" on History of Science, YouTube.
#xrays #historyofscience #science #womeninscience #sciencetok

IG Reels:
The first X-ray showed a wedding ring
The first X-ray proof was Bertha Röntgen's hand: her bones, and the darker shadow of her wedding ring.
The full story is on our YouTube channel, History of Science.
#xrays #historyofscience #sciencehistory #womeninscience #physics

## Rules
Zero /go/ or affiliate links. No Orbit wording. Covers use the platform default frame for now (TikTok and Reels pick from the video, and none open on Explorer).

## At scheduling (after the CoS green only)
- Re-check the sha256 of the exact file handed to Buffer against the values above.
- The Buffer API takes media by URL, so the master needs a temporary direct link. The link host gets picked at scheduling time, and no file is re-encoded.
- Read each queued post back from Buffer (channel, time, caption) and log the evidence to Buffer/evidence_<date>/.
