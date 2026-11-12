import copy
import unittest
from _j2242_caption_composites import eligible,row_clock,source_runs,source_graph

class CompositeScope(unittest.TestCase):
    def setUp(self):
        self.row=dict(timeline_frames=[2,4],source_frame_indices=[6,7,8],poor_match_local_frames=[],ambiguous_local_frames=[],nonmonotonic_steps=[])
        self.timeline=dict(time_base='1/12288',frames=[dict(index=i,pts=1536+i*512,duration=512) for i in range(5)])
    def test_only_confident_monotonic_maps(self):
        self.assertTrue(eligible(self.row))
        for field in ('poor_match_local_frames','ambiguous_local_frames','nonmonotonic_steps'):
            with self.subTest(field=field):self.assertFalse(eligible({**self.row,field:[1]}))
        for schedule in ([6,7,7],[6,7,9]):
            self.assertTrue(eligible({**self.row,'source_frame_indices':schedule}))
        for schedule in ([],[8,7,6],[-1,0,1],[True,2,3]):
            self.assertFalse(eligible({**self.row,'source_frame_indices':schedule}))
    def test_runs_preserve_repeats_and_skips(self):
        schedule=[0,0,2,3,4,8,9,9]
        runs=source_runs(schedule)
        self.assertEqual([i for a,b in runs for i in range(a,b)],schedule)
        self.assertEqual(runs,[(0,1),(0,1),(2,5),(8,10),(9,10)])
        self.assertIn('concat=n=5',source_graph(schedule))
        for bad in ([],[2,1],[0,-1],[0,True]):
            with self.assertRaises(ValueError):source_runs(bad)
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
