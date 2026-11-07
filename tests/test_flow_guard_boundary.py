"""Production helper functions exercised with fake browser/IO; never submit Flow."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / '04_Audio/tools/orbit_flow_veo_ui.py'


def functions():
    names = {'submit_create', '_generate_clip_once', 'generate_clip', 'wait_and_download_passive'}
    tree = ast.parse(SOURCE.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    env = dict(Path=Path, DEFAULT_MODEL='Veo 3.1 - Quality', FLOW_HOME='https://flow.google.com/',
               time=SimpleNamespace(time=lambda: 0, monotonic=lambda: 0), os=__import__('os'))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), 'exec'), env)
    return env


class BoundaryTests(unittest.TestCase):
    def test_guard_is_only_create_action_after_mode_preparation(self):
        env = functions(); events = []
        page = Mock()
        env['_dismiss_asset_search_modal'] = lambda p: events.append('dismiss')
        env['_ensure_create_prompt_mode'] = lambda p: events.append('mode')
        def refuse(p):
            events.append('guard'); raise RuntimeError('price drift')
        with self.assertRaisesRegex(RuntimeError, 'price drift'):
            env['submit_create'](page, create_guard=refuse)
        self.assertEqual(events, ['dismiss', 'mode', 'guard'])
        page.evaluate.assert_not_called(); page.mouse.click.assert_not_called()

    def prepared(self, root, guard):
        env = functions(); events = []
        page = Mock(url='https://flow.google.com/project/test')
        page._orbit_flow_project_url = page.url
        frame = root/'frame.png'; frame.write_bytes(b'fake fixture')
        for name in ('ensure_agent_session','settle_after_nav','dismiss_banners'):
            env[name] = Mock()
        env['looks_logged_in'] = lambda p: True
        env['assert_veo3_model'] = lambda m: m
        env['collect_media_ids'] = lambda p: set()
        env['configure_veo_settings'] = lambda *a, **kw: events.append('settings')
        env['attach_image_to_prompt'] = lambda *a: True
        env['_start_frame_present'] = lambda p: True
        env['set_prompt'] = lambda *a: events.append('prompt')
        env['flow_prompt'] = lambda p, **kw: p
        env['_dismiss_asset_search_modal'] = lambda p: None
        env['_ensure_create_prompt_mode'] = lambda p: events.append('mode')
        env['_record_flow_spend'] = Mock(side_effect=AssertionError('legacy accounting bypass'))
        env['confirm_generation_spend'] = Mock(side_effect=AssertionError('unguarded confirmation'))
        env['wait_and_download'] = Mock(side_effect=AssertionError('legacy retry loop'))
        def download(p, dest, **kwargs):
            dest.write_bytes(b'fake output fixture')
            return 'fake-media'
        env['wait_and_download_passive'] = Mock(side_effect=download)
        env['veo'] = SimpleNamespace(already_done=lambda p: True, strip_audio=Mock())
        return env, page, frame, events

    def test_full_generation_configures_then_guards_then_passively_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); env,page,frame,events=self.prepared(root, None)
            def guard(p): events.append('guard')
            result=env['generate_clip'](page,'locked prompt',root/'out.mp4',
                start_frame=frame,reuse_project=True,attempts=1,create_guard=guard)
            self.assertEqual(events, ['settings','prompt','mode','guard'])
            self.assertEqual(result['media_id'],'fake-media')
            env['wait_and_download_passive'].assert_called_once()
            env['confirm_generation_spend'].assert_not_called()
            env['_record_flow_spend'].assert_not_called()
            page.mouse.click.assert_not_called()

    def test_failure_at_actual_guard_never_downloads_recovers_or_retries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); env,page,frame,events=self.prepared(root, None)
            env['recover_flow_home']=Mock(side_effect=AssertionError('retry'))
            env['is_transient_ui_error']=lambda e: True
            def guard(p):
                events.append('guard'); raise RuntimeError('changed exact price')
            with self.assertRaisesRegex(RuntimeError, 'changed exact price'):
                env['generate_clip'](page,'prompt',root/'out.mp4',start_frame=frame,
                    reuse_project=True,attempts=1,create_guard=guard)
            self.assertEqual(events.count('guard'),1)
            env['wait_and_download_passive'].assert_not_called()
            env['recover_flow_home'].assert_not_called()

    def test_guarded_retry_configuration_refused_before_any_page_action(self):
        env=functions(); page=Mock()
        for attempts in (0,2,3):
            with self.assertRaises(ValueError):
                env['generate_clip'](page,'p',Path('out'),attempts=attempts,create_guard=Mock())
        self.assertEqual(page.mock_calls, [])

    def test_guarded_missing_frame_never_uses_context_animate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); env,page,frame,events=self.prepared(root,None)
            env['attach_image_to_prompt']=lambda *a: False
            env['_start_frame_present']=lambda p: False
            env['try_context_animate']=Mock(side_effect=AssertionError('unguarded Animate'))
            with self.assertRaisesRegex(RuntimeError,'Guarded start frame missing'):
                env['generate_clip'](page,'p',root/'out.mp4',start_frame=frame,
                    reuse_project=True,attempts=1,create_guard=Mock())
            env['try_context_animate'].assert_not_called()

    def test_passive_download_is_exclusive_and_never_clicks(self):
        env=functions(); page=Mock()
        env['collect_media_ids']=lambda p: {'old','new'}
        env['absolute_media_url']=lambda mid: mid
        payload=b'\0\0\0\x18ftyp'+b'x'*200000
        page.request.get.return_value=SimpleNamespace(ok=True,headers={'content-type':'video/mp4'},body=lambda:payload)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out.mp4'
            self.assertEqual(env['wait_and_download_passive'](page,out,before_ids={'old'},timeout_s=1),'new')
            self.assertEqual(out.read_bytes(),payload)
            with self.assertRaises(FileExistsError):
                env['wait_and_download_passive'](page,out,before_ids={'old'},timeout_s=1)
            page.evaluate.assert_not_called();page.mouse.click.assert_not_called()

    def test_actual_account_guard_rejects_settings_drift_at_helper_boundary(self):
        from tests.test_hos009_tranche2_runner import RUNNER, LiveCreateAdapterTests
        for field, value in [('outputs', ['x4']), ('prices', ['Generating will use 200 credits']),
                             ('accounts', [RUNNER.FORBIDDEN_ACCOUNT]), ('ultra', False)]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); env,page,frame,events=self.prepared(root,None)
                fixture=LiveCreateAdapterTests.Page(LiveCreateAdapterTests().evidence())
                page.evaluate=fixture.evaluate
                # Drift occurs during configuration, after any earlier batch check.
                env['configure_veo_settings']=lambda *a, **kw: fixture.evidence.update({field:value})
                with RUNNER.SharedFlowAccounting(root/'state') as account:
                    account.reserve('job','HOS:009',6000,live=10000)
                    guard=lambda p: RUNNER.guarded_create(p,account,reservation='job',
                        charge='take',evidence_path=root/'evidence.json')
                    with self.assertRaises(RUNNER.GuardError):
                        env['generate_clip'](page,'p',root/'out.mp4',start_frame=frame,
                            reuse_project=True,attempts=1,create_guard=guard)
                    self.assertEqual(fixture.clicks,0)
                    self.assertFalse(account.snapshot()['charges'])
                    env['wait_and_download_passive'].assert_not_called()

    def test_actual_account_guard_is_only_click_with_durable_intent(self):
        from tests.test_hos009_tranche2_runner import RUNNER, LiveCreateAdapterTests
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); env,page,frame,events=self.prepared(root,None)
            with RUNNER.SharedFlowAccounting(root/'state') as account:
                account.reserve('job','HOS:009',6000,live=10000)
                def before_click():
                    self.assertTrue(account.snapshot()['pending'])
                    self.assertTrue((root/'evidence.json').exists())
                fixture=LiveCreateAdapterTests.Page(LiveCreateAdapterTests().evidence(),before_click)
                page.evaluate=fixture.evaluate
                env['generate_clip'](page,'p',root/'out.mp4',start_frame=frame,
                    reuse_project=True,attempts=1,create_guard=lambda p: RUNNER.guarded_create(
                        p,account,reservation='job',charge='take',evidence_path=root/'evidence.json'))
                self.assertEqual(fixture.clicks,1)
                self.assertEqual(account.snapshot()['charges']['take']['status'],'CHARGED')
                env['confirm_generation_spend'].assert_not_called()
                env['_record_flow_spend'].assert_not_called()

    def test_real_live_submit_adapter_and_helper_share_reservation_at_click(self):
        import os
        import sys
        from types import ModuleType
        from unittest.mock import MagicMock, patch
        from tests.test_hos009_tranche2_runner import RUNNER, ROOT, LiveCreateAdapterTests
        for live, drift in [(10000,False),(8900,False),(10000,True)]:
            with self.subTest(live=live,drift=drift), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); env,page,frame,events=self.prepared(root,None)
                # The real adapter starts a project; keep this fixture on its
                # existing fake project without touching any browser process.
                env['ensure_project']=lambda p: page.url
                fixture=LiveCreateAdapterTests.Page(LiveCreateAdapterTests().evidence())
                fixture.evidence['balances']=[live]
                if drift: fixture.evidence['outputs']=['x4']
                page.evaluate=fixture.evaluate
                fake_flow=ModuleType('orbit_flow_veo_ui')
                fake_flow.FLOW_HOME='https://flow.google.com/'
                fake_flow.generate_clip=env['generate_clip']
                fake_api=ModuleType('playwright.sync_api')
                context=MagicMock()
                context.__enter__.return_value.chromium.connect_over_cdp.return_value=Mock()
                fake_api.sync_playwright=lambda: context
                with RUNNER.SharedFlowAccounting(root/'state') as account, \
                     patch.dict(os.environ,{RUNNER.SUBMIT_ENV:'1'}), \
                     patch.dict(sys.modules,{'orbit_flow_veo_ui':fake_flow,'playwright.sync_api':fake_api}), \
                     patch.object(RUNNER,'open_flow_page',return_value=page):
                    row=RUNNER.order_rows(RUNNER.load_scope(ROOT))[0]
                    def submit():
                        return RUNNER.live_video_submit(row,root/'out.mp4',frame,accounting=account,
                            reservation='J2033',charge='fake-take',evidence_path=root/'create.json')
                    if live<9000 or drift:
                        with self.assertRaises(RUNNER.GuardError): submit()
                        self.assertEqual(fixture.clicks,0)
                        self.assertFalse(account.snapshot()['charges'])
                        env['wait_and_download_passive'].assert_not_called()
                    else:
                        evidence=submit()
                        self.assertEqual(evidence['charge'],'fake-take')
                        self.assertEqual(fixture.clicks,1)
                        self.assertEqual(account.snapshot()['reservations']['J2033']['cap'],6000)
                        self.assertEqual(account.snapshot()['liability'],6000)
                        env['wait_and_download_passive'].assert_called_once()
                    env['confirm_generation_spend'].assert_not_called()
                    env['_record_flow_spend'].assert_not_called()


if __name__=='__main__': unittest.main()
