import importlib.util
import pathlib
import unittest
p=pathlib.Path(__file__).resolve().parents[1]/'00_Brand/Channel-Setup/tools/hos_desk.py'
spec=importlib.util.spec_from_file_location('desk',p);desk=importlib.util.module_from_spec(spec);spec.loader.exec_module(desk)
class DeskHandoffs(unittest.TestCase):
    def setUp(self):
        self.state={};self.message={'id':10,'header':{'from':'claude','to':'codex','film':'031','stage':'vo'},'body':'Check voice'}
        self.reply={'id':11,'user':{'login':'owner'},'body':desk.header(**{'from':'codex','to':'claude','film':'031','stage':'vo','status':'review','reply_to':'10'})+'\nRecorded result'}
    def test_seen_message_survives_restart_and_no_new_comments(self):
        desk.pending_messages(self.state,[self.message],'codex')
        import json
        restarted=json.loads(json.dumps(self.state))
        self.assertEqual(desk.pending_messages(restarted,[],'codex'),[self.message])
        self.assertEqual(len(desk.pending_messages(restarted,[self.message],'codex')),1)
    def test_acknowledged_outcome_stops_replay(self):
        desk.pending_messages(self.state,[self.message],'codex')
        desk.acknowledge(self.state,'codex',10,self.reply,'owner')
        self.assertEqual(desk.pending_messages(self.state,[self.message],'codex'),[])
    def test_unrelated_or_untrusted_outcome_cannot_clear_message(self):
        desk.pending_messages(self.state,[self.message],'codex')
        import copy
        for change in ['author','stage','from','reply_to','status','old']:
            reply=copy.deepcopy(self.reply)
            if change=='author':reply['user']['login']='other'
            elif change=='old':reply['id']=9
            else:reply['body']=reply['body'].replace({'stage':'stage=vo','from':'from=codex','reply_to':'reply_to=10','status':'status=review'}[change], {'stage':'stage=edit','from':'from=cursor','reply_to':'reply_to=9','status':'status=task'}[change])
            with self.assertRaises(ValueError):desk.acknowledge(self.state,'codex',10,reply,'owner')
            self.assertIn('10',self.state['pending']['codex'])

class Delivery(unittest.TestCase):
    def test_failed_worker_and_restart_redeliver_until_explicit_outcome(self):
        import tempfile,json,types
        from unittest.mock import patch
        source={'id':10,'user':{'login':'owner'},'body':desk.header(**{'from':'claude','to':'codex','film':'031','stage':'vo','status':'task'})+'\nCheck recording'}
        ns=types.SimpleNamespace(agent='codex',run=True,recover_since_id=None)
        with tempfile.TemporaryDirectory() as root, patch.object(desk,'HOME',pathlib.Path(root)),patch.object(desk,'repo',return_value='owner/repo'),patch.object(desk,'desk_pr',return_value=180),patch.object(desk,'comments',return_value=[source]),patch.object(desk,'run_agent',return_value=2) as worker:
            desk.save_state({'literal_snapshot_v2': True})
            self.assertEqual(desk.check_inbox(ns),1)
            self.assertEqual(desk.check_inbox(ns),1)
            self.assertEqual(worker.call_count,2)
            state=desk.load_state();self.assertEqual(state['last_codex'],10)
            self.assertIn('10',state['pending']['codex'])
            outcome={'id':11,'user':{'login':'owner'},'body':desk.compose('codex','claude','031','vo','review','Checks recorded',[],reply_to='10')}
            desk.acknowledge(state,'codex',10,outcome,'owner');desk.save_state(state)
            self.assertEqual(desk.check_inbox(ns),0)
    def test_corrupt_state_fails_visibly_instead_of_losing_pending_work(self):
        import tempfile,json
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as root,patch.object(desk,'HOME',pathlib.Path(root)):
            (pathlib.Path(root)/'state.json').write_text('{')
            with self.assertRaises(json.JSONDecodeError):desk.load_state()

class TerminalNotifications(unittest.TestCase):
    def test_done_does_not_start_acknowledgement_ping_pong(self):
        state={}
        self.assertEqual(desk.pending_messages(state,[{'id':20,'header':{'status':'done'}}],'codex'),[])


