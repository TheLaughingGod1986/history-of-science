import copy
import unittest
from _j2242_opening_caption import validate_clock

class OpeningScope(unittest.TestCase):
    def setUp(self):
        self.timeline=dict(time_base='1/12288',frames=[dict(index=i,pts=1536+i*512,duration=512) for i in range(142)])
        self.layer=dict(row='01_kite_open',frame_in=0,frame_last=95,frame_count=96,
                        pts_in=1536,pts_end=50688,label='PHILADELPHIA 1752',overlay_position=[0,720])
    def test_exact_opening(self):
        self.assertEqual(len(validate_clock(self.timeline,self.layer)),142)
    def test_reject_changed_clock(self):
        for key in ('index','pts','duration'):
            t=copy.deepcopy(self.timeline);t['frames'][12][key]+=1
            with self.subTest(key=key),self.assertRaises(ValueError):validate_clock(t,self.layer)
    def test_reject_short_clock(self):
        self.timeline['frames'].pop()
        with self.assertRaises(ValueError):validate_clock(self.timeline,self.layer)
    def test_reject_layer_leak_or_wrong_label(self):
        for key,value in [('frame_last',141),('frame_count',142),('pts_end',74240),('label','WRONG'),('overlay_position',[0,0])]:
            layer={**self.layer,key:value}
            with self.subTest(key=key),self.assertRaises(ValueError):validate_clock(self.timeline,layer)

if __name__=='__main__':unittest.main()
