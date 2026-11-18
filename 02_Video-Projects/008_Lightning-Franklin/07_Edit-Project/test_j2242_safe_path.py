import unittest
from _j2242_caption_composites import source_runs
from _j2242_safe_path import (
    BODY_INDICES, FRAME_COUNT, UNUSED_BODY_FRAMES, accept_safe_path,
)


def _hit(best, mse=0, margin=4.0, second=None, same=None):
    row = {
        'best': best,
        'second': best - 1 if second is None else second,
        'best_mse': mse,
        'margin': margin,
    }
    if same is not None:
        row['same_picture'] = same
    return row


def exact():
    ranked = []
    for index in BODY_INDICES:
        margin = 0.02 if index in (44, 48) else 4.0
        same = True if margin < 0.1 else None
        ranked.append(_hit(index, margin=margin, second=index + 1 if index < 79 else index - 1, same=same))
    return ranked


class SafePath(unittest.TestCase):
    def test_pinned_schedule_holds_and_skips(self):
        self.assertEqual(len(BODY_INDICES), FRAME_COUNT)
        self.assertEqual(BODY_INDICES[0], 0)
        self.assertEqual(BODY_INDICES[-1], 79)
        self.assertEqual(BODY_INDICES.count(44), 2)
        self.assertEqual(BODY_INDICES.count(48), 3)
        self.assertTrue(all(frame not in BODY_INDICES for frame in UNUSED_BODY_FRAMES))
        self.assertEqual(source_runs(BODY_INDICES), [
            (0, 45), (44, 45), (46, 49), (48, 49), (48, 49), (51, 80),
        ])

    def test_accepts_only_the_exact_body_frames(self):
        self.assertEqual(accept_safe_path(exact()), list(BODY_INDICES))

    def test_rejects_a_different_inexact_or_short_schedule(self):
        changed = exact()
        changed[10] = _hit(11)
        weak = exact()
        weak[3] = _hit(BODY_INDICES[3], margin=0.02, same=False)
        inexact = exact()
        inexact[0] = _hit(0, mse=0.001)
        unused = exact()
        unused[0] = _hit(45, mse=0, margin=4)
        for ranked in (changed, weak, inexact, unused, exact()[:79]):
            with self.subTest(ranked=ranked[0]):
                with self.assertRaises(ValueError):
                    accept_safe_path(ranked)


if __name__ == '__main__':
    unittest.main()
