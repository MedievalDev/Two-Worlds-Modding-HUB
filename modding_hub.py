"""TW1 Modding Hub - one door to every Two Worlds 1 modding tool.

Three lists in one window: the tools (found on this PC or with a download
link), the guides (text files next to the hub, in English and German) and
the file formats of the game. A search field filters whichever list is open.

Rebuilt for PY_TOOL_DESIGN.md (3.0.0): theme.py, menubar with DE/EN, guide
window (F1), tour on first start, ? marks, self-update, test window. What
the hub knows lives in data.py, the texts of the guides in guides/.
"""

import json
import os
import subprocess
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tkinter as tk                                   # noqa: E402
from tkinter import ttk, filedialog, messagebox        # noqa: E402

import data                                             # noqa: E402
import guidebook                                        # noqa: E402
import theme                                            # noqa: E402
import updater                                          # noqa: E402
from version import VERSION                             # noqa: E402

APP_NAME = 'TW1 MODDING HUB'
GITHUB_URL = 'https://github.com/MedievalDev/Two-Worlds-Modding-HUB'
SITE_URL = 'https://alchemy-fox.de/'
TOOLS_URL = 'https://alchemy-fox.de/game/TW1_Tools/'
COMMUNITY_URL = 'https://twmp.alchemy-fox.de/'
LINKS = (('GitHub-Repo', GITHUB_URL), ('Alchemy Fox', SITE_URL),
         ('Alle Werkzeuge', TOOLS_URL), ('Community', COMMUNITY_URL))
SEP = chr(92)
NL = chr(10)


# ------------------------------------------------------------------ Sprache --

_LANG = 'en'

DE = {
    # menus
    'File': 'Datei', 'View': 'Ansicht', 'Help': 'Hilfe',
    'Open guides folder': 'Anleitungen-Ordner oeffnen',
    'Pick a game folder...': 'Spielordner waehlen...',
    'Exit': 'Beenden', 'Language': 'Sprache',
    'Show tools without a download': 'Werkzeuge ohne Download zeigen',
    'Check for updates on start': 'Beim Start auf Updates pruefen',
    'Guide (F1)': 'Guide (F1)', 'Show the tour again': 'Rundgang noch einmal',
    'Check for updates...': 'Nach Updates suchen...', 'About': 'Ueber',
    # window
    'Tools': 'Werkzeuge', 'Guides': 'Anleitungen', 'File formats': 'Dateiformate',
    'Search': 'Suche',
    'Every tool, guide and file format of Two Worlds 1 in one window':
        'Jedes Werkzeug, jede Anleitung und jedes Dateiformat von Two Worlds 1 in einem Fenster',
    'ready': 'bereit',
    'Name': 'Name', 'State': 'Zustand', 'Formats': 'Formate', 'Kind': 'Art',
    'Extension': 'Endung', 'What it is': 'Was es ist',
    'found': 'gefunden', 'not here': 'nicht da',
    'Start': 'Starten', 'Download': 'Download', 'Choose file...': 'Datei waehlen...',
    'Forget path': 'Pfad vergessen', 'Tool page': 'Tool-Seite',
    'Open in a window': 'In einem Fenster oeffnen',
    'Nothing matches "{q}".': 'Nichts passt zu "{q}".',
    '{n} of {total} tools': '{n} von {total} Werkzeugen',
    '{n} of {total} guides': '{n} von {total} Anleitungen',
    '{n} of {total} formats': '{n} von {total} Formaten',
    'This tool is a Python script: it needs Python 3 on this PC.':
        'Dieses Werkzeug ist ein Python-Skript: es braucht Python 3 auf diesem Rechner.',
    'Not found on this PC. Download it, or point the hub at the file.':
        'Auf diesem Rechner nicht gefunden. Herunterladen, oder dem Hub die Datei zeigen.',
    'Starting {name} ...': 'Starte {name} ...',
    'Could not start {name}:{nl}{e}': 'Konnte {name} nicht starten:{nl}{e}',
    'The guide file is missing: {name}': 'Die Anleitungsdatei fehlt: {name}',
    'Guides folder: {path}': 'Anleitungen-Ordner: {path}',
    'Choose the program of {name}': 'Programm von {name} waehlen',
    'Path saved.': 'Pfad gemerkt.', 'Path forgotten.': 'Pfad vergessen.',
    'Used by': 'Gehoert zu',
    'No tool of the hub uses this format.': 'Kein Werkzeug des Hubs nutzt dieses Format.',
    'A tool is missing? Every tool of the hub with its download: {url}':
        'Ein Werkzeug fehlt? Alle Werkzeuge des Hubs mit Download: {url}',
    # about / updates
    'Version {v}': 'Fassung {v}',
    'Everything for Two Worlds 1 in one window. Free, CC0.':
        'Alles fuer Two Worlds 1 in einem Fenster. Frei, CC0.',
    'Close': 'Schliessen',
    'You are up to date ({v}).': 'Alles aktuell ({v}).',
    'Update check failed: {e}': 'Update-Pruefung fehlgeschlagen: {e}',
    # tour
    'Welcome': 'Willkommen',
    'This window holds three lists: the tools, their guides and the file formats of the game. One search field for all three.':
        'Dieses Fenster hat drei Listen: die Werkzeuge, ihre Anleitungen und die Dateiformate des Spiels. Ein Suchfeld fuer alle drei.',
    'The list': 'Die Liste',
    'Green means the hub found the program on this PC and can start it. Grey means it is not here - the download link is on the right.':
        'Gruen heisst: der Hub hat das Programm auf diesem Rechner gefunden und kann es starten. Grau heisst: es ist nicht da - der Download steht rechts.',
    'The panel': 'Die Seite rechts',
    'What the selected entry is, which formats it touches, and the buttons: start it, download it, or point the hub at the file.':
        'Was der gewaehlte Eintrag ist, welche Formate er anfasst, und die Knoepfe: starten, herunterladen oder dem Hub die Datei zeigen.',
    'Search': 'Suche',
    'Type a word, an extension like .wd, or a tool name. The open list shrinks to what matches.':
        'Ein Wort, eine Endung wie .wd oder einen Werkzeugnamen tippen. Die offene Liste schrumpft auf das Passende.',
    'Menu bar': 'Menueleiste',
    'Language, the guide (F1), links, and the update check sit up here.':
        'Sprache, der Guide (F1), Links und die Update-Pruefung sitzen hier oben.',
    'Tour': 'Rundgang', "Don't show at startup": 'Beim Start nicht mehr zeigen',
    'Back': 'Zurueck', 'Next': 'Weiter', 'Quit tour': 'Rundgang beenden',
    'Step {n} of {m}': 'Schritt {n} von {m}', 'Finish': 'Fertig',
}


