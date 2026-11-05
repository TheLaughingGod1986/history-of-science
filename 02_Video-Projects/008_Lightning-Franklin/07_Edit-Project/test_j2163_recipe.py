import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('recipe', Path(__file__).with_name('_build_rough_v13_recipe.py'))
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

class PlannerTests(unittest.TestCase):
    def fixture(self):
        return [{'pts':125,'duration':40,'key_frame':1},
                {'pts':165,'duration':40,'key_frame':0},
                {'pts':245,'duration':40,'key_frame':0},
                {'pts':285,'duration':40,'key_frame':1}], {'time_base':'1/1000','start_pts':125,'duration_ts':200}

    def test_actual_start_and_gap_survive(self):
        raw, stream = self.fixture(); t=r.validate_frames(raw,stream,4)
        self.assertEqual(t['start_pts'],125)
        self.assertEqual(t['gaps'],[{'after_frame':1,'delta_ticks':40}])
        p=r.build_plan(t,[{'candidate_frames':[1,2]}])[0]
        self.assertEqual([f['pts'] for f in p['source_frame_schedule']],[165,245])
        self.assertEqual(p['candidate_boundary_gop_envelope'],[0,2])
        self.assertFalse(p['pts_reconciled'])

    def test_short_decode_rejected(self):
        raw,s=self.fixture()
        with self.assertRaises(r.PlanError):r.validate_frames(raw[:-1],s,4)
        with self.assertRaises(r.PlanError):r.validate_frames(raw[:-1],s)

    def test_missing_timestamp_rejected(self):
        raw,s=self.fixture();del raw[1]['pts']
        with self.assertRaises(r.PlanError):r.validate_frames(raw,s)

    def test_nonmonotonic_rejected(self):
        raw,s=self.fixture();raw[1]['pts']=125
        with self.assertRaises(r.PlanError):r.validate_frames(raw,s)

    def test_decoder_failure_and_stderr_rejected(self):
        for code,err in [(1,'broken decoder'),(0,'corrupt packet')]:
            with patch.object(r.sp,'run',return_value=subprocess.CompletedProcess([],code,'{}',err)):
                with self.assertRaises(r.PlanError):r.strict_json(['ffprobe'])

    def test_hash_size_missing_and_overwrite_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'input';p.write_bytes(b'original')
            with self.assertRaises(r.PlanError):r.require_hash(p,'0'*64)
            with self.assertRaises(r.PlanError):r.require_hash(p,r.sha256_file(p),99)
            with self.assertRaises(r.PlanError):r.require_hash(Path(tmp)/'missing','0'*64)
            with self.assertRaises(FileExistsError):r.write_new(p,{})
            self.assertEqual(p.read_bytes(),b'original')

    def test_explicit_missing_retake_has_no_fallback(self):
        with self.assertRaises(r.PlanError):r.verify_plan(retakes={'p2':{'path':'/nonexistent-retake','sha256':'0'*64}})

    def test_short_explicit_retake_refused(self):
        with patch.object(r, 'require_hash'), patch.object(r, 'probe_video', return_value={'decoded_frames': 159}):
            with self.assertRaises(r.PlanError):
                r.verify_plan(retakes={'p2_02': {'path': 'fixture', 'sha256': '0'*64}})

    def test_overlapping_or_unavailable_patch_refused(self):
        raw, stream = self.fixture(); t=r.validate_frames(raw, stream, 4)
        for rows in ([{'candidate_frames':[1,2]}, {'candidate_frames':[2,3]}], [{'candidate_frames':[1,4]}]):
            with self.assertRaises(r.PlanError):r.build_plan(t, rows)

    def test_execution_is_unconditionally_refused(self):
        with self.assertRaises(r.PlanError):r.execute_recipe()
        with self.assertRaises(r.PlanError):r.extract_unchanged_range()
        proc=subprocess.run(['python3',str(Path(r.__file__)),'--execute'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2);self.assertIn('refused',proc.stderr)

    def test_manifest_safe_windows_and_missing_assets(self):
        d=json.loads(Path(r.__file__).with_name('J2163_CORRECTION_MANIFEST.json').read_text())
        self.assertEqual([x['candidate_frames'] for x in d['six_rows']],[[427,544],[744,839],[2506,2665],[3260,3343],[4977,5077],[11358,11492]])
        for i in [2,5]:self.assertFalse(d['six_rows'][i]['recipe']['generation_proposal']['authorized'])
        self.assertNotIn('3,600',json.dumps(d))

    def test_eight_item_amend_stays_unresolved_and_unbordered(self):
        d = r.load_manifest()
        self.assertEqual(d['execution'], 'REFUSED_UNTIL_J1881_REREVIEW')
        self.assertEqual([x['timestamp'] for x in d['eight_rows']],
                         ['00:20', '0:30', '0:51', '1:49', '2:20', '3:13', '3:31', '7:58'])
        self.assertEqual([x['candidate_frames'] for x in d['eight_rows']],
                         [[427, 544], [744, 839], [1124, 1227], [2506, 2665],
                          [3260, 3343], [4500, 4659], [4977, 5077], [11358, 11492]])
        self.assertFalse(d['eight_rows'][2]['same_source_as_1_49'])
        self.assertEqual(d['eight_rows'][2]['hair_tube_source']['candidate_frames'], [2506, 2665])
        self.assertFalse(d['eight_rows'][2]['recipe']['generation_proposal']['authorized'])
        self.assertFalse(d['eight_rows'][3]['recipe']['generation_proposal']['authorized'])
        self.assertFalse(d['eight_rows'][5]['recipe']['generation_proposal']['authorized'])
        self.assertFalse(d['eight_rows'][7]['recipe']['generation_proposal']['authorized'])
        flip = d['eight_rows'][4]['jar_flip_2_18']
        self.assertEqual(flip['master_frame'], 3305)
        self.assertTrue(flip['inside_replace_3260_3343'])
        self.assertFalse(flip['inside_keep_3168_3259'])
        self.assertFalse(flip['new_row'])
        cap = d['caption_treatment']
        self.assertEqual(cap['scope'], 'every_bottom_onscreen_text_over_moving_footage')
        self.assertGreater(len(cap['labels']), 8)
        self.assertTrue(all(lab['splice'] is False for lab in cap['labels']))
        self.assertIn('J1755', '\n'.join(d['holds']))
        self.assertTrue(all(row['status'].startswith('UNRESOLVED') for row in d['eight_rows']))

    def test_clocks_map_on_stored_master_pts(self):
        pts = json.loads(Path(r.__file__).with_name('J2163_MASTER_FRAME_PTS.json').read_text())
        self.assertEqual(pts['master_sha256'], r.MASTER_SHA)
        self.assertEqual(r.clock_frame(pts['frames'], pts['time_base'], 51), 1220)
        self.assertEqual(r.clock_frame(pts['frames'], pts['time_base'], 193), 4621)
        self.assertEqual(r.clock_frame(pts['frames'], pts['time_base'], 138), 3305)
        self.assertEqual(r.clock_frame(pts['frames'], pts['time_base'], 479), 11469)
        timeline = {'frames': [{'index': f[0], 'pts': f[1], 'duration': f[2], 'key_frame': f[3]} for f in pts['frames']]}
        patches = r.build_plan(timeline, r.load_manifest()['eight_rows'])
        self.assertEqual(len(patches), 8)
        self.assertEqual(patches[2]['measured_pts_in'], timeline['frames'][1124]['pts'])
        self.assertEqual(timeline['frames'][1220]['pts'], 626688)
        self.assertEqual(patches[5]['measured_pts_in'], timeline['frames'][4500]['pts'])
        self.assertEqual(timeline['frames'][4621]['pts'], 2371584)
        self.assertEqual(timeline['frames'][3305]['pts'], 1695744)
        self.assertTrue(all(p['pts_reconciled'] is False for p in patches))
        self.assertNotIn('caption_treatment', patches[0])

    def test_execution_names_the_j1881_rereview(self):
        with self.assertRaises(r.PlanError) as caught:
            r.execute_recipe()
        self.assertIn('J1881', str(caught.exception))
        self.assertIn('eight-item', str(caught.exception))

if __name__=='__main__':unittest.main(verbosity=2)
