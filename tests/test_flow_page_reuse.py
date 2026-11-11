"""Exercise the actual mint caller with the shared tab policy; no CDP or spend."""
import ast
import os
import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / '02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tests.hos009_then import HAS_STUDIO, NEEDS_STUDIO  # noqa: E402

class Page:
    def __init__(self, url, closed=False):
        self.url, self.closed, self.visits = url, closed, []
    def is_closed(self): return self.closed
    def bring_to_front(self): pass
    def goto(self, url, **kwargs):
        self.url = url
        self.visits.append(url)

class Context:
    def __init__(self, pages): self.pages, self.created = pages, 0
    def new_page(self):
        self.created += 1
        page = Page('about:blank')
        self.pages.append(page)
        return page

@unittest.skipUnless(HAS_STUDIO, NEEDS_STUDIO)
class FlowPageTests(unittest.TestCase):
    def choose(self, pages):
        node = next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'flow_page')
        env = {'Path': Path, 'os': os, 'sys': __import__('sys'), 'time': SimpleNamespace(sleep=lambda _: None)}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), env)
        ctx = Context(pages)
        flow = SimpleNamespace(FLOW_HOME='https://flow.google.com/', dismiss_banners=lambda _: None)
        with patch.dict(os.environ, {'OWB_REPO': os.environ.get('OWB_REPO', str(Path.home() / 'YouTube/orbit-with-ben'))}):
            result = env['flow_page'](SimpleNamespace(contexts=[ctx]), flow)
        return result, ctx
    def test_project_reused_without_navigation(self):
        page = Page('https://flow.google.com/project/current')
        chosen, ctx = self.choose([page])
        self.assertIs(chosen, page)
        self.assertEqual((ctx.created, page.visits), (0, []))
    def test_about_reused_and_navigated(self):
        page = Page('https://flow.google.com/about')
        chosen, ctx = self.choose([page])
        self.assertIs(chosen, page)
        self.assertEqual((ctx.created, page.visits), (0, ['https://flow.google.com/']))
    def test_blank_reused(self):
        page = Page('about:blank')
        chosen, ctx = self.choose([Page('https://studio.youtube.com/'), page])
        self.assertIs(chosen, page)
        self.assertEqual(ctx.created, 0)
    def test_closed_page_ignored(self):
        closed = Page('https://flow.google.com/project/old', closed=True)
        chosen, ctx = self.choose([closed])
        self.assertIsNot(chosen, closed)
        self.assertEqual(ctx.created, 1)
    def test_other_site_preserved(self):
        studio = Page('https://studio.youtube.com/')
        chosen, ctx = self.choose([studio])
        self.assertIsNot(chosen, studio)
        self.assertEqual((ctx.created, studio.visits), (1, []))

if __name__ == '__main__': unittest.main()
