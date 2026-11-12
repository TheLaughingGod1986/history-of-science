import copy
import unittest
from _j2242_caption_composites import eligible,row_clock

class CompositeScope(unittest.TestCase):
    def setUp(self):
        self.row=dict(timeline_frames=[2,4],source_frame_indices=[6,7,8],poor_match_local_frames=[],ambiguous_local_frames=[],nonmonotonic_steps=[])
        self.timeline=dict(time_base='1/12288',frames=[dict(index=i,pts=1536+i*512,duration=512) for i in range(5)])
    def test_only_contiguous_confident_maps(self):
        self.assertTrue(eligible(self.row))
        for field in ('poor_match_local_frames','ambiguous_local_frames','nonmonotonic_steps'):
            with self.subTest(field=field):self.assertFalse(eligible({**self.row,field:[1]}))
        for schedule in ([6,7,7],[6,7,9],[],[8,7,6]):
            self.assertFalse(eligible({**self.row,'source_frame_indices':schedule}))
    def test_original_clock_slice(self):
        self.assertEqual([f['index'] for f in row_clock(self.timeline,self.row)],[2,3,4])
    def test_wrong_map_count_short_clock_and_indices(self):
        bad=copy.deepcopy(self.row);bad['source_frame_indices'].pop()
        with self.assertRaises(ValueError):row_clock(self.timeline,bad)
        bad=copy.deepcopy(self.timeline);bad['frames'][3]['index']=5
        with self.assertRaises(ValueError):row_clock(bad,self.row)
        bad=copy.deepcopy(self.timeline);bad['frames'].pop()
        with self.assertRaises(ValueError):row_clock(bad,self.row)

if __name__=='__main__':unittest.main()
