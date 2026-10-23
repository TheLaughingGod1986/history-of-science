# J0878 — compilation package draft, parked for Chief

Codex worker, 23 Oct 2026. Based on Chief-reviewed HOS PR #300 commit `3ba58733`; £0, no generation credits. No final OK or stage PASS is issued here.

Proposed question title: **How Did Experiments Explain Blood, Germs and Atoms?**
Cover hook: **FLASK PROOF**. The £0 builder reuses approved painted 001 art and the Explorer, replacing the old title in its clear left band with cream/gold Didot. Source: `00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg`. `PHONE_v01.jpg` and `STYLE_v01.jpg` both generated successfully (exit 0); worker inspected both. The words read at 168×94, remain off the flask, and retain the house palette and small Explorer. These tools produce sheets, not machine PASS verdicts; visual sign-off remains Chief's. Only one draft cover was requested by this job; further T&C variants remain for Chief.

## Checks and blockers

`npm run lint:package -- --film 099` exits 1, verbatim:

```
FAIL  02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package/PACKAGE_MANIFEST.json
   FAIL  [schedule.slot] schedule is Sun 2026-11-08 18:00 UK; longs go out Thu 18:00 UK
   warn  [captions] no captionsFile (captions from the script)
```

The job and OWB #99 comment 6361644928 explicitly authorize Sunday. The existing contract has no supported exception field. HOS AGENTS.md forbids overriding a failed gate; an incorrect check needs its own PR with Ben's OK. This worker has neither changed the contract nor substituted another date. Chief needs to resolve the authorized Sunday slot against that gate before upload.

`youtube:package` dry run succeeds (`ok: true`, `dryRun: true`, no platformPostId): would upload Private with `publishAt=2026-11-08T18:00:00.000Z`. See `DRY_RUN_v01.txt` and the dry-run result JSON. Dry-run `thumbnail api_done` and `scheduledOnPlatform: true` are simulated; **no thumbnail was set, no upload ran, and no live privacy/publishAt read-back exists**. No YouTube state changed. No Buffer post.

The draft copies the v02 chapter list exactly. The existing long descriptions for 005 and 006 contain Sources sections, copied into the draft. The descriptions located for 001, 002, 003 and 004 have no Sources line or bibliography. The job's requirement to carry every film's Sources line is therefore incomplete. Chief/listing research must supply those four source-approved lines; they must not be invented. No claim of a new fact check is made in the description.

Master remains on the mounted NAS at `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4`. Approved SHA-256: `8282ffa8eb09e3a7cf1420562d70e14a428a0ae0489b3fdeccf5e4aeffe98490`; 49:18. No scratch or NAS file deleted. Mini free space is about 10 GiB. Current/previous 028 and 029 renders are retained; this compilation's scratch is already on NAS and this job explicitly says not to delete scratch. No unrelated archive job was taken.

The four-week measurement plan is appended to `docs/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md`, pending a real upload id and release time. Local project container 099 is solely a discoverable input for the unmodified package-lint CLI, which only scans numbered project folders; it does not commission a new film or mark any film stage approved.

Next: Chief reviews title/cover, resolves the gate conflict and the four Sources lines, then worker reruns lint/dry-run, uploads once, reads back metadata and thumbnail result, and reports on HOS #180. No upload is ready to run yet.

Repository `check_all.sh` ran before push: 20 contract tests passed; full check exits 1 at the same compilation Sunday-slot failure. No gate code was changed.
