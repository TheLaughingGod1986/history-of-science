"""Independent offline reservation ordering and process-restart checks."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('fixtures', root / 'jobs/reviews/J3150/test_score_flight.py')
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
flight = fixtures.flight

for scenario in ('failed_transport', 'untrusted_receipt', 'restart_before_transport'):
    desk = fixtures.Desk()
    reservation = desk.root / 'elevenlabs' / flight.READ_ONCE_NAME
    calls = []
    def mocked(method, body):
        assert reservation.is_file(), 'transport entered before reservation'
        record = json.loads(reservation.read_bytes())
        assert record['recorder_ino'] == os.fstat(flight.guard._held_fd).st_ino
        assert method == 'GET', 'unexpected POST'
        calls.append(method)
        if scenario == 'failed_transport':
            raise OSError('fixture failure')
        return 200, None, b''
    try:
        with patch.object(flight, '_read_one_response', mocked):
            if scenario == 'restart_before_transport':
                flight.guard.hold_recorder()
                flight._reserve_one_read(flight.guard._held_fd, flight.guard._held_ino, flight.guard._held_started)
            else:
                try:
                    flight.from_generator(prompt='fixture lute', length_ms=180000)
                except (OSError, flight.guard.GuardRefused):
                    pass
                else:
                    raise AssertionError('failure fixture did not refuse')
            kept = reservation.read_bytes()
            assert not desk.store.exists()
            # End the holder, then restart in an independent interpreter.
            flight.guard.release_test_holder()
            child = '''import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import hos009_score_flight as f
f.guard.bind_desk(Path(sys.argv[2]))
def forbidden(*args):
    raise AssertionError('restart reached transport')
f._read_one_response = forbidden
try:
    f.from_generator(prompt='fixture lute', length_ms=180000)
except f.guard.GuardRefused as error:
    assert error.code == 'read_reserved', error.code
    print('read_reserved; zero transport calls')
else:
    raise AssertionError('restart did not refuse')
'''
            result = subprocess.run([sys.executable, '-c', child, str(fixtures.TOOLS), str(desk.root)], capture_output=True, text=True, check=True)
            assert reservation.read_bytes() == kept
            assert not desk.store.exists()
            assert calls == ([] if scenario == 'restart_before_transport' else ['GET'])
            print(f'{scenario}: initial calls={calls!r}; {result.stdout.strip()}; reservation unchanged; pinned store absent')
    finally:
        desk.close()
print('All three reservation scenarios confirmed offline; no live store touched.')
