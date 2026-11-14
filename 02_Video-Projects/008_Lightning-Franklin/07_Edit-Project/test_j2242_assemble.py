import unittest

import _j2242_assemble as asm


def frames_of(*rows):
    return [{'pts': pts, 'duration': dur} for pts, dur in rows]


class AssembleSchedule(unittest.TestCase):
    def test_copied_packets_keep_their_decode_times(self):
        frames = frames_of((100, 512), (700, 512), (1300, 1024), (2400, 512))
        # Source decode order is 0, 2, 1, 3. Durations make the copied times.
        demux = [0, 2, 1, 3]
        source_dts = [80, 1616, 592, 2128]
        events = asm.schedule(demux, frames, source_dts, lambda index: index in (0, 3))
        by_index = {row['index']: row for row in events}
        self.assertEqual(by_index[0]['dts'], 80)
        self.assertEqual(by_index[3]['dts'], 2128)
        self.assertEqual([row['index'] for row in events], [0, 1, 2, 3])
        self.assertEqual(by_index[1]['dts'], 80 + 512)
        self.assertEqual(by_index[2]['dts'], 80 + 512 + 512)
        self.assertEqual(events[1]['dts'] - events[0]['dts'], events[0]['duration'])
        self.assertEqual(asm.clock_ok(events, frames)[1024], 1)

    def test_a_high_run_stays_together_when_decode_order_splits_it(self):
        frames = frames_of((0, 512), (512, 512), (1024, 512), (1600, 1024))
        # Frame 2 is an exact picture decoded before the high run's second frame.
        demux = [0, 2, 1, 3]
        source_dts = [0, 1024, 512, 1536]
        events = asm.schedule(demux, frames, source_dts, lambda index: index == 3)
        self.assertEqual([row['index'] for row in events], [0, 1, 2, 3])
        asm.high_runs_contiguous(events, [
            {'role': 'high_encode', 'first': 0, 'last': 1},
            {'role': 'exact_pcm', 'first': 2, 'last': 2},
            {'role': 'packet_copy', 'first': 3, 'last': 3, 'clip': 'master_packets'},
        ])

    def test_no_room_between_copied_packets_is_refused(self):
        frames = frames_of((0, 512), (10, 512), (20, 1024))
        with self.assertRaises(ValueError):
            asm.schedule([0, 1, 2], frames, [0, 100, 1], lambda index: index != 1)

    def test_annex_b_exact_pictures_carry_idr_headers(self):
        sps = bytes([0x67, 0x64])
        pps = bytes([0x68, 0x00])
        idr = bytes([0x65, 0x88])
        one = b'\x00\x00\x00\x01' + sps + b'\x00\x00\x00\x01' + pps + b'\x00\x00\x00\x01' + idr
        units = asm.access_units(one + one)
        self.assertEqual(len(units), 2)
        self.assertTrue({7, 8, 5} <= asm.idr_headers(asm.to_avcc(units[0])))

    def test_the_assembly_cannot_be_named_as_the_master(self):
        with self.assertRaises(ValueError):
            asm.refuse_output('hos_008_master_v04.mp4')


if __name__ == '__main__':
    unittest.main()