def comment(cid, to, status='task', user='owner'):
    body = desk.header(**{'from': 'claude', 'to': to, 'film': '031', 'stage': 'edit', 'status': status}) + '\nDecide the handoff'
    return {'id': cid, 'user': {'login': user}, 'body': body}


class RoleRouting(unittest.TestCase):
    def test_duplicate_recipients_and_chief_role_match_once(self):
        parsed = desk.parse(desk.header(**{'from': 'claude', 'to': 'codex,codex,chief', 'film': '031', 'stage': 'edit', 'status': 'task'}))
        self.assertEqual(parsed['to'], 'codex,chief')
        state = {'last_role': 0}
        comments = [comment(5, 'codex,codex,chief')]
        self.assertEqual([c['id'] for c in desk.for_agent(comments, 0, 'owner', 'codex', elected='codex', state=state)], [5])
        self.assertEqual(desk.for_agent(comments, 0, 'owner', 'grok', elected='codex', state=state), [])
        self.assertEqual(desk.for_agent(comments, 0, 'owner', 'cursor', elected='cursor', state=state), [])
        named = [comment(6, 'claude,gemini')]
        self.assertEqual([c['id'] for c in desk.for_agent(named, 0, 'owner', 'claude')], [6])
        self.assertEqual([c['id'] for c in desk.for_agent(named, 0, 'owner', 'gemini')], [6])
        self.assertFalse(desk.worker_may_run(parsed, 'cursor'))
        self.assertFalse(desk.worker_may_run(parsed, 'codex'))

    def test_role_seed_does_not_replay_history_and_one_id_can_be_recovered(self):
        state = {}
        old = [comment(3, 'chief'), comment(5, 'chief')]
        self.assertEqual(desk.select_role_messages(old, state, 'codex', 'codex', 'owner'), [])
        self.assertEqual(state['last_role'], 5)
        self.assertEqual([c['id'] for c in desk.select_role_messages(old + [comment(8, 'chief')], state, 'codex', 'codex', 'owner')], [8])
        self.assertEqual(state['last_role'], 8)
        recovered = desk.select_role_messages(old + [comment(8, 'chief')], state, 'codex', 'codex', 'owner', recover_id=3)
        self.assertEqual([c['id'] for c in recovered], [3])
        self.assertEqual(state['last_role'], 8)

    def test_handover_keeps_one_holder_until_handback_and_cursor_cannot_take_it(self):
        state = {'last_role': 0}
        message = comment(5, 'chief')
        first = desk.select_role_messages([message], state, 'codex', 'codex', 'owner')
        desk.pending_messages(state, first, 'codex')
        self.assertEqual(state['assignments']['5']['holder'], 'codex')
        self.assertEqual(desk.select_role_messages([message], state, 'grok', 'grok', 'owner'), [])
        self.assertEqual(desk.for_agent([message], 0, 'owner', 'cursor', elected='codex', state=state), [])
        with self.assertRaises(ValueError):
            desk.handback(state, 'cursor', 5, 'grok')
        desk.handback(state, 'codex', 5, 'grok')
        self.assertNotIn('5', state['pending']['codex'])
        self.assertIn('5', state['pending']['grok'])
        self.assertEqual(state['assignments']['5']['holder'], 'grok')
        reply = {'id': 9, 'user': {'login': 'owner'}, 'body': desk.compose('grok', 'claude', '031', 'edit', 'done', 'Recorded', [], reply_to='5')}
        desk.acknowledge(state, 'grok', 5, reply, 'owner')
        self.assertNotIn('5', state.get('assignments', {}))
        self.assertNotIn('5', state['pending']['grok'])

    def test_upgrade_fence_does_not_auto_run_the_old_backlog(self):
        import tempfile
        import types
        from unittest.mock import patch
        old = {'id': 1, 'header': {'from': 'claude', 'to': 'grok', 'film': '031', 'stage': 'edit', 'status': 'task'}, 'body': 'old'}
        source = {'id': 4, 'user': {'login': 'owner'}, 'body': desk.header(**{'from': 'claude', 'to': 'grok', 'film': '031', 'stage': 'edit', 'status': 'task'}) + '\nnew'}
        ns = types.SimpleNamespace(agent='grok', run=True, recover_since_id=None)
        with tempfile.TemporaryDirectory() as root, patch.object(desk, 'HOME', pathlib.Path(root)), patch.object(desk, 'repo', return_value='owner/repo'), patch.object(desk, 'desk_pr', return_value=180), patch.object(desk, 'comments', return_value=[source]), patch.object(desk, 'run_agent', return_value=0) as worker:
            desk.save_state({'last': 2, 'pending': {'grok': {'1': old}}})
            self.assertEqual(desk.check_inbox(ns), 0)
            self.assertEqual(desk.check_inbox(ns), 0)
        self.assertEqual(worker.call_count, 0)
        ran = [pathlib.Path(call.args[0]).name for call in worker.call_args_list]
        self.assertTrue(all(name.startswith('4_') for name in ran))

    def test_role_delivery_never_starts_the_worker(self):
        import tempfile
        import types
        from unittest.mock import patch
        source = comment(6, 'chief')
        ns = types.SimpleNamespace(agent='codex', elected='codex', run=True, recover_id=None)
        with tempfile.TemporaryDirectory() as root, patch.object(desk, 'HOME', pathlib.Path(root)), patch.object(desk, 'repo', return_value='owner/repo'), patch.object(desk, 'desk_pr', return_value=180), patch.object(desk, 'comments', return_value=[source]), patch.object(desk, 'run_agent') as worker:
            desk.save_state({'last_role': 0})
            self.assertEqual(desk.deliver_role(ns), 1)
            self.assertEqual(desk.deliver_role(ns), 1)
            text = (pathlib.Path(root) / 'inbox' / '6_031_edit.md').read_text()
        worker.assert_not_called()
        self.assertIn('Cursor does not hold Chief authority', text)

    def test_classifies_later_outcome_without_delivery(self):
        self.assertEqual(desk.classify_message(comment(5, 'chief'), [ {'id': 9, 'body': desk.compose('codex', 'claude', '031', 'edit', 'done', 'Done', [], reply_to='5')} ], {}), 'later-outcome')



