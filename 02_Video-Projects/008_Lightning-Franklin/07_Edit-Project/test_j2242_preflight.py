import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import _j2242_source_preflight as p


class PreflightTests(unittest.TestCase):
    def test_truncated_and_empty_nals_rejected(self):
        for data in (b'\0', b'\0\0\0\0', b'\0\0\0\x05\x65'):
            with self.assertRaises(ValueError):
                p.nal_types(data, 4)
        self.assertEqual(p.nal_types(b'\0\0\0\x01\x65', 4), [5])

    def fixture(self, directory, nal=5):
        payload = b'\0\0\0\x01' + bytes([nal])
        source = Path(directory) / 'sample'
        source.write_bytes(payload)
        probe = {'streams': [
            {'index': 0, 'codec_type': 'video', 'codec_name': 'h264',
             'is_avc': 'true', 'nal_length_size': '4', 'time_base': '1/12288'},
            {'index': 1, 'codec_type': 'audio'}],
            'packets': [{'stream_index': 0, 'pts': 1536, 'pos': 0,
                         'size': len(payload), 'flags': 'K_',
                         'data_hash': 'SHA256:' + hashlib.sha256(payload).hexdigest()},
                        {'stream_index': 1}]}
        timeline = {'time_base': '1/12288',
                    'frames': [{'index': 0, 'pts': 1536, 'key_frame': 1}]}
        return source, probe, timeline

    def test_keyflag_without_idr_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source, probe, timeline = self.fixture(directory, nal=1)
            with self.assertRaisesRegex(ValueError, 'all-IDR'):
                p.inspect_packets(source, probe, timeline)

    def test_actual_idr_accepted_and_corrupt_packet_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source, probe, timeline = self.fixture(directory)
            with patch.object(p.recipe, 'EXPECTED_FRAMES', 1):
                result = p.inspect_packets(source, probe, timeline)
                self.assertTrue(result['all_random_access_samples_are_idr'])
                self.assertEqual(result['idr_frame_indices'], [0])
                probe['packets'][0]['data_hash'] = 'SHA256:' + '0' * 64
                with self.assertRaisesRegex(ValueError, 'packet bytes'):
                    p.inspect_packets(source, probe, timeline)

    def test_duplicate_pts_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source, probe, timeline = self.fixture(directory)
            probe['packets'].append(probe['packets'][0].copy())
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                p.inspect_packets(source, probe, timeline)


if __name__ == '__main__':
    unittest.main()
