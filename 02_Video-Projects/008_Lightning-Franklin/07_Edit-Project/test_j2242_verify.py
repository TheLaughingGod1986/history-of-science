"""Reject timestamp, pixel, packet and scope corruption independently."""
import copy
import unittest
from _j2242_verify_output import verify, ranges, parse_hashes

class PreservationTests(unittest.TestCase):
    def fixture(self):
        timeline = {'time_base': '1/12288', 'frames': [
            {'pts': p, 'duration': 512} for p in (1536, 2048, 3072, 3584)]}
        hashes = [(f['pts'], 512, 6, 'a'*64) for f in timeline['frames']]
        probe = {'streams': [
            {'index': 0, 'codec_type': 'video', 'codec_name': 'h264', 'time_base': '1/12288'},
            {'index': 1, 'codec_type': 'audio', 'codec_name': 'aac', 'time_base': '1/48000'}],
            'packets': [dict(stream_index=0, pts=f['pts'], dts=f['pts']-1024,
                             duration=512, size=3, data_hash='SHA256:abc', flags='K_')
                        for f in timeline['frames']] + [
                dict(stream_index=1, pts=-1024, dts=-1024, duration=1024,
                     size=4, data_hash='SHA256:def', side_data_list=[{'skip_samples': 1024}])]}
        return [timeline, probe, hashes, copy.deepcopy(timeline), copy.deepcopy(probe),
                list(hashes), {'modified_frames': [[1, 1]], 'encoded_envelopes': [[0, 1]]}, [0, 2]]

    def test_preserves_nonuniform_clock(self):
        self.assertEqual(verify(*self.fixture())['unchanged_decoded_frames_verified'], 3)

    def test_allowed_patch_only(self):
        a = self.fixture()
        a[5][1] = (*a[5][1][:3], 'b'*64)
        a[4]['packets'][1]['data_hash'] = 'changed'
        self.assertEqual(verify(*a)['copied_video_packets_verified'], 2)

    def test_rejects_unchanged_pixel_inside_encoded_envelope(self):
        a = self.fixture()
        a[5][0] = (*a[5][0][:3], 'b'*64)
        with self.assertRaisesRegex(ValueError, 'Unchanged decoded'):
            verify(*a)

    def test_rejects_video_packet_change_outside_envelope(self):
        a = self.fixture()
        a[4]['packets'][2]['data_hash'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'Copied GOP'):
            verify(*a)

    def test_rejects_audio_changes(self):
        for field, value in [('pts', 0), ('dts', 0), ('duration', 512),
                             ('data_hash', 'changed'), ('side_data_list', [])]:
            a = self.fixture()
            a[4]['packets'][-1][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'audio packets'):
                verify(*a)

    def test_rejects_collapsed_gap_and_changed_duration(self):
        for field in ('pts', 'duration'):
            a = self.fixture()
            a[3]['frames'][2][field] -= 512
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'frame count, PTS'):
                verify(*a)

    def test_rejects_out_of_scope_and_non_idr(self):
        for contract in [
            {'modified_frames': [[2, 2]], 'encoded_envelopes': [[0, 1]]},
            {'modified_frames': [[1, 1]], 'encoded_envelopes': [[1, 1]]}]:
            a = self.fixture()
            a[6] = contract
            with self.assertRaises(ValueError):
                verify(*a)

    def test_bad_ranges(self):
        for value in [[[0, 2], [2, 3]], [[-1, 1]], [[0, 4]], [[True, 2]], [[2, 1]]]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                ranges(value, 4)

    def test_rejects_missing_or_wrong_hash_clock(self):
        for text in ['', '#tb 0: 1/24\n0,0,0,1,6,' + 'a'*64]:
            with self.assertRaises(ValueError):
                parse_hashes(text)

if __name__ == '__main__':
    unittest.main()
