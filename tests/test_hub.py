"""The hub window driven like a user: the three lists, the search, the
detail panel, paths. Nothing is sent anywhere, settings live in a temp
folder, the window is never topmost."""
import io
import json
import os
import shutil
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import data  # noqa: E402
import foxfeedback  # noqa: E402
import foxfeedback_ui  # noqa: E402
import guidebook  # noqa: E402
import modding_hub as M  # noqa: E402


class Data(unittest.TestCase):
    def test_entries_are_complete(self):
        ids = [t['id'] for t in data.TOOLS]
        self.assertEqual(len(ids), len(set(ids)), 'tool ids are unique')
        for t in data.TOOLS:
            for key in ('name', 'desc_en', 'desc_de', 'type'):
                self.assertTrue(t.get(key), f'{t["id"]}: {key}')
            self.assertIn(t['type'], ('exe', 'python'))
            if t['type'] == 'exe':
                self.assertTrue(t.get('filename', '').lower().endswith('.exe'), t['id'])
        for g in data.GUIDES:
            for key in ('title_en', 'title_de'):
                self.assertTrue(g.get(key), f'{g["id"]}: {key}')
        for ext, entry in data.FORMATS.items():
            self.assertTrue(ext.startswith('.'), ext)
            self.assertTrue(entry.get('en') and entry.get('de'), ext)

    def test_guide_files_are_there(self):
        folder = os.path.join(ROOT, 'guides')
        for g in data.GUIDES:
            for key in ('file_en', 'file_de'):
                name = g.get(key)
                if name:
                    self.assertTrue(os.path.isfile(os.path.join(folder, name)),
                                    f'{g["id"]}: {name} missing in guides/')

    def test_guide_ids_point_at_tools(self):
        ids = {t['id'] for t in data.TOOLS}
        for g in data.GUIDES:
            for tid in g.get('tool_ids') or []:
                self.assertIn(tid, ids, f'{g["id"]} -> {tid}')

    def test_texts_and_chapters(self):
        M._check_translations()
        self.assertEqual(len(guidebook.CHAPTERS), 6)