def system_is_german():
    try:
        import locale
        return (locale.getdefaultlocale()[0] or '').lower().startswith('de')
    except Exception:
        return False


def tr(text):
    return DE.get(text, text) if _LANG == 'de' else text


def loc(entry, key):
    """'desc_en'/'desc_de' or 'title_en'/'title_de' by the current language."""
    return entry.get(f'{key}_{_LANG}') or entry.get(f'{key}_en') or ''


def data_dir():
    if getattr(sys, 'frozen', False):
        base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
        return os.path.join(base, 'TW1ModdingHub')
    return HERE


class Config(dict):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(data_dir(), 'modding_hub_settings.json')
        try:
            with open(self.path, encoding='utf-8') as f:
                self.update(json.load(f))
        except (OSError, ValueError):
            pass

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(dict(self), f, indent=1, ensure_ascii=False)
        except OSError:
            pass


def guides_dir(cfg):
    return cfg.get('guides_dir') or os.path.join(getattr(sys, '_MEIPASS', HERE), 'guides')


def tool_path(cfg, tool):
    """Where the program of ``tool`` is, or None."""
    saved = (cfg.get('tool_paths') or {}).get(tool['id'])
    if saved and os.path.exists(saved):
        return saved
    name = tool.get('filename') or ''
    if not name:
        return None
    here = [HERE, os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else HERE]
    for base in here:
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    game = cfg.get('game_dir')
    roots = [HERE] + ([game] if game else [])
    for root in roots:
        for sp in tool.get('search_paths') or []:
            p = os.path.normpath(os.path.join(root, sp, name))
            if os.path.exists(p):
                return p
    return None


def guide_text(guide, cfg):
    """The text of a guide: the file next to the hub, else the fallback."""
    name = guide.get(f'file_{_LANG}') or guide.get('file_en')
    if name:
        p = os.path.join(guides_dir(cfg), name)
        if os.path.isfile(p):
            try:
                with open(p, encoding='utf-8', errors='replace') as f:
                    return f.read()
            except OSError as e:
                return tr('The guide file is missing: {name}').format(name=f'{name} ({e})')
    return loc(guide, 'fallback') or tr('The guide file is missing: {name}').format(name=name or '?')


def help_mark(parent, text, chapter, app):
    lbl = ttk.Label(parent, text='?', foreground=theme.GOLD, cursor='hand2')
    lbl.pack(side='left', padx=(6, 0))
    theme.Tooltip(lbl, text)
    lbl.bind('<Button-1>', lambda ev: app.show_help(text, chapter))
    return lbl


GUIDE_STEPS = (
    {'title': 'Welcome', 'text': 'This window holds three lists: the tools, their guides and the file formats of the game. One search field for all three.', 'widget': None},
    {'title': 'The list', 'text': 'Green means the hub found the program on this PC and can start it. Grey means it is not here - the download link is on the right.', 'widget': 'tree'},
    {'title': 'The panel', 'text': 'What the selected entry is, which formats it touches, and the buttons: start it, download it, or point the hub at the file.', 'widget': 'side'},
    {'title': 'Search', 'text': 'Type a word, an extension like .wd, or a tool name. The open list shrinks to what matches.', 'widget': 'search'},
    {'title': 'Menu bar', 'text': 'Language, the guide (F1), links, and the update check sit up here.', 'widget': 'head'},
)


