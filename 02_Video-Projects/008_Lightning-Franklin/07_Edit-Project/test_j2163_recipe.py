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

if __name__=='__main__':unittest.main(verbosity=2)
