"""Offline reproduction: no credentials, account calls, or live desk access."""
import importlib.util
import os
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('fixture_suite', root / 'jobs/reviews/J3150/test_score_flight.py')
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)
desk = suite.Desk()
desk.pause.write_text('fixture pause')
seen = []
class Response:
    status = 200
    headers = {}
    def read(self): return b'{}'
    def __enter__(self): return self
    def __exit__(self, *args): return False

def spy(req, **kwargs):
    seen.append((req.get_method(), req.selector))
    return Response()

try:
    with patch.dict(os.environ, {'HOS_DESK_DIR': str(desk.root), 'EL_GUARD_OFF': '1'}), patch('urllib.request.urlopen', spy):
        assert suite.flight.ACTIVATION_AUTHORIZED is False
        assert desk.pause.is_file()
        class ClientPath(str): pass
        for path in (ClientPath('/v1/music'), ClientPath('/v1/music#fragment')):
            for entry in ('request', 'multipart_post'):
                before = len(seen)
                if entry == 'request':
                    suite.el_client.request('POST', path, 'fixture', 'api_key', data={'prompt': 'fixture lute', 'music_length_ms': 180000, 'model_id': 'music_v2', 'force_instrumental': True})
                else:
                    suite.el_client.multipart_post(path, 'fixture', 'api_key', fields={'prompt': 'fixture lute', 'music_length_ms': '180000', 'model_id': 'music_v2', 'force_instrumental': 'true'}, files=[])
                print(f'{entry} {path!r}: route={suite.el_client._music_route(path)!r}, transport={seen[before:]!r}')
                assert seen[before:] == [('POST', '/v1/music')]
        for query in (ClientPath(''), None):
            before = len(seen)
            suite.el_client.request('POST', '/v1/music', 'fixture', 'api_key', query=query, data={'prompt': 'fixture lute', 'music_length_ms': 180000, 'model_id': 'music_v2', 'force_instrumental': True})
            print(f'request canonical path query type={type(query).__name__}: transport={seen[before:]!r}')
            assert seen[before:] == [('POST', '/v1/music')]
        print('CONFIRMED: six mocked music POSTs bypass the disabled flight; zero real network calls.')
finally:
    suite.el_guard.release_lock()
    suite.el_guard._last.clear()
    desk.close()