class Window(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='hub_ui_')
        cls._orig = (M.data_dir, foxfeedback.submit, foxfeedback_ui.FeedbackUI.start,
                     M.webbrowser.open, M.subprocess.Popen, M.filedialog.askopenfilename)
        data_folder = os.path.join(cls.tmp, 'data')
        os.makedirs(data_folder)
        M.data_dir = lambda: data_folder
        cls.opened, cls.started = [], []
        foxfeedback.submit = lambda *a, **k: (_ for _ in ()).throw(AssertionError('nothing is sent'))
        foxfeedback_ui.FeedbackUI.start = lambda self: None
        M.webbrowser.open = lambda url: cls.opened.append(url)
        M.subprocess.Popen = lambda *a, **k: cls.started.append(a) or None
        cfg = M.Config()
        cfg.update(guide_seen=True, update_check=False, lang='en')
        cfg.save()
        cls.app = M.App()
        cls.app.root.geometry('1020x660+40+40')
        cls.app.root.lower()
        cls.pump(0.4)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.root.destroy()
        except Exception:
            pass
        (M.data_dir, foxfeedback.submit, foxfeedback_ui.FeedbackUI.start, M.webbrowser.open,
         M.subprocess.Popen, M.filedialog.askopenfilename) = cls._orig
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def pump(cls, secs=0.15):
        end = time.time() + secs
        while time.time() < end:
            cls.app.root.update()
            time.sleep(0.01)

    def setUp(self):
        self.opened.clear()
        self.started.clear()
        self.app.search_var.set('')
        self.app.set_tab('tools')
        self.pump()

    def test_three_lists_hold_what_data_says(self):
        self.assertEqual(len(self.app.rows), len(data.TOOLS))
        self.app.set_tab('guides')
        self.pump()
        self.assertEqual(len(self.app.rows), len(data.GUIDES))
        self.app.set_tab('formats')
        self.pump()
        self.assertEqual(len(self.app.rows), len(data.FORMATS))

    def test_search_filters_the_open_list(self):
        self.app.search_var.set('.wd')
        self.pump()
        self.assertTrue(0 < len(self.app.rows) < len(data.TOOLS))
        for t in self.app.rows:
            self.assertIn('.wd', ' '.join((t.get('formats') or []) + [t['name'].lower(),
                                                                      M.loc(t, 'desc').lower()]))
        self.app.search_var.set('zzzz-nothing')
        self.pump()
        self.assertEqual(self.app.rows, [])
        self.assertIn('Nothing matches', self.app.status_lbl.cget('text'))

    def test_detail_panel_follows_the_selection(self):
        self.app.set_tab('formats')
        self.app.search_var.set('.par')
        self.pump()
        self.assertTrue(self.app.rows)
        self.assertEqual(self.app.title_lbl.cget('text'), '.par')
        self.assertIn('PAR', self.app.desc_lbl.cget('text'))

    def select(self, name):
        """Pick the row whose title starts with ``name``."""
        for i, item in enumerate(self.app.rows):
            title = item['name'] if isinstance(item, dict) and 'name' in item else (
                M.loc(item, 'title') if isinstance(item, dict) else item[0])
            if title.startswith(name):
                row = self.app.tree.get_children()[i]
                self.app.tree.selection_set(row)
                self.pump()
                return item
        self.fail(f'no row for {name}')

    def test_a_missing_tool_offers_the_download(self):
        self.app.search_var.set('WhizzEdit')
        self.pump()
        self.select('WhizzEdit')
        self.assertFalse(self.app.btn_main.winfo_ismapped(), 'no Start without the program')
        self.assertTrue(self.app.btn_dl.winfo_ismapped())
        self.app.download()
        self.assertEqual(len(self.opened), 1)

    def test_pointing_at_a_file_is_remembered_and_can_be_undone(self):
        fake = os.path.join(self.tmp, 'WhizzEdit.exe')
        with open(fake, 'wb') as f:
            f.write(b'MZ')
        M.filedialog.askopenfilename = lambda *a, **k: fake
        self.app.search_var.set('WhizzEdit')
        self.pump()
        self.select('WhizzEdit')
        self.app.pick_file()
        self.pump()
        self.assertEqual(self.app.cfg['tool_paths']['whizzedit'], os.path.normpath(fake))
        self.assertTrue(self.app.btn_main.winfo_ismapped(), 'Start appears')
        self.app.primary()
        self.assertEqual(len(self.started), 1)
        self.app.pick_file()                       # the button now forgets the path
        self.pump()
        self.assertNotIn('whizzedit', self.app.cfg.get('tool_paths') or {})

    def test_a_guide_shows_its_text(self):
        self.app.set_tab('guides')
        self.app.search_var.set('Editor Beginner')
        self.pump()
        self.select('Editor Beginner')
        shown = self.app.text.get('1.0', 'end')
        self.assertGreater(len(shown), 2000)
        self.assertIn('EDITOR', shown.upper())

    def test_hiding_the_tools_without_a_download(self):
        self.app.missing_var.set(False)
        self.app._toggle_missing()
        self.pump()
        self.assertTrue(all(M.tool_path(self.app.cfg, t) for t in self.app.rows))
        self.app.missing_var.set(True)
        self.app._toggle_missing()
        self.pump()

    def test_selftest_line(self):
        out = os.path.join(self.tmp, 'selftest.txt')
        self.app.selftest = out
        keep = self.app.root.destroy
        self.app.root.destroy = lambda: None      # the probe would close the window
        try:
            self.app._run_selftest()
            self.pump(0.3)
        finally:
            self.app.root.destroy = keep
        with io.open(out, encoding='utf-8') as f:
            line = f.read()
        self.assertIn(f'version={M.VERSION}', line)
        self.assertIn(f'tools={len(data.TOOLS)}', line)
        self.assertIn('chapters=6', line)


class Untested(unittest.TestCase):
    def test_file_is_valid(self):
        with io.open(os.path.join(ROOT, 'untested.json'), encoding='utf-8') as f:
            tests = json.load(f)['tests']
        ids = [t['id'] for t in tests]
        self.assertEqual(len(ids), len(set(ids)))
        for t in tests:
            for key in ('title', 'why', 'steps', 'expect'):
                self.assertTrue(t.get(key), f'{t["id"]}: {key}')
                self.assertTrue(t[key].get('de') and t[key].get('en'), f'{t["id"]}: {key}')


if __name__ == '__main__':
    unittest.main()
