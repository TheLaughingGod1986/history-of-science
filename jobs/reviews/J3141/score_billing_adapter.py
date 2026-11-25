"""Offline adapter for one proposed HOS 009 score flight.

This is a design stand-in. It does not import the live client, the live
recorder, or a generator, and it does not open a socket. The mocked
transport is called for one subscription read and, only after consume,
at most one music post.

Live el_client.request still performs its own subscription GET inside
before_spend, and generate_music_bed.py --generate still reaches that
path. INTEGRATION_DIFF.md describes the change that would close both.
That diff is not applied.
"""

from __future__ import annotations

from score_billing_guard import GuardRefused, read_subscription, recorder_held


def proposed_flight(board: object, transport: object, request: object) -> dict:
    """One GET, then decide, then consume, then at most one POST.

    A second call on a board that already decided does not fetch again.
    A refusal does not post. The recorder lock is not taken or released here.
    """
    if not recorder_held():
        raise GuardRefused("shared_meter")
    if getattr(board, "used", False):
        raise GuardRefused("retry_or_shared_meter")
    get = getattr(transport, "get_subscription", None)
    post = getattr(transport, "post_music", None)
    if not callable(get) or not callable(post):
        raise GuardRefused("untrusted_receipt")
    receipt = read_subscription(get)
    token = board.decide(receipt, request=request)
    spent = board.consume(token, body_sha256=token["body_sha256"])
    if not recorder_held():
        raise GuardRefused("shared_meter")
    post(spent)
    return spent
