import unittest
import numpy as np
from _j2242_caption_source_map import measure

class CandidateMapping(unittest.TestCase):
    def test_recovers_skipped_and_repeated_native_frames(self):
        source=np.array([[0,1],[20,21],[40,41],[60,61]],dtype=np.uint8)
        result=measure(source[[0,1,1,3]],source)
        self.assertEqual(result['source_frame_indices'],[0,1,1,3])
        self.assertEqual(result['maximum_mse'],0)
        self.assertEqual(result['ambiguous_local_frames'],[])
    def test_flags_ambiguous_identical_candidates(self):
        result=measure(np.zeros((2,3),dtype=np.uint8),np.zeros((4,3),dtype=np.uint8))
        self.assertEqual(result['ambiguous_local_frames'],[0,1])
    def test_flags_poor_and_backwards_matches(self):
        source=np.array([[0,1],[20,21],[40,41]],dtype=np.uint8)
        result=measure(np.array([[40,41],[0,1],[100,101]],dtype=np.uint8),source)
        self.assertEqual(result['nonmonotonic_steps'],[1])
        self.assertEqual(result['poor_match_local_frames'],[2])
    def test_missing_frames_refused(self):
        with self.assertRaises(ValueError):measure([],[[1]])

if __name__=='__main__':unittest.main()
