"""Guide window of the Modding Hub: Help > Guide, F1 (PY_TOOL_DESIGN.md 6.2).

Chapter tree on the left, text on the right, search on top, German and
English. The tables are built from the same data the window shows
(data.TOOLS, data.FORMATS), each with a source line.
"""

import re
import tkinter as tk
from tkinter import ttk

import theme


def _lang():
    import modding_hub as M
    return M._LANG


def _l(de, en):
    return de if _lang() == 'de' else en


def _table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for r in rows:
        out.append('| ' + ' | '.join(str(c) for c in r) + ' |')
    return '\n'.join(out)


def _source(text):
    return _l('Quelle: ', 'Source: ') + text + '\n'


def ch_start():
    keys = [('Strg+F', 'Ctrl+F', _l('ins Suchfeld springen', 'jump into the search field')),
            ('Esc', 'Esc', _l('Suche leeren', 'clear the search')),
            ('Enter', 'Enter', _l('den gewaehlten Eintrag starten oder oeffnen',
                                  'start or open the selected entry')),
            ('F1', 'F1', _l('Dieser Guide', 'This guide'))]
    rows = [(k[0] if _lang() == 'de' else k[1], k[2]) for k in keys]
    return _l('''# Einstieg

Der Hub ist die Eingangstuer zum Modden von Two Worlds 1: er sammelt die
Werkzeuge, ihre Anleitungen und die Dateiformate des Spiels in einem Fenster.

- **Werkzeuge:** jedes Programm der Sammlung. Gruen heisst, der Hub hat es auf
  diesem Rechner gefunden und kann es starten. Grau heisst, es fehlt - rechts
  steht der Download.
- **Anleitungen:** die Texte aus dem Ordner `guides` neben dem Hub, auf
  Deutsch und Englisch.
- **Dateiformate:** was `.wd`, `.lan`, `.par` und die anderen Endungen des
  Spiels enthalten, und welches Werkzeug sie anfasst.

Das Suchfeld oben rechts filtert die offene Liste - ein Wort, ein Werkzeugname
oder eine Endung wie `.phx`.

''', '''# Getting started

The hub is the front door to modding Two Worlds 1: it gathers the tools,
their guides and the file formats of the game in one window.

- **Tools:** every program of the collection. Green means the hub found it on
  this PC and can start it. Grey means it is missing - the download is on the
  right.
- **Guides:** the texts from the `guides` folder next to the hub, in German
  and English.
- **File formats:** what `.wd`, `.lan`, `.par` and the other extensions of the
  game hold, and which tool touches them.

The search field at the top right filters the open list - a word, a tool name
or an extension like `.phx`.

''') + _table([_l('Taste', 'Key'), _l('Wirkung', 'Action')], rows) + '\n' + _source('modding_hub.py, _bind_keys')


def ch_tools():
    import data
    have = sum(1 for t in data.TOOLS if t.get('type') == 'exe')
    return _l(f'''# Werkzeuge

Die Liste kennt {len(data.TOOLS)} Eintraege, {have} davon sind fertige
Programme, der Rest sind Python-Skripte.

1. Einen Eintrag anklicken. Rechts steht, was er tut, welche Formate er
   anfasst und wo er liegt.
2. **Starten** oeffnet das Programm (Doppelklick tut dasselbe).
3. Fehlt es, fuehrt **Download** zur Bezugsquelle - bei den Werkzeugen von
   Alchemy Fox direkt zur neuesten Fassung.
4. Liegt ein Programm woanders auf der Platte, zeigt man es dem Hub einmal
   ueber **Datei waehlen...**; der Pfad wird gemerkt, bis man ihn mit
   **Pfad vergessen** wieder loescht.

Gesucht wird neben dem Hub selbst, im Spielordner (Datei > Spielordner
waehlen) und in den Unterordnern, die zum Eintrag gehoeren.

Python-Skripte brauchen Python 3 auf dem Rechner; der Hub startet sie mit
demselben Python, mit dem er selbst laeuft.
''', f'''# Tools

The list holds {len(data.TOOLS)} entries, {have} of them ready-made programs,
the rest Python scripts.

1. Click an entry. The right side says what it does, which formats it touches
   and where it sits.
2. **Start** opens the program (a double click does the same).
3. If it is missing, **Download** leads to where it comes from - for the
   Alchemy Fox tools straight to the newest release.
4. If a program lives elsewhere on the disk, show it to the hub once with
   **Choose file...**; the path is kept until **Forget path** clears it.

The hub searches next to itself, in the game folder (File > Pick a game
folder) and in the subfolders that belong to the entry.

Python scripts need Python 3 on the PC; the hub starts them with the same
Python it runs on itself.
''')