class CommandRegressions(unittest.TestCase):
    def setUp(self):
        import tempfile, types
        from unittest.mock import patch
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = pathlib.Path(self.tmp.name)
        for name, value in [('HOME', self.home), ('repo', lambda: 'owner/repo'), ('desk_pr', lambda r: 180)]:
            patcher = patch.object(desk, name, value)
            patcher.start(); self.addCleanup(patcher.stop)
        self.ns = types.SimpleNamespace(agent='codex', elected='codex', run=True, recover_id=None, recover_since_id=None)

    def test_upgrade_unseen_literal_all_recipients_and_specific_recovery(self):
        from unittest.mock import patch
        snapshot = [comment(4, 'grok'), comment(5, 'gemini')]
        desk.save_state({'last': 2, 'pending': {}})
        with patch.object(desk, 'comments', return_value=snapshot), patch.object(desk, 'run_agent') as worker:
            self.ns.agent = 'grok'
            self.assertEqual(desk.check_inbox(self.ns), 0)
            self.ns.agent = 'gemini'
            self.assertEqual(desk.check_inbox(self.ns), 0)
            worker.assert_not_called()
            state = desk.load_state()
            self.assertEqual(state['last'], 5)
            self.assertEqual(state['last_gemini'], 5)
            self.ns.recover_id = 5
            self.assertEqual(desk.check_inbox(self.ns), 1)
            self.assertEqual(desk.load_state()['last_gemini'], 5)
            self.assertEqual(worker.call_count, 1)
            self.ns.recover_since_id = 0
            with self.assertRaises(ValueError): desk.check_inbox(self.ns)

    def test_new_literal_after_snapshot_still_runs(self):
        from unittest.mock import patch
        with patch.object(desk, 'comments', return_value=[]):
            self.assertEqual(desk.check_inbox(self.ns), 0)
        with patch.object(desk, 'comments', return_value=[comment(6, 'codex,codex')]), patch.object(desk, 'run_agent', return_value=0) as worker:
            self.assertEqual(desk.check_inbox(self.ns), 1)
            worker.assert_called_once()

    def test_role_restart_handback_first_poll_and_trusted_ack(self):
        import json
        from unittest.mock import patch
        desk.save_state({'last_role': 0})
        with patch.object(desk, 'comments', return_value=[comment(4, 'chief,codex,chief')]), patch.object(desk, 'run_agent') as worker:
            self.assertEqual(desk.deliver_role(self.ns), 1)
            desk.save_state(json.loads(json.dumps(desk.load_state())))
            self.assertEqual(desk.deliver_role(self.ns), 1)
            self.ns.agent = self.ns.elected = 'grok'
            self.assertEqual(desk.deliver_role(self.ns), 0)  # held by Codex until explicit handback
            desk.cmd_handback(type('NS', (), {'agent':'codex', 'id':4, 'to':'grok'})())
            self.assertEqual(desk.check_inbox(self.ns), 0)  # first literal poll cannot swallow role mail
            self.assertEqual(desk.deliver_role(self.ns), 1)
            reply = {'id':9, 'user':{'login':'intruder'}, 'body':desk.compose('grok','claude','031','edit','done','Resolved',[],reply_to='4')}
            with patch.object(desk, 'comments', return_value=[reply]):
                with self.assertRaises(ValueError): desk.cmd_ack(type('NS', (), {'agent':'grok','id':4,'ref':9})())
            reply['user']['login'] = 'owner'
            with patch.object(desk, 'comments', return_value=[reply]):
                desk.cmd_ack(type('NS', (), {'agent':'grok','id':4,'ref':9})())
            self.assertEqual(desk.deliver_role(self.ns), 0)
            self.ns.agent = self.ns.elected = 'cursor'
            self.assertEqual(desk.deliver_role(self.ns), 0)
            worker.assert_not_called()

    def refresh(self, *, ps='100 1\n', fail_print=False, change_pid=False, confirm=True):
        import types
        from unittest.mock import patch
        self.calls = []
        self.restarted = False
        def run(args, **kwargs):
            self.calls.append(args)
            if args[:2] == ['launchctl', 'print']:
                if fail_print: raise desk.subprocess.CalledProcessError(1, args)
                pid = 101 if self.restarted or (change_pid and sum(c[:2] == ['launchctl','print'] for c in self.calls) > 1) else 100
                return types.SimpleNamespace(stdout=f'pid = {pid}\n')
            if args[0] == 'ps': return types.SimpleNamespace(stdout=ps)
            if args[:2] == ['launchctl', 'kickstart']:
                self.restarted = True
                if confirm:
                    (self.home/'loaded.json').write_text(desk.json.dumps({'pid':101,'code':desk.CODE,'sha256':desk.LOADED_SHA256}))
                return types.SimpleNamespace(stdout='')
            self.fail(f'Unexpected OS call {args}')
        with patch.dict(desk.os.environ, {'HOS_DESK_INSTALLED':str(p)}), patch.object(desk.subprocess, 'run', side_effect=run), patch.object(desk.time, 'sleep'):
            desk.cmd_refresh(types.SimpleNamespace(apply=True))

    def test_watch_start_records_actual_loaded_pid_and_hash(self):
        import types
        from unittest.mock import patch
        ns = types.SimpleNamespace(watch=120, agent='grok')
        with patch.object(desk, 'check_inbox'), patch.object(desk, 'resolve_elected', return_value=None), patch.object(desk.time, 'sleep', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt): desk.cmd_inbox(ns)
        loaded = desk.json.loads((self.home/'loaded.json').read_text())
        self.assertEqual(loaded, {'pid':desk.os.getpid(), 'code':desk.CODE, 'sha256':desk.LOADED_SHA256})

    def test_refresh_rejects_changed_installed_source_before_os_calls(self):
        import types
        from unittest.mock import patch
        wrong = self.home/'wrong.py'
        wrong.write_text(desk.CODE)  # a matching marker is insufficient
        with patch.dict(desk.os.environ, {'HOS_DESK_INSTALLED':str(wrong)}), patch.object(desk.subprocess,'run') as run:
            with self.assertRaises(SystemExit): desk.cmd_refresh(types.SimpleNamespace(apply=True))
            run.assert_not_called()

    def test_refresh_proves_pid_hash_and_holds_all_locks(self):
        from unittest.mock import patch
        original = desk.inspect_idle
        def inspect(target):
            for agent in desk.WRITERS:
                with (self.home/f'dispatch-{agent}.lock').open('a') as lock:
                    with self.assertRaises(BlockingIOError): desk.fcntl.flock(lock, desk.fcntl.LOCK_EX | desk.fcntl.LOCK_NB)
            return original(target)
        with patch.object(desk, 'inspect_idle', side_effect=inspect): self.refresh()
        result = desk.json.loads((self.home/'refresh-result.json').read_text())
        self.assertEqual((result['old_pid'], result['pid'], result['sha256']), (100,101,desk.LOADED_SHA256))

    def test_refresh_refuses_descendants_unknown_process_lease_and_race(self):
        for kwargs in [{'ps':'100 1\n200 100\n300 200\n'}, {'ps':'bad'}, {'ps':''}, {'fail_print':True}, {'change_pid':True}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(SystemExit): self.refresh(**kwargs)
            self.assertFalse(self.restarted)
        (self.home/'execution.json').write_text('{')
        with self.assertRaises(SystemExit): self.refresh()
        (self.home/'execution.json').write_text('{"pid":100}')
        with self.assertRaises(SystemExit): self.refresh()
        self.assertFalse(self.restarted)

    def test_refresh_refuses_busy_dispatch_and_unconfirmed_version(self):
        with (self.home/'dispatch-grok.lock').open('a') as lock:
            desk.fcntl.flock(lock, desk.fcntl.LOCK_EX | desk.fcntl.LOCK_NB)
            with self.assertRaises(SystemExit): self.refresh()
            self.assertEqual(self.calls, [])
        with self.assertRaises(SystemExit): self.refresh(confirm=False)
        self.assertTrue(self.restarted)
        self.assertFalse((self.home/'refresh-result.json').exists())


if __name__ == '__main__':
    unittest.main()

class StaleChiefReplies(unittest.TestCase):
    def message(self, sender='codex', reply_to='10', supersedes=''):
        return desk.parse(desk.compose(sender, 'claude', '031', 'edit', 'review',
                                       'Outcome', [], reply_to, supersedes))

    def post(self, cid, sender='grok', film='031', stage='edit', user='owner'):
        return {'id': cid, 'user': {'login': user},
                'body': desk.compose(sender, 'claude', film, stage, 'done', 'Decision', [])}

    def test_each_chief_sender_refuses_newer_chief_post(self):
        for sender in desk.CHIEF_DESK_IDS:
            with self.subTest(sender=sender), self.assertRaisesRegex(ValueError, '--supersedes 20'):
                desk.refuse_stale_reply(self.message(sender), [self.post(20)], 'owner')

    def test_override_must_name_newest_even_when_snapshot_is_unsorted(self):
        snapshot = [self.post(30, 'gemini'), self.post(20, 'claude')]
        for supersedes in ('', '20', '31'):
            with self.subTest(supersedes=supersedes), self.assertRaises(ValueError):
                desk.refuse_stale_reply(self.message(supersedes=supersedes), snapshot, 'owner')
        message = self.message(supersedes='30')
        self.assertEqual(message['supersedes'], '30')
        desk.refuse_stale_reply(message, snapshot, 'owner')

    def test_cursor_no_reply_and_unrelated_posts_are_unchanged(self):
        desk.refuse_stale_reply(self.message('cursor'), [self.post(20)], 'owner')
        desk.refuse_stale_reply(self.message(reply_to=''), [self.post(20)], 'owner')
        snapshot = [self.post(10), self.post(9), self.post(20, 'cursor'),
                    self.post(21, film='032'), self.post(22, stage='vo'),
                    self.post(23, user='intruder')]
        desk.refuse_stale_reply(self.message(), snapshot, 'owner')

    def test_cmd_post_refuses_before_images_or_comment_side_effects(self):
        import types
        from unittest.mock import patch
        ns = types.SimpleNamespace(frm='codex', to='claude', film='031', stage='edit',
                                   status='review', body='Outcome', body_file=None,
                                   image=['unused.jpg'], reply_to=10, supersedes=None)
        with patch.object(desk, 'repo', return_value='owner/repo'), \
                patch.object(desk, 'desk_pr', return_value=180), \
                patch.object(desk, 'comments', return_value=[self.post(20)]), \
                patch.object(desk, 'push_images') as images, patch.object(desk, 'sh') as shell:
            with self.assertRaisesRegex(SystemExit, 'Stale desk reply'):
                desk.cmd_post(ns)
            images.assert_not_called()
            shell.assert_not_called()