class Guide:
    def __init__(self, app):
        self.app, self.i, self.frames, self.win = app, 0, [], None

    def start(self):
        self.i = 0
        if self.win:
            self.win.destroy()
        self.win = tk.Toplevel(self.app.root)
        self.win.title(tr('Tour'))
        self.win.configure(background=theme.PANEL)
        self.win.transient(self.app.root)
        self.win.protocol('WM_DELETE_WINDOW', lambda: self.finish(False))
        theme.dark_titlebar(self.win)
        f = ttk.Frame(self.win, style='Panel.TFrame', padding=14)
        f.pack(fill='both', expand=True)
        self.head = ttk.Label(f, style='PanelTitle.TLabel')
        self.head.pack(anchor='w')
        self.title = ttk.Label(f, style='Panel.TLabel', font=theme.FONT_H2, foreground=theme.GOLD)
        self.title.pack(anchor='w', pady=(4, 6))
        self.text = ttk.Label(f, style='Panel.TLabel', wraplength=340, justify='left')
        self.text.pack(anchor='w')
        self.dont = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text=tr("Don't show at startup"), variable=self.dont,
                        style='Panel.TCheckbutton').pack(anchor='w', pady=(14, 8))
        b = ttk.Frame(f, style='Panel.TFrame')
        b.pack(fill='x')
        self.back = ttk.Button(b, text=tr('Back'), command=self.prev)
        self.back.pack(side='left')
        self.next = ttk.Button(b, text=tr('Next'), style='Accent.TButton', command=self.nxt)
        self.next.pack(side='left', padx=8)
        ttk.Button(b, text=tr('Quit tour'), command=lambda: self.finish(self.dont.get())).pack(side='right')
        self.win.bind('<Escape>', lambda e: self.finish(self.dont.get()))
        self.win.bind('<Return>', lambda e: self.nxt())
        self.show()
        self.place()
        try:                                   # sonst geht er hinter dem Fenster auf
            self.win.lift()
            self.win.attributes('-topmost', True)
        except tk.TclError:
            pass

    def place(self):
        """Rechts neben das Fenster, sonst hinein - nie aus dem Bildschirm."""
        r = self.app.root
        self.win.update_idletasks()
        w, h = self.win.winfo_width(), self.win.winfo_height()
        x, y = r.winfo_rootx() + r.winfo_width() + 8, r.winfo_rooty() + 60
        if x + w > r.winfo_screenwidth():
            x = max(0, r.winfo_rootx() + 16)
        y = min(y, max(0, r.winfo_screenheight() - h - 40))
        self.win.geometry(f'+{x}+{y}')

    def show(self):
        s = GUIDE_STEPS[self.i]
        self.head.configure(text=tr('Step {n} of {m}').format(n=self.i + 1, m=len(GUIDE_STEPS)))
        self.title.configure(text=tr(s['title']))
        self.text.configure(text=tr(s['text']))
        self.back.state(['!disabled'] if self.i > 0 else ['disabled'])
        self.next.configure(text=tr('Next') if self.i < len(GUIDE_STEPS) - 1 else tr('Finish'))
        self.highlight(getattr(self.app, s['widget'], None) if s['widget'] else None)

    def prev(self):
        if self.i > 0:
            self.i -= 1
            self.show()

    def nxt(self):
        if self.i < len(GUIDE_STEPS) - 1:
            self.i += 1
            self.show()
        else:
            self.finish(True)

    def highlight(self, widget):
        for f in self.frames:
            f.destroy()
        self.frames = []
        if widget is None:
            return
        root = self.app.root
        root.update_idletasks()
        x = widget.winfo_rootx() - root.winfo_rootx()
        y = widget.winfo_rooty() - root.winfo_rooty()
        w, h, t = widget.winfo_width(), widget.winfo_height(), 3
        for fx, fy, fw, fh in ((x, y, w, t), (x, y + h - t, w, t), (x, y, t, h), (x + w - t, y, t, h)):
            f = tk.Frame(root, background=theme.GOLD)
            f.place(x=fx, y=fy, width=fw, height=fh)
            self.frames.append(f)

    def finish(self, dont_show):
        self.highlight(None)
        if dont_show or self.i == len(GUIDE_STEPS) - 1:
            self.app.cfg['guide_seen'] = True
            self.app.cfg.save()
        if self.win:
            self.win.destroy()
            self.win = None


# ------------------------------------------------------------------ App --