def ch_guides():
    import data
    rows = [(g['title_en'], ', '.join((g.get('tags') or [])[:3])) for g in data.GUIDES]
    return _l('''# Anleitungen

Die Anleitungen sind gewoehnliche Textdateien im Ordner `guides` neben dem
Hub. Der Reiter zeigt sie mit Suche; **In einem Fenster oeffnen** macht ein
eigenes Fenster auf, in dem man ebenfalls suchen kann.

Eigene Anleitung dazulegen: die Datei in den Ordner legen (Datei >
Anleitungen-Ordner oeffnen), Name auf `_de` oder `_en` enden lassen. Beim
naechsten Start steht sie in der Liste.

''', '''# Guides

The guides are plain text files in the `guides` folder next to the hub. The
tab shows them with a search; **Open in a window** gives a window of its own,
with its own search.

To add your own: drop the file into the folder (File > Open guides folder)
and let the name end in `_de` or `_en`. It is in the list on the next start.

''') + _table([_l('Anleitung', 'Guide'), _l('Schlagworte', 'Tags')], rows) + '\n' + _source('data.py, GUIDES')


def ch_formats():
    import data
    rows = [(ext, (entry.get(_lang()) or entry.get('en') or '').split('—')[0].strip())
            for ext, entry in data.FORMATS.items()]
    return _l('''# Dateiformate

Was in den Dateien des Spiels steckt. Der Reiter zeigt zu jeder Endung den
langen Text und die Werkzeuge, die damit umgehen.

''', '''# File formats

What sits inside the files of the game. The tab shows the long text for every
extension and the tools that handle it.

''') + _table([_l('Endung', 'Extension'), _l('Kurz', 'In short')], rows) + '\n' + _source('data.py, FORMATS')


def ch_own():
    return _l('''# Eigene Eintraege

Der Hub liest beim Start drei Quellen: die eingebaute Liste (`data.py`), die
Textdateien im Ordner `guides` und die eigenen Eintraege aus der
Einstellungsdatei.

- **Eigenes Werkzeug:** in der Einstellungsdatei unter `user_tools` ein
  Eintrag mit `id`, `name`, `desc_en`, `desc_de`, `filename` und, wenn
  vorhanden, `download`. Die Datei liegt bei der Exe unter
  `%LOCALAPPDATA%\\TW1ModdingHub\\modding_hub_settings.json`, beim Skript
  daneben.
- **Eigene Anleitung:** Textdatei in den Ordner `guides`.

Nichts davon wird ueberschrieben, wenn der Hub sich selbst aktualisiert.
''', '''# Your own entries

At start the hub reads three sources: the built-in list (`data.py`), the text
files in the `guides` folder and your own entries from the settings file.

- **Your own tool:** an entry under `user_tools` in the settings file with
  `id`, `name`, `desc_en`, `desc_de`, `filename` and, if there is one,
  `download`. The file sits next to the exe under
  `%LOCALAPPDATA%\\TW1ModdingHub\\modding_hub_settings.json`, or next to the
  script.
- **Your own guide:** a text file in the `guides` folder.

None of it is overwritten when the hub updates itself.
''')


def ch_trouble():
    return _l('''# Fehlersuche

## "Auf diesem Rechner nicht gefunden"

Das Programm liegt woanders. **Datei waehlen...** zeigt dem Hub den Pfad, oder
**Download** holt es.

## Ein Python-Skript startet nicht

Es braucht Python 3. Ohne Python bleibt der Knopf zwar da, das Fenster meldet
aber den Fehler von Windows.

## Die Anleitung ist leer

Die Textdatei fehlt im Ordner `guides`. Datei > Anleitungen-Ordner oeffnen
zeigt, wo er liegt.

## Der Hub findet das Spiel nicht

Datei > Spielordner waehlen, den Ordner mit `WDFiles` nehmen. Danach sucht der
Hub auch dort nach Werkzeugen des SDK.
''', '''# Troubleshooting

## "Not found on this PC"

The program sits somewhere else. **Choose file...** shows the hub the path, or
**Download** fetches it.

## A Python script does not start

It needs Python 3. Without Python the button stays, but the window reports
what Windows said.

## A guide is empty

The text file is missing from the `guides` folder. File > Open guides folder
shows where it is.

## The hub does not find the game

File > Pick a game folder, take the folder with `WDFiles`. After that the hub
also looks there for tools of the SDK.
''')


