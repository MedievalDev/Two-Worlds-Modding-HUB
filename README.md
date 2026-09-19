# TW1 Modding Hub

One door to every Two Worlds 1 (2007) modding tool: the tools, their guides
and the file formats of the game in one window.

![License: CC0](https://img.shields.io/badge/license-CC0-green) ![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey)

**Download:** [`TW1_Modding_Hub.exe`](https://github.com/MedievalDev/Two-Worlds-Modding-HUB/releases/latest/download/TW1_Modding_Hub.exe) - one file, no install, no admin rights.

## What it does

- **Tools (23).** Every tool of the ecosystem with what it does and which
  formats it touches. Green means the hub found the program on this PC and
  starts it; grey means it is missing and the download link is one click
  away. A program somewhere else on the disk is shown to the hub once and
  remembered.
- **Guides (6).** The guide texts from the `guides` folder in English and
  German, with a search, and a window of its own per guide. Drop your own
  text file in and it is there on the next start.
- **File formats (11).** What `.wd`, `.lan`, `.par`, `.lnd`, `.phx`, `.lhc`
  and the rest hold - and which tool handles them.
- One search field for whichever list is open: a word, a tool name or an
  extension like `.phx`.
- **Guide inside** (F1) with chapters, search and the tables built from the
  same data the window shows. Tour on first start, gold `?` marks.
- **Self-update from GitHub**, SHA-256 verified. Test window and bug reports
  to the Alchemy Fox feedback server, never without a preview and a button.
- Dark theme, DE · EN, the same look as the other TW1 tools
  (PY_TOOL_DESIGN.md).

## Files

| File | Purpose |
|---|---|
| `modding_hub.py` | the window |
| `data.py` | what the hub knows: tools, guides, formats |
| `guidebook.py` | guide window (F1), chapters DE/EN, tables from `data.py` |
| `guides/` | the guide texts, one file per language |
| `theme.py`, `updater.py`, `foxfeedback*.py` | shared with the other TW1 tools |
| `tests/` | `py -3.13 -m unittest discover -s tests -t .` |
| `ModdingHub_V2/` | the previous version (2.1), kept for reference |

Build: `build_hub_exe.bat` (PyInstaller, one file), then `selftest_exe.bat`.

## All the tools

Every tool with page, source and download:
**https://alchemy-fox.de/game/TW1_Tools/** - their guides:
**https://alchemy-fox.de/game/TW1_Tools/guides/**

## Credits

- **Buglord** - wdio.py (the core of the WD Packer), Mod Selector, WD
  Repacker, TWSE, WD/LAN/QTX format documentation
- **JadetheReaper** - Map Test EX.wd, map-to-mod process
- **Smoothness** - editor tutorials, dungeon workflow
- **MedievalDev / Alchemy Fox** - the hub and the tools it lists
- Reality Pump Studios / TopWare Interactive - Two Worlds (2007)

## License

CC0 1.0 Universal - free for everyone, no conditions.
