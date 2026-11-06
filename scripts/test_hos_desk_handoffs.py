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
            self.assertEqual(desk.check_inbox(ns), 2)
            self.assertEqual(desk.check_inbox(ns), 2)
        self.assertEqual(worker.call_count, 2)
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
            self.assertEqual(desk.deliver_role(ns), 0)
            text = (pathlib.Path(root) / 'inbox' / '6_031_edit.md').read_text()
        worker.assert_not_called()
        self.assertIn('Cursor does not hold Chief authority', text)

    def test_refresh_waits_for_idle_installed_code(self):
        self.assertEqual(desk.refresh_decision(children=1, code_installed=True), 'wait')
        self.assertEqual(desk.refresh_decision(children=0, code_installed=False), 'refuse')
        self.assertEqual(desk.refresh_decision(children=0, code_installed=True), 'refresh')
        self.assertEqual(desk.classify_message(comment(5, 'chief'), [ {'id': 9, 'body': desk.compose('codex', 'claude', '031', 'edit', 'done', 'Done', [], reply_to='5')} ], {}), 'later-outcome')


if __name__ == '__main__':
    unittest.main()