class App:
    def __init__(self, carry=None):
        global _LANG
        self.cfg = Config()
        self._carry = carry or {}
        self.selftest = os.environ.get('TW1HUB_SELFTEST')
        _LANG = self.cfg.get('lang') or ('de' if system_is_german() else 'en')
        self.root = tk.Tk()
        self.root.withdraw()
        theme.apply_dark_theme(self.root)
        self.root.title(f'TW1 Modding Hub {VERSION}')
        self._icon()
        self.restart = False
        self.tools = list(data.TOOLS) + list(self.cfg.get('user_tools') or [])
        self.guides = list(data.GUIDES) + list(self.cfg.get('user_guides') or [])
        self.rows = []                        # what the open list shows
        self.current = None
        self.update_var = tk.BooleanVar(value=bool(self.cfg.get('update_check', True)))
        self.missing_var = tk.BooleanVar(value=bool(self.cfg.get('show_missing', True)))
        self.guide = Guide(self)
        self._init_feedback()
        self.build()
        self.place_window()
        self.root.deiconify()
        self.root.after(150, self._startup)

    # ---- feedback (tw1-testfenster) ----
    def _init_feedback(self):
        import foxfeedback_ui
        base = getattr(sys, '_MEIPASS', HERE)

        def cfg_set(key, value):
            self.cfg[key] = value
            self.cfg.save()
        self.fb = foxfeedback_ui.FeedbackUI(
            self.root, 'moddinghub', VERSION,
            cfg_get=lambda k, d=None: self.cfg.get(k, d), cfg_set=cfg_set,
            lang=_LANG, tests_file=os.path.join(base, 'untested.json'),
            open_guide=self.show_guide, tool_name='TW1 Modding Hub')
        self.root.report_callback_exception = self._crash

    def _crash(self, exc, val, tb):
        import traceback
        frames = traceback.extract_tb(tb)
        mine = [f for f in frames if os.path.dirname(os.path.abspath(f.filename))
                in (HERE, getattr(sys, '_MEIPASS', HERE))]
        where = mine[-1] if mine else (frames[-1] if frames else None)
        spot = f'{os.path.basename(where.filename)}:{where.lineno}' if where else '?'
        shown = ''.join(traceback.format_exception(exc, val, tb))[-3000:]
        try:
            self.fb.log.add(f'crash {exc.__name__} at {spot}')
            ErrorDialog(self, 'crash', f'{exc.__name__} at {spot}', shown, None,
                        title='crash: ' + exc.__name__)
        except Exception:
            sys.__excepthook__(exc, val, tb)

    def error(self, key, message, shown, guide=None):
        ErrorDialog(self, key, message, shown, guide)

    def _icon(self):
        base = getattr(sys, '_MEIPASS', HERE)
        ico = os.path.join(base, 'modding_hub.ico')
        if os.path.exists(ico):
            try:
                self.root.iconbitmap(default=ico)
            except Exception:
                pass

    def place_window(self):
        if self._carry.get('geometry'):
            self.root.geometry(self._carry['geometry'])
            return
        w, h = 1020, 660
        self.root.update_idletasks()
        x = max(0, (self.root.winfo_screenwidth() - w) // 2)
        y = max(0, (self.root.winfo_screenheight() - h) // 2 - 30)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.minsize(860, 560)

    # ---- start ----
    def _startup(self):
        if getattr(self, '_started', False):
            return
        self._started = True
        updater.cleanup_old()
        self.root.protocol('WM_DELETE_WINDOW', self._close)
        if self.selftest:
            self._run_selftest()
            return
        if not self._carry:
            if self.cfg.get('update_check', True):
                self.root.after(1500, self.check_updates)
            if not self.cfg.get('guide_seen'):
                self.root.after(500, self.guide.start)
            self.root.after(2500, self.fb.start)

    def _run_selftest(self):
        found = sum(1 for t in self.tools if tool_path(self.cfg, t))
        texts = sum(1 for g in self.guides if len(guide_text(g, self.cfg)) > 400)
        https = 'ok'
        try:
            import http.client  # noqa: F401
            import ssl  # noqa: F401
            import urllib.request  # noqa: F401
        except ImportError as e:
            https = f'missing:{e.name}'
        try:
            with open(self.selftest, 'w', encoding='utf-8') as f:
                f.write(f'version={VERSION} tools={len(self.tools)} found={found} '
                        f'guides={len(self.guides)}/{texts} formats={len(data.FORMATS)} '
                        f'chapters={len(guidebook.CHAPTERS)} tests={len(self.fb.tests)} '
                        f'https={https} frozen={getattr(sys, "frozen", False)}' + NL)
        finally:
            self.root.after(50, self.root.destroy)

    # ---- window ----
    def build(self):
        self.statusbar = ttk.Frame(self.root, style='Status.TFrame')
        self.statusbar.pack(fill='x', side='bottom')
        self.status_lbl = ttk.Label(self.statusbar, text='', style='Status.TLabel')
        self.status_lbl.pack(side='left', padx=10, pady=3)
        self.build_menubar()
        body = ttk.Frame(self.root, padding=(14, 10, 14, 8))
        body.pack(fill='both', expand=True)

        self.head = head = ttk.Frame(body)
        head.pack(fill='x')
        ttk.Label(head, text=tr('Every tool, guide and file format of Two Worlds 1 in one window'),
                  style='H1.TLabel').pack(side='left')
        help_mark(head, tr('Every tool, guide and file format of Two Worlds 1 in one window'),
                  'start', self)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *a: self.fill())
        right = ttk.Frame(head)
        right.pack(side='right')
        ttk.Label(right, text=tr('Search'), style='Muted.TLabel').pack(side='left', padx=(0, 6))
        self.search = ttk.Entry(right, textvariable=self.search_var, width=26)
        self.search.pack(side='left')

        self.tab = 'tools'
        self.tabbar = ttk.Frame(body)
        self.tabbar.pack(fill='x', pady=(12, 0))
        self.tab_btns = {}
        for key, name in (('tools', 'Tools'), ('guides', 'Guides'), ('formats', 'File formats')):
            b = ttk.Button(self.tabbar, text=tr(name), width=16,
                           command=lambda k=key: self.set_tab(k))
            b.pack(side='left', padx=(0, 6))
            self.tab_btns[key] = b
        ttk.Separator(body, orient='horizontal').pack(fill='x', pady=(10, 0))
        self._build_list(body)

    def _build_list(self, parent):
        """One list and one detail panel; the tab bar above decides what is in it."""
        self.body = body = ttk.Frame(parent, padding=(0, 10, 0, 0))
        body.pack(fill='both', expand=True)
        left = ttk.Frame(body)
        left.pack(side='left', fill='both', expand=True)
        cols = ('state', 'kind')
        self.tree = ttk.Treeview(left, columns=cols, show='tree headings', height=18)
        self.tree.heading('#0', text=tr('Name'))
        self.tree.heading('state', text=tr('State'))
        self.tree.heading('kind', text=tr('Kind'))
        self.tree.column('#0', width=320, anchor='w')
        self.tree.column('state', width=110, anchor='w')
        self.tree.column('kind', width=180, anchor='w')
        bar = ttk.Scrollbar(left, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)
        self.tree.tag_configure('found', foreground=theme.OK)
        self.tree.tag_configure('missing', foreground=theme.MUT)
        self.tree.bind('<<TreeviewSelect>>', lambda e: self.pick())
        self.tree.bind('<Double-1>', lambda e: self.primary())
        self.tree.bind('<Return>', lambda e: self.primary())

        self.side = side = ttk.Frame(body, padding=(14, 0, 0, 0), width=380)
        side.pack(side='left', fill='both')
        side.pack_propagate(False)
        self.title_lbl = ttk.Label(side, text='', style='H2.TLabel', wraplength=360,
                                   justify='left')
        self.title_lbl.pack(anchor='w')
        self.desc_lbl = ttk.Label(side, text='', wraplength=360, justify='left',
                                  style='Muted.TLabel')
        self.desc_lbl.pack(anchor='w', pady=(6, 8))
        self.meta_lbl = ttk.Label(side, text='', wraplength=360, justify='left',
                                  style='Muted.TLabel')
        self.meta_lbl.pack(anchor='w')
        self.text = tk.Text(side, wrap='word', height=14, background=theme.FIELD,
                            foreground=theme.INK, relief='flat', font=theme.FONT_MONO,
                            highlightthickness=0, padx=8, pady=6)
        self.btns = ttk.Frame(side)
        self.btns.pack(side='bottom', fill='x', pady=(10, 0))
        self.btn_main = ttk.Button(self.btns, text=tr('Start'), style='Accent.TButton',
                                   command=self.primary)
        self.btn_dl = ttk.Button(self.btns, text=tr('Download'), command=self.download)
        self.btn_pick = ttk.Button(self.btns, text=tr('Choose file...'), command=self.pick_file)
        self.btn_page = ttk.Button(self.btns, text=tr('Tool page'), command=self.open_page)
        self.fill()

    def build_menubar(self):
        bar = ttk.Frame(self.root, style='Menubar.TFrame')
        bar.pack(fill='x')
        self.menubar = bar
        for key, filler in ((tr('File'), self._fill_file), (tr('View'), self._fill_view),
                            (tr('Help'), self._fill_help)):
            item = ttk.Label(bar, text=key, style='Menubar.TLabel')
            item.pack(side='left')
            item.bind('<Button-1>', lambda ev, f=filler, w=item: self._popup(f, w))
            item.bind('<Enter>', lambda ev, w=item: w.state(['active']))
            item.bind('<Leave>', lambda ev, w=item: w.state(['!active']))
        ttk.Label(bar, text=APP_NAME, style='Menubar.TLabel').pack(side='right', padx=(0, 6))
        box = ttk.Frame(bar, style='Menubar.TFrame')
        for i, code in enumerate(('de', 'en')):
            if i:
                ttk.Label(box, text='·', style='Menubar.TLabel', padding=(2, 5)).pack(side='left')
            lbl = ttk.Label(box, text=code.upper(), style='Menubar.TLabel', padding=(4, 5), cursor='hand2',
                            foreground=theme.GOLD if code == _LANG else theme.MUT)
            lbl.pack(side='left')
            lbl.bind('<Button-1>', lambda ev, c=code: self.set_lang(c))
        box.pack(side='right', padx=(0, 10))
        self._bind_keys()

    def _popup(self, filler, widget):
        menu = theme.Menu(self.root)
        filler(menu)
        try:
            menu.tk_popup(widget.winfo_rootx(), widget.winfo_rooty() + widget.winfo_height())
        finally:
            menu.grab_release()

    def _fill_file(self, m):
        m.add_command(label=tr('Open guides folder'), command=self.open_guides_folder)
        m.add_command(label=tr('Pick a game folder...'), command=self.pick_game_dir)
        m.add_separator()
        m.add_command(label=tr('Exit'), command=self._close)

    def _fill_view(self, m):
        lang = theme.Menu(m, tearoff=0)
        lang.add_command(label='Deutsch', command=lambda: self.set_lang('de'))
        lang.add_command(label='English', command=lambda: self.set_lang('en'))
        m.add_cascade(label=tr('Language'), menu=lang)
        m.add_checkbutton(label=tr('Show tools without a download'), variable=self.missing_var,
                          command=self._toggle_missing)

    def _fill_help(self, m):
        m.add_command(label=tr('Guide (F1)'), command=self.show_guide)
        m.add_command(label=tr('Show the tour again'), command=self.guide.start)
        m.add_separator()
        self.fb.add_menu_items(m)
        m.add_separator()
        for label, url in LINKS:
            m.add_command(label=label, command=lambda u=url: webbrowser.open(u))
        m.add_separator()
        m.add_checkbutton(label=tr('Check for updates on start'), variable=self.update_var,
                          command=self._toggle_update_check)
        m.add_command(label=tr('Check for updates...'), command=lambda: self.check_updates(True))
        m.add_command(label=tr('About'), command=self.show_about)

    def _bind_keys(self):
        self.root.bind('<F1>', lambda e: self.show_guide())
        self.root.bind('<Control-f>', lambda e: self.search.focus_set())
        self.root.bind('<Escape>', lambda e: self.search_var.set(''))

    # ---- status, guide ----
    def status(self, text, error=False):
        self.status_lbl.configure(text=text, foreground=theme.ERR if error else theme.MUT)

    def show_guide(self, chapter='start'):
        guidebook.GuideWindow.show(self, chapter)

    def show_help(self, text, chapter):
        self.status(text.split(NL)[0][:140])
        self.show_guide(chapter)

    # ---- the three lists ----
    def kind(self):
        return self.tab

    def set_tab(self, key):
        self.tab = key
        for k, b in self.tab_btns.items():
            b.configure(style='Accent.TButton' if k == key else 'TButton')
        self.fill()

    def fill(self):
        """Fill the list for the open tab, filtered by the search field."""
        kind = self.kind()
        for k, b in self.tab_btns.items():
            b.configure(style='Accent.TButton' if k == kind else 'TButton')
        q = (self.search_var.get() or '').strip().lower()
        self.tree.delete(*self.tree.get_children())
        self.rows = []
        if kind == 'tools':
            self.tree.heading('state', text=tr('State'))
            self.tree.heading('kind', text=tr('Formats'))
            total = 0
            for t in self.tools:
                path = tool_path(self.cfg, t)
                if not path and not self.missing_var.get():
                    continue
                total += 1
                hay = ' '.join((t['name'], loc(t, 'desc'), ' '.join(t.get('formats') or []),
                                t.get('filename', ''))).lower()
                if q and q not in hay:
                    continue
                self.rows.append(t)
                self.tree.insert('', 'end', text=t['name'],
                                 values=(tr('found') if path else tr('not here'),
                                         ' '.join(t.get('formats') or []) or '-'),
                                 tags=('found' if path else 'missing',))
            self.status(tr('{n} of {total} tools').format(n=len(self.rows), total=total))
        elif kind == 'guides':
            self.tree.heading('state', text=tr('Kind'))
            self.tree.heading('kind', text=tr('Used by'))
            for g in self.guides:
                hay = ' '.join((loc(g, 'title'), ' '.join(g.get('tags') or []),
                                guide_text(g, self.cfg)[:4000])).lower()
                if q and q not in hay:
                    continue
                self.rows.append(g)
                tools = [t['name'] for t in self.tools if t['id'] in (g.get('tool_ids') or [])]
                self.tree.insert('', 'end', text=loc(g, 'title'),
                                 values=(', '.join((g.get('tags') or [])[:2]),
                                         ', '.join(tools[:2]) or '-'))
            self.status(tr('{n} of {total} guides').format(n=len(self.rows), total=len(self.guides)))
        else:
            self.tree.heading('state', text=tr('Used by'))
            self.tree.heading('kind', text=tr('What it is'))
            for ext, entry in data.FORMATS.items():
                text = entry.get(_LANG) or entry.get('en') or ''
                if q and q not in (ext + ' ' + text).lower():
                    continue
                self.rows.append((ext, text))
                tools = [t['name'] for t in self.tools if ext in (t.get('formats') or [])]
                self.tree.insert('', 'end', text=ext, values=(', '.join(tools[:2]) or '-',
                                                              text.split('—')[0][:60]))
            self.status(tr('{n} of {total} formats').format(n=len(self.rows),
                                                            total=len(data.FORMATS)))
        if q and not self.rows:
            self.status(tr('Nothing matches "{q}".').format(q=q), error=True)
        if self.rows:
            keep = 0                          # keep the selection across a refill
            if self.current is not None:
                for i, row in enumerate(self.rows):
                    if row is self.current or (isinstance(row, dict) and isinstance(self.current, dict)
                                               and row.get('id') == self.current.get('id')):
                        keep = i
                        break
            item = self.tree.get_children()[keep]
            self.tree.selection_set(item)
            self.tree.focus(item)
        else:
            self.current = None
            self.show_detail(None)

    def pick(self):
        sel = self.tree.selection()
        if not sel:
            return
        i = self.tree.index(sel[0])
        if i < len(self.rows):
            self.current = self.rows[i]
            self.show_detail(self.current)

    def show_detail(self, item):
        for b in (self.btn_main, self.btn_dl, self.btn_pick, self.btn_page):
            b.pack_forget()
        self.text.pack_forget()
        if item is None:
            self.title_lbl.configure(text='')
            self.desc_lbl.configure(text='')
            self.meta_lbl.configure(text='')
            return
        kind = self.kind()
        if kind == 'tools':
            path = tool_path(self.cfg, item)
            self.title_lbl.configure(text=item['name'])
            self.desc_lbl.configure(text=loc(item, 'desc'))
            bits = []
            if item.get('formats'):
                bits.append(tr('Formats') + ': ' + ' '.join(item['formats']))
            if item.get('type') == 'python':
                bits.append(tr('This tool is a Python script: it needs Python 3 on this PC.'))
            bits.append(path if path else tr('Not found on this PC. Download it, or point the hub at the file.'))
            self.meta_lbl.configure(text=NL.join(bits))
            if path:
                self.btn_main.configure(text=tr('Start'))
                self.btn_main.pack(side='left')
                self.btn_pick.configure(text=tr('Forget path')
                                        if (self.cfg.get('tool_paths') or {}).get(item['id'])
                                        else tr('Choose file...'))
            else:
                self.btn_pick.configure(text=tr('Choose file...'))
            if item.get('download'):
                self.btn_dl.pack(side='left', padx=6)
            self.btn_pick.pack(side='left', padx=6)
            if item.get('page'):
                self.btn_page.pack(side='left', padx=6)
        elif kind == 'guides':
            self.title_lbl.configure(text=loc(item, 'title'))
            tools = [t['name'] for t in self.tools if t['id'] in (item.get('tool_ids') or [])]
            self.desc_lbl.configure(text=(tr('Used by') + ': ' + ', '.join(tools)) if tools else '')
            self.meta_lbl.configure(text=' '.join(item.get('tags') or []))
            self.text.configure(state='normal')
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', guide_text(item, self.cfg))
            self.text.configure(state='disabled')
            self.text.pack(fill='both', expand=True, pady=(8, 0))
            self.btn_main.configure(text=tr('Open in a window'))
            self.btn_main.pack(side='left')
        else:
            ext, text = item
            self.title_lbl.configure(text=ext)
            self.desc_lbl.configure(text=text)
            tools = [t['name'] for t in self.tools if ext in (t.get('formats') or [])]
            self.meta_lbl.configure(text=(tr('Used by') + ': ' + ', '.join(tools)) if tools
                                    else tr('No tool of the hub uses this format.'))

    # ---- actions ----
    def primary(self):
        item = self.current
        if item is None:
            return
        if self.kind() == 'tools':
            self.launch(item)
        elif self.kind() == 'guides':
            TextWindow(self, loc(item, 'title'), guide_text(item, self.cfg))

    def launch(self, tool):
        path = tool_path(self.cfg, tool)
        if not path:
            self.status(tr('Not found on this PC. Download it, or point the hub at the file.'),
                        error=True)
            return
        self.status(tr('Starting {name} ...').format(name=tool['name']))
        self.fb.log.add(f"launch {tool['id']}")
        try:
            if tool.get('type') == 'python' or path.lower().endswith('.py'):
                subprocess.Popen([sys.executable, path], cwd=os.path.dirname(path))
            else:
                subprocess.Popen([path], cwd=os.path.dirname(path))
        except OSError as e:
            self.error('launch.failed', 'Starting a tool failed',
                       tr('Could not start {name}:{nl}{e}').format(name=tool['name'], nl=NL, e=e),
                       'tools')

    def download(self):
        item = self.current
        if item and item.get('download'):
            webbrowser.open(item['download'])

    def open_page(self):
        item = self.current
        if item and item.get('page'):
            webbrowser.open(item['page'])

    def pick_file(self):
        item = self.current
        if item is None or self.kind() != 'tools':
            return
        paths = dict(self.cfg.get('tool_paths') or {})
        if paths.get(item['id']):
            paths.pop(item['id'], None)
            self.cfg['tool_paths'] = paths
            self.cfg.save()
            self.status(tr('Path forgotten.'))
            self.fill()
            return
        p = filedialog.askopenfilename(
            parent=self.root, title=tr('Choose the program of {name}').format(name=item['name']),
            filetypes=[('Programme', '*.exe;*.py'), ('Alle Dateien', '*.*')])
        if not p:
            return
        paths[item['id']] = os.path.normpath(p)
        self.cfg['tool_paths'] = paths
        self.cfg.save()
        self.status(tr('Path saved.'))
        self.fill()

    def open_guides_folder(self):
        d = guides_dir(self.cfg)
        if os.path.isdir(d):
            os.startfile(d)
            self.status(tr('Guides folder: {path}').format(path=d))

    def pick_game_dir(self):
        d = filedialog.askdirectory(parent=self.root, title=tr('Pick a game folder...'),
                                    initialdir=self.cfg.get('game_dir') or None)
        if d:
            self.cfg['game_dir'] = os.path.normpath(d)
            self.cfg.save()
            self.fill()

    def _toggle_missing(self):
        self.cfg['show_missing'] = bool(self.missing_var.get())
        self.cfg.save()
        self.fill()

    def _toggle_update_check(self):
        self.cfg['update_check'] = bool(self.update_var.get())
        self.cfg.save()

    # ---- language / close ----
    def _close(self):
        self.root.destroy()

    def set_lang(self, code):
        global _LANG
        if code == _LANG:
            return
        self.cfg['lang'] = code
        self.cfg.save()
        _LANG = code
        self.restart = True
        self.carry_out = {'geometry': self.root.geometry()}
        self.root.destroy()

    # ---- updates / about ----
    def check_updates(self, manual=False):
        results = []
        updater.check_async(lambda info, err: results.append((info, err)))

        def poll():
            try:
                if not self.root.winfo_exists():
                    return
            except tk.TclError:
                return
            if not results:
                self.root.after(400, poll)
                return
            info, err = results[0]
            if err and manual:
                self.status(tr('Update check failed: {e}').format(e=err), error=True)
            elif info and updater.is_newer(info['tag']):
                UpdateWindow(self, info)
            elif manual:
                self.status(tr('You are up to date ({v}).').format(v=VERSION))
        self.root.after(400, poll)

    def show_about(self):
        win = tk.Toplevel(self.root)
        win.title(tr('About'))
        win.transient(self.root)
        theme.dark_titlebar(win)
        f = ttk.Frame(win, padding=18)
        f.pack(fill='both', expand=True)
        ttk.Label(f, text='TW1 Modding Hub', style='Brand.TLabel').pack(anchor='w')
        ttk.Label(f, text=tr('Version {v}').format(v=VERSION), style='Muted.TLabel').pack(anchor='w')
        ttk.Label(f, text=tr('Everything for Two Worlds 1 in one window. Free, CC0.'),
                  wraplength=380, justify='left').pack(anchor='w', pady=(8, 10))
        for label, url in LINKS:
            link = ttk.Label(f, text=url, foreground=theme.GOLD, cursor='hand2')
            link.pack(anchor='w')
            link.bind('<Button-1>', lambda e, u=url: webbrowser.open(u))
        ttk.Button(f, text=tr('Close'), style='Accent.TButton',
                   command=win.destroy).pack(anchor='e', pady=(14, 0))
        win.update_idletasks()
        win.geometry(f'+{self.root.winfo_rootx() + 60}+{self.root.winfo_rooty() + 60}')

    def run(self):
        self.root.mainloop()


class TextWindow:
    """A guide in a window of its own, with a search field."""

    def __init__(self, app, title, text):
        self.win = win = tk.Toplevel(app.root)
        win.title(title)
        theme.dark_titlebar(win)
        win.geometry('860x640')
        f = ttk.Frame(win, padding=12)
        f.pack(fill='both', expand=True)
        top = ttk.Frame(f)
        top.pack(fill='x')
        ttk.Label(top, text=title, style='H2.TLabel').pack(side='left')
        self.var = tk.StringVar()
        ttk.Label(top, text=tr('Search'), style='Muted.TLabel').pack(side='left', padx=(14, 6))
        e = ttk.Entry(top, textvariable=self.var, width=24)
        e.pack(side='left')
        e.bind('<Return>', lambda ev: self.find())
        box = tk.Text(f, wrap='word', background=theme.FIELD, foreground=theme.INK,
                      relief='flat', font=theme.FONT_MONO, highlightthickness=0, padx=10, pady=8)
        bar = ttk.Scrollbar(f, orient='vertical', command=box.yview)
        box.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y', pady=(10, 0))
        box.pack(fill='both', expand=True, pady=(10, 0))
        box.insert('1.0', text)
        box.configure(state='disabled')
        box.tag_configure('hit', background=theme.GOLD, foreground=theme.BG)
        self.box = box
        win.bind('<Escape>', lambda ev: win.destroy())

    def find(self):
        q = self.var.get().strip()
        self.box.tag_remove('hit', '1.0', 'end')
        if not q:
            return
        i = '1.0'
        first = None
        while True:
            i = self.box.search(q, i, nocase=True, stopindex='end')
            if not i:
                break
            end = f'{i}+{len(q)}c'
            self.box.tag_add('hit', i, end)
            first = first or i
            i = end
        if first:
            self.box.see(first)


class ErrorDialog:
    """An error the user can report: message, OK, "Report a bug", guide."""

    def __init__(self, app, key, message, shown, guide=None, title=None):
        self.win = win = tk.Toplevel(app.root)
        win.title(tr('Error') if _LANG == 'en' else 'Fehler')
        win.transient(app.root)
        theme.dark_titlebar(win)
        win.bind('<Escape>', lambda e: win.destroy())
        win.bind('<Return>', lambda e: win.destroy())
        f = ttk.Frame(win, padding=16)
        f.pack(fill='both', expand=True)
        box = tk.Text(f, wrap='word', height=min(14, max(3, shown.count(NL) + 2 + len(shown) // 80)),
                      width=76, background=theme.FIELD, foreground=theme.INK, relief='flat',
                      font=theme.FONT_MONO, highlightthickness=0, padx=8, pady=6)
        box.insert('1.0', shown)
        box.configure(state='disabled')
        box.pack(fill='both', expand=True)
        btns = ttk.Frame(f)
        btns.pack(fill='x', pady=(12, 0))
        ttk.Button(btns, text='OK', style='Accent.TButton', command=win.destroy).pack(side='right')
        ttk.Button(btns, text='Bug melden...' if _LANG == 'de' else 'Report a bug...',
                   command=lambda: app.fb.report_bug(parent=win, error_text=shown, error_key=key,
                                                     title=title or f'{key}: {message}',
                                                     fp_text=message)).pack(side='right', padx=6)
        if guide:
            ttk.Button(btns, text='Im Guide lesen' if _LANG == 'de' else 'Read in the guide',
                       command=lambda: app.show_guide(guide)).pack(side='left')
        win.update_idletasks()
        win.geometry(f'+{app.root.winfo_rootx() + 40}+{app.root.winfo_rooty() + 60}')


class UpdateWindow:
    """A newer release exists: notes, update now, later, skip (design 9)."""

    def __init__(self, app, info):
        self.app, self.info = app, info
        self.win = win = tk.Toplevel(app.root)
        win.title('Update')
        win.transient(app.root)
        theme.dark_titlebar(win)
        f = ttk.Frame(win, padding=18)
        f.pack(fill='both', expand=True)
        ttk.Label(f, text=f'TW1 Modding Hub {info["version"]}', style='Brand.TLabel').pack(anchor='w')
        ttk.Label(f, text=f'{VERSION} -> {info["version"]}', style='Muted.TLabel').pack(anchor='w')
        box = tk.Text(f, wrap='word', height=12, width=74, background=theme.FIELD,
                      foreground=theme.INK, relief='flat', font=theme.FONT, highlightthickness=0,
                      padx=8, pady=6)
        box.insert('1.0', (info.get('notes') or '')[:4000])
        box.configure(state='disabled')
        box.pack(fill='both', expand=True, pady=(10, 0))
        self.bar = ttk.Progressbar(f, maximum=100)
        self.lbl = ttk.Label(f, text='', style='Muted.TLabel')
        btns = ttk.Frame(f)
        btns.pack(fill='x', pady=(12, 0))
        self.go = ttk.Button(btns, text='Jetzt aktualisieren' if _LANG == 'de' else 'Update now',
                             style='Accent.TButton', command=self.start)
        self.go.pack(side='right')
        ttk.Button(btns, text='Spaeter' if _LANG == 'de' else 'Later',
                   command=win.destroy).pack(side='right', padx=6)
        win.update_idletasks()
        win.geometry(f'+{app.root.winfo_rootx() + 50}+{app.root.winfo_rooty() + 50}')

    def start(self):
        import threading
        self.go.state(['disabled'])
        self.bar.pack(fill='x', pady=(10, 4))
        self.lbl.pack(anchor='w')
        results = []

        def work():
            try:
                exe = updater.frozen_exe()
                if not exe:
                    raise RuntimeError('nur die Exe kann sich selbst tauschen')
                tmp = updater.download(self.info, exe + '.new',
                                       lambda d, t: results.append(('p', d, t)))
                updater.start_swap(exe, tmp)
                results.append(('done', None, None))
            except Exception as e:                       # noqa: BLE001
                results.append(('err', e, None))

        threading.Thread(target=work, daemon=True).start()

        def poll():
            while results:
                kind, a, b = results.pop(0)
                if kind == 'p' and b:
                    self.bar.configure(value=100 * a / max(1, b))
                elif kind == 'done':
                    self.app.root.after(200, self.app.root.destroy)
                    return
                elif kind == 'err':
                    self.lbl.configure(text=str(a), foreground=theme.ERR)
                    self.go.state(['!disabled'])
                    return
            self.win.after(200, poll)
        self.win.after(200, poll)


def _check_translations():
    import re
    guidebook.check_sources()
    for k, v in DE.items():
        assert set(re.findall(r'\{\w+\}', k)) == set(re.findall(r'\{\w+\}', v)), k
    for s in GUIDE_STEPS:
        assert s['text'] in DE and s['title'] in DE, s['title']


def run_gui(carry=None):
    while True:
        app = App(carry)
        app.run()
        if not app.restart:
            break
        carry = getattr(app, 'carry_out', None) or {}


if __name__ == '__main__':
    _check_translations()
    run_gui()
