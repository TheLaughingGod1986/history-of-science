# History of Science: rules for the studio

The studio engine (in orbit-with-ben today; see its `docs/MULTI_CHANNEL_PLAN.md`) reads this folder to plug this channel in:

- `channel.json`: who the channel is (slug `hos`, label `HOS`, YouTube handle), where its film state lives
  (`00_Brand/Channel-Setup/PIPELINE.json`), its share of the studio's production places, and how its pictures are
  made (`picture_route: flow_only`, which means Flow on the AI Ultra credits and never the priced Vertex route).
- This file: where an agent working on a History of Science job finds the channel's own rules.

Studio-wide rules always come first: the Ben gate, no spending past £0, never delete on the NAS, and Studio sign-ins
are Ben's. They live in orbit-with-ben's `AGENTS.md`. A channel can add rules, never remove one.

The channel's own rules are in this repo's `AGENTS.md` and the documents it lists as in force (HOS_STRATEGY,
THUMBNAIL_AND_TITLE_RULES, STUDIO_PLAYBOOK, YOUTUBE_GROWTH_AND_POLICY, CHANNEL_AUTHORITY, ...). Read those for any
HOS job.

To change how the studio treats this channel, change `channel.json` here through a PR. The engine picks it up on its
next pull.
