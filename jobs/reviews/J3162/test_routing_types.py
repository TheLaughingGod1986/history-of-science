"""Offline transport-boundary regressions; fixture desk and tokens only."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('flight_fixture', ROOT / 'jobs/reviews/J3150/test_score_flight.py')
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class ClientString(str):
    pass


class RoutingTypes(unittest.TestCase):
    def setUp(self):
        self.desk = suite.Desk()
        self.addCleanup(self.desk.close)
        self.desk.pause.write_text('fixture pause')
        self.assertIs(suite.flight.ACTIVATION_AUTHORIZED, False)

    def refuse(self, entry, path, *, guard_off=True, **kwargs):
        env = {'HOS_DESK_DIR': str(self.desk.root)}
        if guard_off:
            env['EL_GUARD_OFF'] = '1'
        with patch.dict(os.environ, env), patch('urllib.request.urlopen') as transport, patch.object(suite.el_guard, 'before_spend') as legacy:
            if not guard_off:
                os.environ.pop('EL_GUARD_OFF', None)
            with self.assertRaises(suite.flight.guard.GuardRefused) as caught:
                if entry == 'request':
                    suite.el_client.request('POST', path, 'fixture', 'api_key', data={}, **kwargs)
                else:
                    suite.el_client.multipart_post(path, 'fixture', 'api_key', fields={}, files=[])
            self.assertEqual(caught.exception.code, 'malformed_request')
            transport.assert_not_called()
            legacy.assert_not_called()
        self.assertTrue(self.desk.pause.is_file())
        self.assertFalse(self.desk.store.exists())

    def test_path_types_both_entries(self):
        paths = [ClientString('/v1/music'), ClientString('/v1/music#fragment'), b'/v1/music', b'/v1/music#fragment', None, 1, [], {}]
        for entry in ('request', 'multipart_post'):
            for path in paths:
                with self.subTest(entry=entry, path=repr(path)):
                    self.refuse(entry, path)

    def test_query_types_request(self):
        queries = [None, ClientString(''), ClientString('output_format=mp3_44100_128'), b'', b'output_format=mp3_44100_128', 0, False, [], {}]
        for path in ('/v1/music', '/v1/music#fragment'):
            for query in queries:
                with self.subTest(path=path, query=repr(query)):
                    self.refuse('request', path, query=query)

    def test_obfuscated_music_paths_make_no_post(self):
        paths = (
            '/v1/%6dusic',
            '/v1//music',
            '/v1/./music',
            '/V1/MUSIC',
            '/v1\\music',
            '/v1/x/../music',
            ' /v1/music',
        )
        for guard_off in (True, False):
            for entry in ('request', 'multipart_post'):
                for path in paths:
                    with self.subTest(entry=entry, path=path, guard_off=guard_off):
                        self.refuse(entry, path, guard_off=guard_off)
        self.refuse('request', '/V1/MUSIC', query='output_format=mp3_44100_128')

    def test_clean_paths_stay_classified(self):
        route = suite.el_client._music_route
        self.assertEqual(route('/v1/music'), 'flight')
        self.assertEqual(route('/v1/music', 'output_format=mp3_44100_128'), 'flight')
        for path in (
            '/v1/text-to-speech/voice',
            '/v1/speech-to-text',
            '/v1/sound-generation',
            '/v1/user/subscription',
        ):
            with self.subTest(path=path):
                self.assertEqual(route(path), 'other')
        for path in ('/v1/%6dusic', '/v1//music', '/v1/./music', '/V1/MUSIC', '/v1\\music', '/v1/x/../music', ' /v1/music', 'v1/music'):
            with self.subTest(path=path):
                self.assertEqual(route(path), 'reject')


if __name__ == '__main__':
    unittest.main()
