# 🎮 TW1 Modding Hub v2.0

Central hub for all Two Worlds 1 modding tools, guides, and file format documentation.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## Overview

The TW1 Modding Hub provides a single entry point for the entire Two Worlds 1 modding ecosystem. It automatically detects installed tools, provides bilingual guides (English & German), documents all proprietary file formats, and makes it easy to launch any tool from one place.

**Key Features:**
- 🔧 **11 tools** with auto-detection, manual path selection, and download links
- 📖 **6+ guides** loaded from external files — drop new `.txt` files into the `guides/` folder and they appear automatically
- 🌍 **Bilingual** — full English and German support (UI + all guides)
- 📄 **File format database** — documentation for all TW1 formats (.wd, .lan, .par, .lnd, .vdf, .phx, .lhc, .idx, .qtx, .shf, .bmp)
- 🔍 **Search** across tools, guides, and file formats
- ⚙️ **Settings** — language, font size, view mode, custom tool paths
- ➕ **Extensible** — add custom tools and guides through the UI or by dropping files

---

## Screenshot

![Hub Screenshot 1](https://alchimist-sotw.de/github/Hub1.png)
![Hub Screenshot 2](https://alchimist-sotw.de/github/Hub2.png)


---

## Installation

### Requirements
- Python 3.10 or higher
- Windows (for tool launching and DPI awareness)
- tkinter (included with Python on Windows)

### Setup

1. Download or clone this repository
2. Place the hub files in your modding workspace:

```
YourModdingFolder/
├── TW_ModdingHub.exe          (or tw1_modding_hub.py)
├── tw1_modding_hub.json       (created automatically on first run)
└── guides/
    ├── editor_beginner_guide_en.txt
    ├── editor_beginner_guide_de.txt
    ├── dungeon_guide_part1_en.txt
    ├── dungeon_guide_part1_de.txt
    ├── dungeon_guide_part2_en.txt
    ├── dungeon_guide_part2_de.txt
    ├── map_to_mod_guide_en.txt
    └── map_to_mod_guide_de.txt
```

3. Run:
```bash
python tw1_modding_hub.py
```

Or use the compiled `.exe` if available.

---

## Tools Registry

The hub manages these tools. Found tools show a **Launch** button, missing tools show **Download** + **Set Path** buttons.

| Tool | Formats | Source |
|------|---------|--------|
| TW Editor CMD Injector | — | [GitHub](https://github.com/MedievalDev/TwoWorldsEditor_Command_Injector) |
| TW1 LAN Viewer | .lan | [GitHub](https://github.com/MedievalDev/Twor-Worlds-Dialog-Viewer-Editor) |
| TW1 Quest Editor | .idx .qtx .shf | [GitHub](https://github.com/MedievalDev/Twor-Worlds-Dialog-Viewer-Editor) |
| TW1 PAR Tool | .par | [GitHub](https://github.com/MedievalDev/TwoWorlds_PAR_Editor) |
| TW1 VDF In/Export Tool | .vdf | [GitHub](https://github.com/MedievalDev/Two-Worlds-VDF-In-Export-Tool) |
| TW1 LND Viewer | .lnd | [GitHub](https://github.com/MedievalDev/Twor-Worlds-LND-Viewer) |
| TW1 Modding Guide | — | [GitHub](https://github.com/MedievalDev/Two-Worlds-Modding-Guid) |
| TwoWorlds Editor | .lnd | [ModDB](https://www.moddb.com/games/two-worlds/downloads) |
| WhizzEdit | .shf .idx | [ModDB](https://www.moddb.com/games/two-worlds/downloads) |
| Mod Selector (Buglord) | .wd | [GitHub](https://github.com/MedievalDev/Two-Worlds-Modding-Guid) |
| WD Repacker (Buglord) | .wd | [ModDB](https://www.moddb.com/games/two-worlds/downloads) |

### Tool Auto-Detection

The hub searches for tools in this order:
1. Saved path from config (`tw1_modding_hub.json`)
2. Same directory as the hub
3. `../` and `../Tools/` relative to the hub
4. If not found: shows Download + Browse buttons

Custom paths are saved permanently — set once, works every time.

---

## Guides

### Built-in Guides (included as external files)

| Guide | Description |
|-------|-------------|
| Editor Beginner Guide | Complete TwoWorldsEditor reference — shortcuts, terrain, textures, objects, markers, console commands |
| Dungeon Guide Part 1 | Manual dungeon creation using the main editor (Smoothness method) |
| Dungeon Guide Part 2 | Block-based dungeon creation with the SDK Dungeon Editor tool |
| Map-to-Mod Guide | Complete workflow: editor save → PhysX cooking → rename → pack → activate |
| PhysX Cooking Reference | The 4 console commands and critical warnings (embedded) |
| File Format Overview | All TW1 file formats and which tool handles which (embedded) |

### Auto-Discovery

The hub scans the `guides/` folder on every launch. Any new `.txt` or `.md` file is automatically added to the guides list. The naming convention for bilingual guides:

```
my_new_guide_en.txt    ← English version
my_new_guide_de.txt    ← German version
```

Files with `_en`/`_de` suffixes are paired automatically. Files without a language suffix are treated as English.

---

## File Formats

The hub includes documentation for all Two Worlds 1 file formats:

| Format | Description |
|--------|-------------|
| `.wd` | Mod archive container (zlib-compressed, GUID-identified) |
| `.lan` | Language file — all localized game text (binary, UTF-16-LE) |
| `.par` | Parameter database — items, NPCs, skills, stats (binary, zlib) |
| `.lnd` | Level/map file — terrain, objects, spawns per 128x128 tile |
| `.vdf` | 3D model file — mesh geometry, textures, animations |
| `.phx` | Physics/collision data — must NOT be compressed in .wd |
| `.lhc` | LevelHeaders cache — map index, regenerate after changes |
| `.idx` | Quest data export — SOAP-XML from WhizzEdit |
| `.qtx` | Quest logic — plaintext, compiled for engine |
| `.shf` | WhizzEdit project — .NET binary, read-only |
| `.bmp` | Minimap bitmap per map tile |

---

## Configuration

Settings are stored in `tw1_modding_hub.json` next to the hub. This file is created automatically on first run and includes:

- Language preference (en/de)
- View mode (grid/list)
- Font size
- Guides folder path
- Custom tool paths
- User-added tools and guides

---

## Adding Custom Content

### Custom Tools
Click **+ Add Tool** in the Tools tab to register any `.py` or `.exe` as a new tool with:
- Name, description (EN/DE), supported file formats
- Path to the executable
- Optional download link

### Custom Guides
Click **+ Add Guide** in the Guides tab, or simply drop a `.txt`/`.md` file into the `guides/` folder.

---

## Credits

**Tools & Reverse Engineering**
- **Buglord** — wdio.py, Mod Selector, WD Repacker, WD/LAN/QTX format documentation

**Modding Guides & Testing**
- **JadetheReaper** — Map Test EX.wd, Map-to-Mod process documentation
- **Smoothness** — Editor tutorials, dungeon creation workflow, game object documentation

**Development**
- **MedievalDev** — TW1 Modding Hub, CMD Injector, LAN Viewer, Quest Editor, PAR Tool, VDF Tool, LND Viewer, Modding Guide Tool

**Documentation**
- **MedievalDev & Claude (Anthropic)** — Editor Beginner Guide, Dungeon Guide Part 1 & 2, Map-to-Mod Guide (EN + DE)

**Original Game & SDK**
- Reality Pump Studios — Two Worlds (2007)
- TopWare Interactive — Publisher

---

## License

MIT License — see [LICENSE](LICENSE) for details.
