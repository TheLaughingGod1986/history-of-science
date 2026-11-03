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
if __name__=='__main__':unittest.main()

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