CHAPTERS = (
    ('start', ('Einstieg', 'Getting started'), ch_start),
    ('tools', ('Werkzeuge', 'Tools'), ch_tools),
    ('guides', ('Anleitungen', 'Guides'), ch_guides),
    ('formats', ('Dateiformate', 'File formats'), ch_formats),
    ('own', ('Eigene Eintraege', 'Your own entries'), ch_own),
    ('trouble', ('Fehlersuche', 'Troubleshooting'), ch_trouble),
)


_SEPARATOR = re.compile(r'^\|[\s|:-]+\|?$')
_LIST_ITEM = re.compile(r'^(- |\d+\. )')


def _prepare(text):
    """Join wrapped prose lines into paragraphs and turn markdown tables into
    aligned columns, so the text widget shows them readably."""
    out, para, table, in_code = [], [], [], False

    def flush_para():
        if para:
            out.append(' '.join(x.strip() for x in para))
            para.clear()

    def flush_table():
        if not table:
            return
        rows = [[c.strip().replace('`', '') for c in r.strip().strip('|').split('|')]
                for r in table if not _SEPARATOR.match(r.strip())]
        ncol = max(len(r) for r in rows)
        widths = [max(len(r[i]) if i < len(r) else 0 for r in rows) for i in range(ncol)]
        out.append('```')
        for n, r in enumerate(rows):
            cells = [(r[i] if i < len(r) else '').ljust(widths[i]) for i in range(ncol)]
            out.append('  '.join(cells).rstrip())
            if n == 0:
                out.append('  '.join('-' * w for w in widths))
        out.append('```')
        table.clear()

    for ln in text.split('\n'):
        if ln.startswith('```'):
            flush_para()
            flush_table()
            in_code = not in_code
            out.append(ln)
            continue
        if in_code:
            out.append(ln)
            continue
        if ln.startswith('|'):
            flush_para()
            table.append(ln)
            continue
        flush_table()
        stripped = ln.strip()
        if not stripped or ln.startswith('#'):
            flush_para()
            out.append(ln)
        elif _LIST_ITEM.match(stripped):
            flush_para()
            para.append(ln)
        else:
            para.append(ln)
    flush_para()
    flush_table()
    return '\n'.join(out)


def render_markdown(txt, text):
    in_code = False
    for line in text.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
            continue
        if in_code or line.startswith('|'):
            txt.insert('end', line + '\n', 'code')
            continue
        m = re.match(r'(#{1,3}) (.*)', line)
        if m:
            txt.insert('end', m.group(2) + '\n', 'h%d' % len(m.group(1)))
            continue
        tag = None
        if re.match(r'\s*[-*] ', line):
            line = '• ' + re.sub(r'^\s*[-*] ', '', line)
            tag = 'li'
        elif re.match(r'\s*\d+\. ', line):
            tag = 'li'
        for part in re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', line):
            if part.startswith('`') and part.endswith('`') and len(part) > 1:
                txt.insert('end', part[1:-1], ('inline',) + ((tag,) if tag else ()))
            elif part.startswith('**') and part.endswith('**'):
                txt.insert('end', part[2:-2], ('bold',) + ((tag,) if tag else ()))
            else:
                part = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', part)
                txt.insert('end', part, tag)
        txt.insert('end', '\n', tag)


def chapter_text(cid):
    for key, _title, fn in CHAPTERS:
        if key == cid:
            return fn()
    return ''


def check_sources():
    """Every table in every chapter (both languages) carries a source line."""
    import modding_hub as M
    saved = M._LANG
    try:
        for lang in ('de', 'en'):
            M._LANG = lang
            for cid, _t, fn in CHAPTERS:
                lines = fn().split('\n')
                for i, ln in enumerate(lines):
                    if ln.startswith('|---'):
                        j = i + 1
                        while j < len(lines) and lines[j].startswith('|'):
                            j += 1
                        tail = '\n'.join(lines[j:j + 3])
                        assert 'Quelle:' in tail or 'Source:' in tail, f'{cid}/{lang}: table without source'
    finally:
        M._LANG = saved


