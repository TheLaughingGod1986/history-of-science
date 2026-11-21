"""Offline findings against the exact J3150 checkout passed as argv[1].

Expected output describes defects, not acceptance tests. No live transport.
"""
import importlib.util
import os
import sys
import urllib.request
from pathlib import Path
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('fixture3150', root / 'jobs/reviews/J3150/test_score_flight.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
flight = fixture.flight

# Network is denied globally except where replaced by a synthetic response.
def denied(*args, **kwargs):
    raise AssertionError('Real transport forbidden')

with patch.object(urllib.request, 'urlopen', side_effect=denied):
    desk = fixture.Desk()
    calls = []
    def failed_get(method, body):
        calls.append(method)
        raise OSError('synthetic connection failure')
    with patch.object(flight, '_read_one_response', side_effect=failed_get):
        for _ in range(2):
            try:
                flight.from_generator(prompt=fixture.PROMPT, length_ms=180000)
            except OSError:
                pass
    print('Repeated failed read:', calls, 'store exists:', desk.store.exists())
    assert calls == ['GET', 'GET'] and not desk.store.exists()
    desk.close()

    class Response:
        status = 200
        headers = {}
        def read(self): return b'fixture'
        def __enter__(self): return self
        def __exit__(self, *args): pass

    # Do not mock before_spend: demonstrate the real old bypass switch.
    desk = fixture.Desk()
    with patch.dict(os.environ, {'HOS_DESK_DIR': str(desk.root), 'EL_GUARD_OFF': '1'}):
        (desk.root / 'elevenlabs' / 'TTS_PAUSE').write_text('paused')
        for entry in ('request', 'multipart_post'):
            calls = []
            def exchange(req, **kwargs):
                calls.append((req.get_method(), req.selector))
                return Response()
            with patch.object(urllib.request, 'urlopen', side_effect=exchange):
                if entry == 'request':
                    fixture.el_client.request('POST', '/v1/music#fragment', 'fixture', 'api_key', data={})
                else:
                    fixture.el_client.multipart_post('/v1/music#fragment', 'fixture', 'api_key', fields={}, files=[])
            print(entry, 'activation:', flight.ACTIVATION_AUTHORIZED, 'pause exists:', desk.pause.exists(), 'wire:', calls)
            assert flight.ACTIVATION_AUTHORIZED is False
            assert calls == [('POST', '/v1/music')]
    desk.close()
