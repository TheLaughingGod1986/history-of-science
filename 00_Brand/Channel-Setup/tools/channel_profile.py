"""History of Science's settings for the shared channel tools (studio core, Ben 15 Oct 2026: "unify HOS and OWB but
keeping their own rules"). Each repo keeps its own copy of this file; the tools that read it are identical in both."""

NAME = "History of Science"
HANDLE = "HistoryOfScienceYT"
# Orbit's robot detector misfires on HOS's warm lamp light, so it is off here; check the Explorer is not at frame 0 by eye.
ROBOT_FRAME0_CHECK = False
ROBOT_NAME = "the Explorer"
SHORTS_LOG = "audits/SHORTS_LOG.md"