class GuideWindow:
    _open = None

    @classmethod
    def show(cls, app, chapter='start'):
        win = cls._open
        if win is not None:
            try:
                win.front()
                win.select(chapter)
                return win
            except tk.TclError:
                cls._open = None
        cls._open = cls(app, chapter)
        return cls._open

    def __init__(self, app, chapter='start'):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title('Modding Hub Guide')
        self.win.geometry('1000x700')
        self.win.minsize(820, 520)
        theme.dark_titlebar(self.win)
        self.win.protocol('WM_DELETE_WINDOW', self.close)
        self.win.bind('<Escape>', lambda e: self.close())
        top = ttk.Frame(self.win, padding=(10, 8))
        top.pack(fill='x')
        ttk.Label(top, text=_l('Suche', 'Search')).pack(side='left')
        self.q = tk.StringVar()
        ent = ttk.Entry(top, textvariable=self.q, width=32)
        ent.pack(side='left', padx=6)
        ent.bind('<KeyRelease>', lambda e: self._search())
        self.hits = ttk.Label(top, style='Muted.TLabel')
        self.hits.pack(side='left', padx=8)
        body = ttk.PanedWindow(self.win, orient='horizontal')
        body.pack(fill='both', expand=True)
        left = ttk.Frame(body)
        self.tree = ttk.Treeview(left, show='tree', selectmode='browse')
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', lambda e: self._show_selected())
        right = ttk.Frame(body)
        sb = ttk.Scrollbar(right, orient='vertical')
        self.txt = tk.Text(right, wrap='word', bd=0, padx=26, pady=20, cursor='arrow',
                           spacing1=2, spacing3=4, yscrollcommand=sb.set, font=('Segoe UI', 10))
        sb.configure(command=self.txt.yview)
        sb.pack(side='right', fill='y')
        self.txt.pack(fill='both', expand=True)
        for tag, kw in (('h1', dict(font=theme.FONT_H1, foreground=theme.GOLD, spacing1=18)),
                        ('h2', dict(font=theme.FONT_H2, foreground=theme.GOLD_HI, spacing1=14)),
                        ('h3', dict(font=('Segoe UI Semibold', 10), foreground=theme.GOLD_HI, spacing1=8)),
                        ('li', dict(lmargin1=20, lmargin2=34)),
                        ('code', dict(font=theme.FONT_MONO, background=theme.FIELD, lmargin1=16, lmargin2=16)),
                        ('inline', dict(font=theme.FONT_MONO, foreground=theme.GOLD_HI)),
                        ('bold', dict(font=('Segoe UI Semibold', 10))),
                        ('hit', dict(background=theme.SEL, foreground=theme.GOLD_HI))):
            self.txt.tag_configure(tag, **kw)
        body.add(left, weight=0)
        body.add(right, weight=1)
        self.win.update_idletasks()
        try:
            body.sashpos(0, 250)
        except tk.TclError:
            pass
        self._fill_tree()
        self.select(chapter)
        self.front()

    def front(self):
        """Das Fenster nach vorn holen - sonst geht es hinter dem Hauptfenster auf."""
        try:
            self.win.lift()
            self.win.focus_force()
            self.win.attributes('-topmost', True)          # einmal nach vorn,
            self.win.after(120, lambda: self.win.attributes('-topmost', False))
        except tk.TclError:                                # und gleich wieder normal
            pass

    def close(self):
        GuideWindow._open = None
        self.win.destroy()

    def _fill_tree(self, only=None):
        self.tree.delete(*self.tree.get_children())
        lang = 0 if _lang() == 'de' else 1
        for i, (cid, titles, _fn) in enumerate(CHAPTERS, start=1):
            if only is not None and cid not in only:
                continue
            self.tree.insert('', 'end', iid=cid, text=f'{i}. {titles[lang]}')

    def select(self, cid):
        if cid not in {c for c, _t, _f in CHAPTERS}:
            cid = 'start'
        if not self.tree.exists(cid):
            self._fill_tree()
        self.tree.selection_set(cid)
        self.tree.see(cid)
        self._show(cid)

    def _show_selected(self):
        sel = self.tree.selection()
        if sel:
            self._show(sel[0])

    def _show(self, cid):
        self.current = cid
        self.txt.configure(state='normal')
        self.txt.delete('1.0', 'end')
        render_markdown(self.txt, _prepare(chapter_text(cid)))
        self._mark_hits()
        self.txt.configure(state='disabled')

    def _search(self):
        needle = self.q.get().strip().lower()
        if not needle:
            self._fill_tree()
            self.hits.configure(text='')
            self.select(getattr(self, 'current', 'start'))
            return
        found = [cid for cid, _t, fn in CHAPTERS if needle in fn().lower()]
        self._fill_tree(set(found))
        self.hits.configure(text=_l('{n} Kapitel', '{n} chapters').format(n=len(found)))
        if found:
            self.select(found[0])

    def _mark_hits(self):
        needle = self.q.get().strip() if hasattr(self, 'q') else ''
        self.txt.tag_remove('hit', '1.0', 'end')
        if not needle:
            return
        first = None
        pos = '1.0'
        while True:
            pos = self.txt.search(needle, pos, nocase=True, stopindex='end')
            if not pos:
                break
            end = f'{pos}+{len(needle)}c'
            self.txt.tag_add('hit', pos, end)
            first = first or pos
            pos = end
        if first:
            self.txt.see(first)
