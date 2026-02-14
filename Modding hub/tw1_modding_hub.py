#!/usr/bin/env python3
"""
TW1 Modding Hub v2.0
Central hub for all Two Worlds 1 modding tools and guides.
By MedievalDev — Credits: Buglord, JadetheReaper, Smoothness
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import json
import subprocess
import webbrowser
from pathlib import Path

VERSION = "2.0"
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "tw1_modding_hub.json")
GUIDES_DIR = os.path.join(SCRIPT_DIR, "guides")

# ============================================================
# THEME
# ============================================================
BG       = "#1a1a2e"
BG2      = "#16213e"
BG3      = "#0f3460"
BG4      = "#1b2a4a"
FG       = "#e8e8e8"
FG_DIM   = "#8888aa"
ACCENT   = "#e94560"
GREEN    = "#4ecca3"
YELLOW   = "#ffaa00"
RED      = "#ff6b6b"
BLUE     = "#64b5f6"
ORANGE   = "#ff9f43"
CYAN     = "#7dcfff"
PURPLE   = "#bb9af7"
PINK     = "#ff79c6"
CARD_BG  = "#16213e"
CARD_HL  = "#1e2d4d"
BORDER   = "#2a3a5e"
SEARCH_BG = "#0d1b33"

# ============================================================
# BILINGUAL STRINGS
# ============================================================
LANG = {
    "title":            {"en": "TW1 Modding Hub", "de": "TW1 Modding Hub"},
    "tools":            {"en": "Tools", "de": "Tools"},
    "guides":           {"en": "Guides", "de": "Anleitungen"},
    "settings":         {"en": "Settings", "de": "Einstellungen"},
    "search":           {"en": "Search tools, guides, file formats...", "de": "Tools, Anleitungen, Dateiformate suchen..."},
    "launch":           {"en": "Launch", "de": "Starten"},
    "not_found":        {"en": "Not Found", "de": "Nicht gefunden"},
    "found":            {"en": "Found", "de": "Gefunden"},
    "add_tool":         {"en": "+ Add Tool", "de": "+ Tool hinzufügen"},
    "add_guide":        {"en": "+ Add Guide", "de": "+ Anleitung hinzufügen"},
    "credits":          {"en": "Credits", "de": "Credits"},
    "grid_view":        {"en": "Grid", "de": "Kacheln"},
    "list_view":        {"en": "List", "de": "Liste"},
    "formats":          {"en": "Formats", "de": "Formate"},
    "description":      {"en": "Description", "de": "Beschreibung"},
    "path":             {"en": "Path", "de": "Pfad"},
    "download":         {"en": "Download", "de": "Download"},
    "related_guides":   {"en": "Related Guides", "de": "Zugehörige Anleitungen"},
    "open_full":        {"en": "Open Full View", "de": "Vollansicht öffnen"},
    "close":            {"en": "Close", "de": "Schließen"},
    "preview":          {"en": "Preview", "de": "Vorschau"},
    "no_results":       {"en": "No results found.", "de": "Keine Ergebnisse gefunden."},
    "file_format_info": {"en": "File Format Info", "de": "Dateiformat-Info"},
    "tool_name":        {"en": "Tool Name", "de": "Tool-Name"},
    "tool_path":        {"en": "Tool Path (.py or .exe)", "de": "Tool-Pfad (.py oder .exe)"},
    "tool_formats":     {"en": "Supported Formats (comma-separated, e.g. .lan,.par)", "de": "Unterstützte Formate (kommagetrennt, z.B. .lan,.par)"},
    "tool_desc_en":     {"en": "Description (English)", "de": "Beschreibung (Englisch)"},
    "tool_desc_de":     {"en": "Description (German)", "de": "Beschreibung (Deutsch)"},
    "tool_default_path":{"en": "Default Path (where it's usually located)", "de": "Standard-Pfad (wo es normalerweise liegt)"},
    "tool_download":    {"en": "Download Link (optional)", "de": "Download-Link (optional)"},
    "guide_title":      {"en": "Guide Title", "de": "Anleitung Titel"},
    "guide_title_en":   {"en": "Title (English)", "de": "Titel (Englisch)"},
    "guide_title_de":   {"en": "Title (German)", "de": "Titel (Deutsch)"},
    "guide_content_en": {"en": "Content (English)", "de": "Inhalt (Englisch)"},
    "guide_content_de": {"en": "Content (German)", "de": "Inhalt (Deutsch)"},
    "guide_tags":       {"en": "Tags (comma-separated)", "de": "Tags (kommagetrennt)"},
    "guide_tools":      {"en": "Related Tools (comma-separated tool names)", "de": "Zugehörige Tools (kommagetrennt)"},
    "browse":           {"en": "Browse...", "de": "Durchsuchen..."},
    "save":             {"en": "Save", "de": "Speichern"},
    "cancel":           {"en": "Cancel", "de": "Abbrechen"},
    "or_file":          {"en": "Or load from file (.txt / .md):", "de": "Oder aus Datei laden (.txt / .md):"},
    "select_all":       {"en": "— All —", "de": "— Alle —"},
    "builtin":          {"en": "Built-in", "de": "Eingebaut"},
    "custom":           {"en": "Custom", "de": "Benutzerdefiniert"},
    "by":               {"en": "by", "de": "von"},
    "set_path":         {"en": "Set Path", "de": "Pfad setzen"},
    "reset_path":       {"en": "Reset", "de": "Zurücksetzen"},
    "font_size":        {"en": "Font Size", "de": "Schriftgröße"},
    "language":         {"en": "Language", "de": "Sprache"},
    "view_mode":        {"en": "View Mode", "de": "Ansichtsmodus"},
    "guides_folder":    {"en": "Guides Folder", "de": "Anleitungen-Ordner"},
    "tool_paths_mgmt":  {"en": "Tool Paths", "de": "Tool-Pfade"},
    "general":          {"en": "General", "de": "Allgemein"},
    "guide_not_found":  {"en": "Guide file not found. Place guide .txt files in the 'guides' folder next to this hub.",
                         "de": "Guide-Datei nicht gefunden. Guide .txt-Dateien im 'guides'-Ordner neben diesem Hub ablegen."},
    "open_folder":      {"en": "Open Folder", "de": "Ordner öffnen"},
}

# ============================================================
# FILE FORMAT DATABASE
# ============================================================
FILE_FORMATS = {
    ".wd": {
        "en": "WD Archive — Two Worlds mod container format. Contains packed game files (maps, physics, textures). Compressed with zlib, directory at end of file. Version 0x200 for TW1. GUID identifies each archive. .phx files must NOT be compressed inside.",
        "de": "WD-Archiv — Two Worlds Mod-Containerformat. Enthält gepackte Spieldateien (Maps, Physik, Texturen). Zlib-komprimiert, Verzeichnis am Dateiende. Version 0x200 für TW1. GUID identifiziert jedes Archiv. .phx-Dateien dürfen NICHT komprimiert werden.",
    },
    ".lan": {
        "en": "LAN Language File — Binary file containing all localized game text. Three sections: translations (16,194 entries), aliases (215 redirects), quest dialog trees (583 quests, 9,799 entries). UTF-16-LE encoded strings with 'translate' prefix keys.",
        "de": "LAN-Sprachdatei — Binärdatei mit allen lokalisierten Spieltexten. Drei Abschnitte: Übersetzungen (16.194 Einträge), Aliase (215 Weiterleitungen), Quest-Dialogbäume (583 Quests, 9.799 Einträge). UTF-16-LE kodierte Strings mit 'translate'-Präfix.",
    },
    ".par": {
        "en": "PAR Parameter File — Central binary database containing all item definitions, NPC stats, creatures, skills, weapons, armor. Compressed with zlib. Contains groups with typed entries (int32, float, uint32, string + arrays). GUID in header.",
        "de": "PAR-Parameterdatei — Zentrale Binär-Datenbank mit allen Item-Definitionen, NPC-Stats, Kreaturen, Skills, Waffen, Rüstungen. Zlib-komprimiert. Enthält Gruppen mit typisierten Einträgen (int32, float, uint32, string + Arrays). GUID im Header.",
    },
    ".lnd": {
        "en": "LND Level/Map File — Contains terrain heightmap, textures, object placements, NPC spawns, and all map tile data. Zlib-compressed. Each tile is 128x128. Files named Map_F01.lnd etc. Editor saves with 's' suffix (Map_F01s.lnd).",
        "de": "LND Level/Map-Datei — Enthält Terrain-Heightmap, Texturen, Objekt-Platzierungen, NPC-Spawns und alle Map-Tile-Daten. Zlib-komprimiert. Jedes Tile ist 128x128. Dateien heißen Map_F01.lnd etc. Editor speichert mit 's'-Suffix (Map_F01s.lnd).",
    },
    ".vdf": {
        "en": "VDF 3D Model File — Two Worlds proprietary 3D model format. Contains mesh geometry, textures, animations. Created by Maya plugins or TreesGenerator. Can be used as terrain stamps in the editor.",
        "de": "VDF 3D-Modelldatei — Two Worlds proprietäres 3D-Modellformat. Enthält Mesh-Geometrie, Texturen, Animationen. Wird von Maya-Plugins oder TreesGenerator erstellt. Kann als Terrain-Stempel im Editor verwendet werden.",
    },
    ".phx": {
        "en": "PHX Physics File — Collision data for map tiles. Generated by cooking PhysX in the editor (4 console commands). Must NOT be compressed when packed into .wd archives or the game will crash.",
        "de": "PHX-Physikdatei — Kollisionsdaten für Map-Tiles. Wird durch PhysX-Kochen im Editor erzeugt (4 Konsolenbefehle). Darf beim Packen in .wd-Archive NICHT komprimiert werden, sonst crasht das Spiel.",
    },
    ".lhc": {
        "en": "LHC LevelHeaders Cache — Index file containing header information of all map files. Generated by LevelHeadersCacheGen.bat / MeshParamsGen.exe. Must be regenerated after every map change.",
        "de": "LHC LevelHeaders-Cache — Indexdatei mit Header-Informationen aller Map-Dateien. Wird durch LevelHeadersCacheGen.bat / MeshParamsGen.exe erzeugt. Muss nach jeder Map-Änderung neu generiert werden.",
    },
    ".idx": {
        "en": "IDX Quest Data (SOAP-XML) — Full quest data export from WhizzEdit. Contains complete quest trees, NPC definitions, dialog structures, quest logic (GIVER, FC, AOQ, ACTION, REWARD). Recommended format for quest editing.",
        "de": "IDX Quest-Daten (SOAP-XML) — Vollständiger Quest-Datenexport aus WhizzEdit. Enthält komplette Quest-Bäume, NPC-Definitionen, Dialog-Strukturen, Quest-Logik (GIVER, FC, AOQ, ACTION, REWARD). Empfohlenes Format zum Quest-Editieren.",
    },
    ".qtx": {
        "en": "QTX Quest Logic (Plaintext) — Compiled quest logic for the game engine. Contains NPC definitions, quest parameters, actions, rewards. No dialog text (that's in .lan). OBJECTS field can carry item drop lists.",
        "de": "QTX Quest-Logik (Klartext) — Kompilierte Quest-Logik für die Game-Engine. Enthält NPC-Definitionen, Quest-Parameter, Aktionen, Belohnungen. Kein Dialog-Text (der ist in .lan). OBJECTS-Feld kann Item-Drop-Listen enthalten.",
    },
    ".shf": {
        "en": "SHF WhizzEdit Project — Binary .NET BinaryFormatter format. WhizzEdit's native project files (one per folder). Contains 23,329 strings. Read-only in our tools — use .idx for editing.",
        "de": "SHF WhizzEdit-Projekt — Binäres .NET BinaryFormatter-Format. WhizzEdits native Projektdateien (eine pro Ordner). Enthält 23.329 Strings. Nur lesbar in unseren Tools — .idx zum Editieren verwenden.",
    },
    ".bmp": {
        "en": "BMP Minimap Image — Minimap bitmap for each map tile. Saved alongside .lnd files. Must be renamed (remove 's' suffix) when creating mods, just like .lnd and .phx files.",
        "de": "BMP Minimap-Bild — Minimap-Bitmap für jedes Map-Tile. Wird neben .lnd-Dateien gespeichert. Muss beim Mod-Erstellen umbenannt werden ('s'-Suffix entfernen), genau wie .lnd und .phx.",
    },
}

# ============================================================
# BUILT-IN TOOLS
# ============================================================
BUILTIN_TOOLS = [
    {
        "id": "cmd_injector",
        "name": "TW Editor CMD Injector",
        "icon": "\u2328",
        "desc_en": "Injects commands into the Two Worlds Editor console. Categorized command database with search, multi-command execution via .txt lists, auto-detection of editor window.",
        "desc_de": "Injiziert Befehle in die Two Worlds Editor-Konsole. Kategorisierte Command-Datenbank mit Suche, Multi-Command-Ausführung über .txt-Listen, Auto-Erkennung des Editor-Fensters.",
        "filename": "tw_editor_cmd_injector.py",
        "formats": [],
        "type": "python",
        "download": "https://github.com/MedievalDev/TwoWorldsEditor_Command_Injector",
        "guide_ids": ["editor_beginner_guide", "physx_cooking"],
    },
    {
        "id": "lan_viewer",
        "name": "TW1 LAN Viewer",
        "icon": "\U0001f4ac",
        "desc_en": "View and search .lan language files. Chat-style dialog view, full-text search, compare mode. Part of the Dialog Viewer/Editor repository.",
        "desc_de": "Anzeigen und Durchsuchen von .lan-Sprachdateien. Chat-Ansicht, Volltextsuche, Vergleichsmodus. Teil des Dialog Viewer/Editor Repositories.",
        "filename": "tw1_lan_viewer.py",
        "formats": [".lan"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Twor-Worlds-Dialog-Viewer-Editor",
        "guide_ids": ["format_overview"],
    },
    {
        "id": "quest_editor",
        "name": "TW1 Quest Editor",
        "icon": "\U0001f4dc",
        "desc_en": "Edit .idx/.qtx quest data and .shf WhizzEdit projects. Quest tree editing, NPC assignments, dialog structures. Part of the Dialog Viewer/Editor repository.",
        "desc_de": "Bearbeiten von .idx/.qtx Quest-Daten und .shf WhizzEdit-Projekten. Quest-Baum-Bearbeitung, NPC-Zuweisungen, Dialog-Strukturen. Teil des Dialog Viewer/Editor Repositories.",
        "filename": "tw1_quest_editor.py",
        "formats": [".idx", ".qtx", ".shf"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Twor-Worlds-Dialog-Viewer-Editor",
        "guide_ids": ["format_overview"],
    },
    {
        "id": "par_tool",
        "name": "TW1 PAR Tool",
        "icon": "\U0001f4ca",
        "desc_en": "Convert TwoWorlds.par between binary and JSON. Tree view of all groups/entries, inline editing, GUID management, hex view, file comparison. Full import/export roundtrip.",
        "desc_de": "Konvertiert TwoWorlds.par zwischen Binär und JSON. Baumansicht aller Gruppen/Einträge, Inline-Editing, GUID-Verwaltung, Hex-Ansicht, Dateivergleich. Vollständiger Import/Export.",
        "filename": "tw1param_gui.py",
        "formats": [".par"],
        "type": "python",
        "download": "https://github.com/MedievalDev/TwoWorlds_PAR_Editor",
        "guide_ids": ["format_overview"],
    },
    {
        "id": "vdf_tool",
        "name": "TW1 VDF In/Export Tool",
        "icon": "\U0001f4d0",
        "desc_en": "Import and export Two Worlds .vdf 3D model files. View mesh geometry, textures and animations. Convert between VDF and standard formats.",
        "desc_de": "Import und Export von Two Worlds .vdf 3D-Modelldateien. Mesh-Geometrie, Texturen und Animationen anzeigen. Konvertierung zwischen VDF und Standardformaten.",
        "filename": "tw1_vdf_tool.py",
        "formats": [".vdf"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Two-Worlds-VDF-In-Export-Tool",
        "guide_ids": [],
    },
    {
        "id": "lnd_viewer",
        "name": "TW1 LND Viewer",
        "icon": "\U0001f5fa",
        "desc_en": "View Two Worlds .lnd level/map files. Inspect terrain heightmaps, textures, object placements and map tile data.",
        "desc_de": "Two Worlds .lnd Level/Map-Dateien anzeigen. Terrain-Heightmaps, Texturen, Objekt-Platzierungen und Map-Tile-Daten inspizieren.",
        "filename": "tw1_lnd_viewer.py",
        "formats": [".lnd"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Twor-Worlds-LND-Viewer",
        "guide_ids": ["editor_beginner_guide"],
    },
    {
        "id": "modding_guide",
        "name": "TW1 Modding Guide",
        "icon": "\U0001f4d6",
        "desc_en": "Interactive step-by-step guide for new TW1 modders. Walks through SDK setup, editor usage, map creation, PhysX cooking, mod packaging and activation.",
        "desc_de": "Interaktiver Schritt-für-Schritt-Guide für neue TW1-Modder. Führt durch SDK-Setup, Editor-Benutzung, Map-Erstellung, PhysX-Kochen, Mod-Verpackung und Aktivierung.",
        "filename": "tw1_modding_guide.py",
        "formats": [],
        "type": "python",
        "download": "https://github.com/MedievalDev/Two-Worlds-Modding-Guid",
        "guide_ids": ["map_to_mod_guide", "editor_beginner_guide"],
    },
    {
        "id": "tw_editor",
        "name": "TwoWorlds Editor",
        "icon": "\U0001f3ae",
        "desc_en": "The official Two Worlds SDK map/level editor. Create and edit map tiles, place objects, NPCs, terrain, and structures. Console accessible via 'C' key.",
        "desc_de": "Der offizielle Two Worlds SDK Map/Level-Editor. Map-Tiles erstellen und bearbeiten, Objekte, NPCs, Terrain und Strukturen platzieren. Konsole über 'C'-Taste erreichbar.",
        "filename": "TwoWorldsEditor.exe",
        "search_paths": ["..", "../Tools"],
        "formats": [".lnd"],
        "type": "exe",
        "download": "https://www.moddb.com/games/two-worlds/downloads",
        "guide_ids": ["editor_beginner_guide", "dungeon_guide_part1", "dungeon_guide_part2"],
    },
    {
        "id": "whizzedit",
        "name": "WhizzEdit",
        "icon": "\U0001f9d9",
        "desc_en": "Reality Pump's quest authoring tool from the SDK. Views quest trees, dialog structures, NPC assignments. Barely runs on modern systems. Use our LAN Viewer and Quest Editor instead.",
        "desc_de": "Reality Pumps Quest-Erstellungstool aus dem SDK. Zeigt Quest-Bäume, Dialog-Strukturen, NPC-Zuweisungen. Läuft kaum auf modernen Systemen. Lieber unseren LAN Viewer und Quest Editor nutzen.",
        "filename": "WhizzEdit.exe",
        "search_paths": ["..", "../Tools"],
        "formats": [".shf", ".idx"],
        "type": "exe",
        "download": "https://www.moddb.com/games/two-worlds/downloads",
        "guide_ids": [],
    },
    {
        "id": "mod_selector",
        "name": "Mod Selector (Buglord)",
        "icon": "\u2705",
        "desc_en": "Buglord's tool to toggle mods on/off via Windows registry. Place in game directory, run, press Enter to switch mods between active (green) and inactive (red).",
        "desc_de": "Buglords Tool zum Aktivieren/Deaktivieren von Mods über die Windows-Registry. Ins Spielverzeichnis legen, starten, Enter drücken zum Umschalten zwischen aktiv (grün) und inaktiv (rot).",
        "filename": "TwoWorlds1 Mod Selector_ madebyBuglord.exe",
        "search_paths": [],
        "formats": [".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/Two-Worlds-Modding-Guid/blob/main/Guid/TwoWorlds1%20Mod%20Selector_%20madebyBuglord.exe",
        "guide_ids": ["map_to_mod_guide"],
    },
    {
        "id": "wd_repacker",
        "name": "WD Repacker (Buglord)",
        "icon": "\U0001f4e6",
        "desc_en": "Buglord's GUI tool for packing/unpacking .wd archives. IMPORTANT: Select the FOLDER as source, not a .wd file! Correctly handles .phx files (uncompressed).",
        "desc_de": "Buglords GUI-Tool zum Packen/Entpacken von .wd-Archiven. WICHTIG: Den ORDNER als Source wählen, nicht eine .wd-Datei! Behandelt .phx-Dateien korrekt (unkomprimiert).",
        "filename": "Tw1WDRepacker.exe",
        "search_paths": [],
        "formats": [".wd"],
        "type": "exe",
        "download": "https://www.moddb.com/games/two-worlds/downloads",
        "guide_ids": ["map_to_mod_guide"],
    },
]

# ============================================================
# BUILT-IN GUIDES (with external file loading)
# ============================================================
BUILTIN_GUIDES = [
    {
        "id": "editor_beginner_guide",
        "title_en": "Editor Beginner Guide",
        "title_de": "Editor Einsteiger-Handbuch",
        "icon": "\U0001f3ae",
        "tags": ["editor", "shortcuts", "objects", "markers", "terrain", "textures", "console", "beginner"],
        "tool_ids": ["cmd_injector", "tw_editor", "modding_guide"],
        "file_en": "editor_beginner_guide_en.txt",
        "file_de": "editor_beginner_guide_de.txt",
        "fallback_en": "Complete editor reference with Quick Start section. Place 'editor_beginner_guide_en.txt' in the guides/ folder.",
        "fallback_de": "Komplette Editor-Referenz mit Schnellstart-Abschnitt. Die Datei 'editor_beginner_guide_de.txt' im guides/-Ordner ablegen.",
    },
    {
        "id": "dungeon_guide_part1",
        "title_en": "Dungeon Guide Part 1 — Manual Method",
        "title_de": "Dungeon-Guide Teil 1 — Manuelle Methode",
        "icon": "\U0001f5ff",
        "tags": ["dungeon", "underground", "cave", "entrance", "markers", "manual"],
        "tool_ids": ["tw_editor", "cmd_injector"],
        "file_en": "dungeon_guide_part1_en.txt",
        "file_de": "dungeon_guide_part1_de.txt",
        "fallback_en": "Manual dungeon creation using the main editor. Place 'dungeon_guide_part1_en.txt' in the guides/ folder.",
        "fallback_de": "Manuelle Dungeon-Erstellung im Haupteditor. Die Datei 'dungeon_guide_part1_de.txt' im guides/-Ordner ablegen.",
    },
    {
        "id": "dungeon_guide_part2",
        "title_en": "Dungeon Guide Part 2 — SDK Dungeon Editor",
        "title_de": "Dungeon-Guide Teil 2 — SDK Dungeon-Editor",
        "icon": "\U0001f3f0",
        "tags": ["dungeon", "underground", "cave", "sdk", "blocks", "dungeon editor"],
        "tool_ids": ["tw_editor"],
        "file_en": "dungeon_guide_part2_en.txt",
        "file_de": "dungeon_guide_part2_de.txt",
        "fallback_en": "Block-based dungeon creation with the SDK tool. Place 'dungeon_guide_part2_en.txt' in the guides/ folder.",
        "fallback_de": "Blockbasierte Dungeon-Erstellung mit dem SDK-Tool. Die Datei 'dungeon_guide_part2_de.txt' im guides/-Ordner ablegen.",
    },
    {
        "id": "map_to_mod_guide",
        "title_en": "Map-to-Mod Conversion Guide",
        "title_de": "Map-zu-Mod Konvertierungsguide",
        "icon": "\U0001f4e6",
        "tags": ["mod", "wd", "pack", "physx", "registry", "levelheaders", "rename", "conversion"],
        "tool_ids": ["cmd_injector", "modding_guide", "mod_selector", "wd_repacker"],
        "file_en": "map_to_mod_guide_en.txt",
        "file_de": "map_to_mod_guide_de.txt",
        "fallback_en": "Complete mod conversion workflow. Place 'map_to_mod_guide_en.txt' in the guides/ folder.",
        "fallback_de": "Kompletter Mod-Konvertierungs-Workflow. Die Datei 'map_to_mod_guide_de.txt' im guides/-Ordner ablegen.",
    },
    {
        "id": "physx_cooking",
        "title_en": "PhysX Cooking Reference",
        "title_de": "PhysX-Kochen Referenz",
        "icon": "\U0001f525",
        "tags": ["physx", "physics", "cooking", "console", "commands", "phx"],
        "tool_ids": ["cmd_injector", "tw_editor"],
        "content_en": """PHYSX COOKING REFERENCE
=======================

How to generate collision/physics data for your map.

THE 4 COMMANDS
--------------
Open the editor console (C key) and enter in this order:

  1. editor.cookphysx.mode geomipmap
  2. editor.cookphysx.strength = 1.0
  3. editor.cookphysx.overwrite = 1
  4. editor.cookphysx.pc out

Command 1: Sets the cooking mode to geomipmap (terrain mesh)
Command 2: Sets physics strength to maximum (1.0)
Command 3: Enables overwriting existing .phx files
Command 4: Starts the actual cooking process - wait until done!

OUTPUT
------
The cooked .phx file is written to:
  %USERPROFILE%\\Saved Games\\Two Worlds Saves\\Levels\\Physic\\

File will be named after your map: Map_F01s.phx

CRITICAL WARNINGS
-----------------
* The .phx file must NEVER be compressed in a .wd archive
  -> Old/other WD packers compress .phx files -> game CRASH
  -> Only use Buglord's wdio.py or his WD Repacker
* Without physics data: no collision on terrain (you fall through)
* Must be regenerated after ANY terrain changes
* The cooking process can take a while for large/complex maps""",
        "content_de": """PHYSX-KOCHEN REFERENZ
=====================

Wie man Kollisions-/Physikdaten fuer deine Map generiert.

DIE 4 BEFEHLE
-------------
Editor-Konsole oeffnen (C-Taste) und in dieser Reihenfolge eingeben:

  1. editor.cookphysx.mode geomipmap
  2. editor.cookphysx.strength = 1.0
  3. editor.cookphysx.overwrite = 1
  4. editor.cookphysx.pc out

Befehl 1: Setzt den Kochmodus auf geomipmap (Terrain-Mesh)
Befehl 2: Setzt Physik-Staerke auf Maximum (1.0)
Befehl 3: Aktiviert Ueberschreiben vorhandener .phx-Dateien
Befehl 4: Startet den Kochprozess - warten bis fertig!

AUSGABE
-------
Die gekochte .phx-Datei wird geschrieben nach:
  %USERPROFILE%\\Saved Games\\Two Worlds Saves\\Levels\\Physic\\

Dateiname nach deiner Map: Map_F01s.phx

KRITISCHE WARNUNGEN
-------------------
* Die .phx-Datei darf in einem .wd-Archiv NIEMALS komprimiert werden
  -> Alte/andere WD-Packer komprimieren .phx -> Spiel CRASHT
  -> Nur Buglords wdio.py oder seinen WD Repacker verwenden
* Ohne Physikdaten: keine Kollision auf dem Terrain (man faellt durch)
* Muss nach JEDER Terrain-Aenderung neu generiert werden
* Der Kochprozess kann bei grossen/komplexen Maps eine Weile dauern""",
    },
    {
        "id": "format_overview",
        "title_en": "File Format Overview",
        "title_de": "Dateiformat-Uebersicht",
        "icon": "\U0001f4c4",
        "tags": ["format", "wd", "lan", "par", "lnd", "phx", "idx", "qtx", "shf", "lhc", "bmp", "vdf"],
        "tool_ids": ["lan_viewer", "quest_editor", "par_tool", "vdf_tool", "lnd_viewer", "wd_repacker"],
        "content_en": """FILE FORMAT OVERVIEW
====================

All file formats used in Two Worlds 1 modding.

GAME DATA FILES
---------------
.wd     WD Archive - Mod container, zlib-compressed, GUID-identified
.par    Parameter Database - Items, NPCs, skills, stats (binary)
.lnd    Level/Map - Terrain, objects, spawns per tile (128x128)
.phx    Physics - Collision data, must NOT be compressed in .wd
.lhc    LevelHeaders Cache - Map index, regenerate after changes
.bmp    Minimap - Bitmap image per map tile
.vdf    3D Model - Mesh geometry, textures, animations

QUEST & DIALOG FILES
--------------------
.lan    Language - All localized text (16,194 translations, binary)
.idx    Quest Data - SOAP-XML, full quest trees (recommended for editing)
.qtx    Quest Logic - Plaintext, compiled for engine (no dialog text)
.shf    WhizzEdit Project - .NET binary, read-only in our tools

PIPELINE
--------
WhizzEdit (.shf) -> Export -> .idx (XML) -> Compile -> .qtx + .lan
Editor -> Save -> .lnd + .bmp -> Cook -> .phx -> Pack -> .wd

WHICH TOOL FOR WHICH FILE?
---------------------------
.lan    -> TW1 LAN Viewer
.idx    -> TW1 Quest Editor
.qtx    -> TW1 Quest Editor
.shf    -> TW1 Quest Editor (read-only)
.par    -> TW1 PAR Tool
.vdf    -> TW1 VDF In/Export Tool
.lnd    -> TW1 LND Viewer / TwoWorlds Editor
.wd     -> WD Repacker / Mod Selector
.phx    -> Generated by editor (PhysX cooking)
.lhc    -> Generated by LevelHeadersCacheGen.bat
.bmp    -> Any image viewer""",
        "content_de": """DATEIFORMAT-UEBERSICHT
======================

Alle Dateiformate beim Two Worlds 1 Modding.

SPIELDATEN-DATEIEN
------------------
.wd     WD-Archiv - Mod-Container, zlib-komprimiert, GUID-identifiziert
.par    Parameter-Datenbank - Items, NPCs, Skills, Stats (binaer)
.lnd    Level/Map - Terrain, Objekte, Spawns pro Tile (128x128)
.phx    Physik - Kollisionsdaten, darf in .wd NICHT komprimiert werden
.lhc    LevelHeaders-Cache - Map-Index, nach Aenderungen neu generieren
.bmp    Minimap - Bitmap-Bild pro Map-Tile
.vdf    3D-Modell - Mesh-Geometrie, Texturen, Animationen

QUEST- & DIALOG-DATEIEN
-----------------------
.lan    Sprache - Alle lokalisierten Texte (16.194 Uebersetzungen, binaer)
.idx    Quest-Daten - SOAP-XML, volle Quest-Baeume (empfohlen zum Editieren)
.qtx    Quest-Logik - Klartext, kompiliert fuer Engine (kein Dialog-Text)
.shf    WhizzEdit-Projekt - .NET-Binaer, nur lesbar in unseren Tools

PIPELINE
--------
WhizzEdit (.shf) -> Export -> .idx (XML) -> Kompilieren -> .qtx + .lan
Editor -> Speichern -> .lnd + .bmp -> Kochen -> .phx -> Packen -> .wd

WELCHES TOOL FUER WELCHE DATEI?
---------------------------------
.lan    -> TW1 LAN Viewer
.idx    -> TW1 Quest Editor
.qtx    -> TW1 Quest Editor
.shf    -> TW1 Quest Editor (nur lesen)
.par    -> TW1 PAR Tool
.vdf    -> TW1 VDF In/Export Tool
.lnd    -> TW1 LND Viewer / TwoWorlds Editor
.wd     -> WD Repacker / Mod Selector
.phx    -> Vom Editor generiert (PhysX-Kochen)
.lhc    -> Von LevelHeadersCacheGen.bat generiert
.bmp    -> Jeder Bildbetrachter""",
    },
]

# ============================================================
# CREDITS
# ============================================================
CREDITS = {
    "en": """CREDITS
=======

TOOLS & REVERSE ENGINEERING
  Buglord (Discord: buglord)
    wdio.py (WD packer/unpacker), Mod Selector, WD Repacker,
    WD archive format documentation, registry mechanism,
    LAN format specification, QTX format specification

MODDING GUIDES & TESTING
  JadetheReaper (Discord: .jadetheripper)
    Map Test EX.wd, Map-to-Mod conversion process documentation

  Smoothness (Discord)
    Editor tutorials, dungeon/underground creation workflow,
    game object behavior documentation, editor shortcuts

DEVELOPMENT
  MedievalDev
    TW1 Modding Hub, CMD Injector, LAN Viewer, Quest Editor,
    PAR Tool, VDF Tool, LND Viewer, Modding Guide Tool

DOCUMENTATION
  MedievalDev & Claude (Anthropic)
    Editor Beginner Guide, Dungeon Guide Part 1 & 2,
    Map-to-Mod Conversion Guide (EN + DE)

ORIGINAL GAME & SDK
  Reality Pump Studios - Two Worlds (2007)
  TopWare Interactive - Publisher""",
    "de": """CREDITS
=======

TOOLS & REVERSE ENGINEERING
  Buglord (Discord: buglord)
    wdio.py (WD-Packer/Entpacker), Mod Selector, WD Repacker,
    WD-Archivformat-Dokumentation, Registry-Mechanismus,
    LAN-Format-Spezifikation, QTX-Format-Spezifikation

MODDING-ANLEITUNGEN & TESTS
  JadetheReaper (Discord: .jadetheripper)
    Map Test EX.wd, Map-zu-Mod Konvertierungsprozess-Dokumentation

  Smoothness (Discord)
    Editor-Tutorials, Dungeon/Untergrund-Erstellungs-Workflow,
    Spielobjekt-Verhaltensdokumentation, Editor-Tastenkuerzel

ENTWICKLUNG
  MedievalDev
    TW1 Modding Hub, CMD Injector, LAN Viewer, Quest Editor,
    PAR Tool, VDF Tool, LND Viewer, Modding Guide Tool

DOKUMENTATION
  MedievalDev & Claude (Anthropic)
    Editor Einsteiger-Handbuch, Dungeon-Guide Teil 1 & 2,
    Map-zu-Mod Konvertierungsguide (EN + DE)

ORIGINALSPIEL & SDK
  Reality Pump Studios - Two Worlds (2007)
  TopWare Interactive - Publisher""",
}

# ============================================================
# CONFIG MANAGEMENT
# ============================================================
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"lang": "en", "view_mode": "grid", "font_size": 10,
            "guides_dir": GUIDES_DIR,
            "user_tools": [], "user_guides": [], "tool_paths": {}}

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Config save error: {e}")


# ============================================================
# GUIDE FILE LOADER
# ============================================================
def load_guide_content(guide, lang, guides_dir):
    """Load guide content from external file or fallback to embedded."""
    file_key = f"file_{lang}"
    content_key = f"content_{lang}"

    # Try external file first
    if file_key in guide:
        filepath = os.path.join(guides_dir, guide[file_key])
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass

    # Fallback to embedded content
    if content_key in guide:
        return guide[content_key]

    # Fallback text
    fallback_key = f"fallback_{lang}"
    if fallback_key in guide:
        return guide[fallback_key]

    # Final fallback
    return LANG.get("guide_not_found", {}).get(lang, "Guide file not found.")


# ============================================================
# MAIN APPLICATION
# ============================================================
class ModdingHub:
    def __init__(self, root):
        self.root = root
        self.cfg = load_config()
        self.lang = self.cfg.get("lang", "en")
        self.view_mode = self.cfg.get("view_mode", "grid")
        self.font_size = self.cfg.get("font_size", 10)
        self.guides_dir = self.cfg.get("guides_dir", GUIDES_DIR)

        # Auto-detect guides folder if default doesn't exist
        if not os.path.isdir(self.guides_dir):
            for alt in ["guides", "Guids", "Guides", "guids"]:
                alt_path = os.path.join(SCRIPT_DIR, alt)
                if os.path.isdir(alt_path):
                    self.guides_dir = alt_path
                    break

        # DPI awareness BEFORE geometry calculations
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.root.title(self.t("title"))

        # Auto-size to screen: 50% width, 50% height, centered
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = int(screen_w * 0.5)
        win_h = int(screen_h * 0.65)
        x = (screen_w - win_w) // 2
        y = max((screen_h - win_h) // 2 - 20, 0)
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.minsize(800, 400)
        self.root.configure(bg=BG)

        self._setup_styles()
        self._build_toolbar()
        self._build_main()
        self._build_statusbar()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def t(self, key):
        entry = LANG.get(key, {})
        return entry.get(self.lang, entry.get("en", key))

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG2, foreground=FG, padding=[12, 6],
                         font=("Segoe UI", 11))
        style.map("TNotebook.Tab",
                   background=[("selected", BG3)],
                   foreground=[("selected", ACCENT)])

    # ────────────────────────────────────────────────────────
    # TOOLBAR
    # ────────────────────────────────────────────────────────
    def _build_toolbar(self):
        tb = tk.Frame(self.root, bg=BG2, padx=10, pady=8)
        tb.pack(fill="x")

        tk.Label(tb, text="\U0001f3ae TW1 Modding Hub", font=("Segoe UI", 14, "bold"),
                 bg=BG2, fg=ACCENT).pack(side="left")

        right = tk.Frame(tb, bg=BG2)
        right.pack(side="right")

        # Language toggle
        self.lang_btn = tk.Button(right, text="DE" if self.lang == "en" else "EN",
                                   font=("Segoe UI", 9, "bold"), bg=BG3, fg=FG,
                                   relief="flat", padx=8, pady=2, cursor="hand2",
                                   command=self._toggle_lang)
        self.lang_btn.pack(side="right", padx=4)
        tk.Label(right, text="\U0001f310", font=("Segoe UI", 11), bg=BG2, fg=FG_DIM).pack(side="right")

        # Settings button
        tk.Button(right, text="\u2699 " + self.t("settings"), font=("Segoe UI", 9), bg=BG3, fg=FG,
                  relief="flat", padx=8, pady=2, cursor="hand2",
                  command=self._show_settings).pack(side="right", padx=4)

        # View toggle
        self.view_btn = tk.Button(right, text=self.t("list_view") if self.view_mode == "grid" else self.t("grid_view"),
                                   font=("Segoe UI", 9), bg=BG3, fg=FG,
                                   relief="flat", padx=8, pady=2, cursor="hand2",
                                   command=self._toggle_view)
        self.view_btn.pack(side="right", padx=4)

        # Credits button
        tk.Button(right, text=self.t("credits"), font=("Segoe UI", 9), bg=BG3, fg=FG_DIM,
                  relief="flat", padx=8, pady=2, cursor="hand2",
                  command=self._show_credits).pack(side="right", padx=4)

        # Search bar
        search_frame = tk.Frame(tb, bg=SEARCH_BG, highlightbackground=BORDER,
                                 highlightthickness=1, padx=6, pady=3)
        search_frame.pack(side="left", padx=(20, 0), fill="x", expand=True)

        tk.Label(search_frame, text="\U0001f50d", font=("Segoe UI", 11), bg=SEARCH_BG, fg=FG_DIM).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                      font=("Segoe UI", 11), bg=SEARCH_BG, fg=FG,
                                      insertbackground=FG, relief="flat", border=0)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=6)
        self.search_entry.insert(0, self.t("search"))
        self.search_entry.config(fg=FG_DIM)
        self.search_entry.bind("<FocusIn>", self._search_focus_in)
        self.search_entry.bind("<FocusOut>", self._search_focus_out)
        self.search_entry.bind("<KeyRelease>", self._on_search)

    def _search_focus_in(self, e):
        if self.search_entry.get() in [LANG["search"]["en"], LANG["search"]["de"]]:
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg=FG)

    def _search_focus_out(self, e):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, self.t("search"))
            self.search_entry.config(fg=FG_DIM)

    def _on_search(self, e=None):
        query = self.search_var.get().strip().lower()
        if query in [self.t("search").lower(), ""] or not query:
            self._show_tools()
            self._show_guides()
            return
        self._show_tools(query)
        self._show_guides(query)

    # ────────────────────────────────────────────────────────
    # MAIN AREA
    # ────────────────────────────────────────────────────────
    def _build_main(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=(4, 0))

        self.tools_frame = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tools_frame, text=f"  \U0001f527 {self.t('tools')}  ")

        self.guides_outer = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.guides_outer, text=f"  \U0001f4d6 {self.t('guides')}  ")

        self._build_tools_tab()
        self._build_guides_tab()

    # ────────────────────────────────────────────────────────
    # TOOLS TAB
    # ────────────────────────────────────────────────────────
    def _build_tools_tab(self):
        self.tools_canvas = tk.Canvas(self.tools_frame, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.tools_frame, orient="vertical", command=self.tools_canvas.yview)
        self.tools_inner = tk.Frame(self.tools_canvas, bg=BG)

        self.tools_inner.bind("<Configure>", lambda e: self.tools_canvas.configure(scrollregion=self.tools_canvas.bbox("all")))
        self._tools_win_id = self.tools_canvas.create_window((0, 0), window=self.tools_inner, anchor="nw")
        self.tools_canvas.configure(yscrollcommand=scrollbar.set)

        # Keep inner frame width = canvas width (so cards fill the space)
        def _on_canvas_resize(e):
            self.tools_canvas.itemconfig(self._tools_win_id, width=e.width)
        self.tools_canvas.bind("<Configure>", _on_canvas_resize)

        self.tools_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(e):
            self.tools_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        self.tools_canvas.bind_all("<MouseWheel>", _on_mousewheel, add="+")

        self._show_tools()

    def _show_tools(self, query=None):
        for w in self.tools_inner.winfo_children():
            w.destroy()

        all_tools = self._get_all_tools()

        if query:
            filtered = []
            for tool in all_tools:
                searchable = f"{tool['name']} {tool.get('desc_'+self.lang, tool.get('desc_en',''))} {' '.join(tool.get('formats',[]))}".lower()
                if query in searchable:
                    filtered.append(tool)
            for fmt, desc in FILE_FORMATS.items():
                if query in fmt.lower() or query in desc.get(self.lang, desc.get("en", "")).lower():
                    for tool in all_tools:
                        if fmt in tool.get("formats", []) and tool not in filtered:
                            filtered.append(tool)
            all_tools = filtered

        if not all_tools:
            tk.Label(self.tools_inner, text=self.t("no_results"), font=("Segoe UI", 12),
                     bg=BG, fg=FG_DIM).pack(pady=40)
            self._add_tool_button(self.tools_inner)
            return

        if self.view_mode == "grid":
            self._show_tools_grid(all_tools)
        else:
            self._show_tools_list(all_tools)

        self._add_tool_button(self.tools_inner)

    def _show_tools_grid(self, tools):
        cols = 4
        self._grid_cols = cols

        # Use a grid container for uniform card sizes
        grid_frame = tk.Frame(self.tools_inner, bg=BG)
        grid_frame.pack(fill="x", padx=10, pady=4)
        for c in range(cols):
            grid_frame.columnconfigure(c, weight=1, uniform="toolcard")

        for i, tool in enumerate(tools):
            row = i // cols
            col = i % cols
            self._create_tool_card(grid_frame, tool, grid=True, grid_row=row, grid_col=col)

    def _show_tools_list(self, tools):
        for tool in tools:
            self._create_tool_card(self.tools_inner, tool, grid=False)

    def _create_tool_card(self, parent, tool, grid=True, grid_row=0, grid_col=0):
        found = self._find_tool_path(tool)
        status_color = GREEN if found else RED
        status_text = self.t("found") if found else self.t("not_found")

        CARD_SIZE = 210  # square cards

        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=BORDER,
                        highlightthickness=1, width=CARD_SIZE, height=CARD_SIZE)
        card.pack_propagate(False)  # enforce fixed size

        if grid:
            card.grid(row=grid_row, column=grid_col, padx=4, pady=4, sticky="nsew")
            parent.rowconfigure(grid_row, weight=0)
        else:
            card.pack(fill="x", padx=10, pady=3)
            card.pack_propagate(True)  # list view can flex

        inner = tk.Frame(card, bg=CARD_BG, padx=10, pady=8)
        inner.pack(fill="both", expand=True)

        # Header
        hdr = tk.Frame(inner, bg=CARD_BG)
        hdr.pack(fill="x")
        icon = tool.get("icon", "\U0001f527")
        tk.Label(hdr, text=icon, font=("Segoe UI", 14), bg=CARD_BG, fg=FG).pack(side="left")
        tk.Label(hdr, text=f"\u25cf {status_text}", font=("Segoe UI", 7), bg=CARD_BG, fg=status_color).pack(side="right")

        # Tool name
        tk.Label(inner, text=tool["name"], font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=FG,
                 anchor="w", wraplength=185).pack(fill="x", pady=(2, 0))

        # Description (short in grid, full in list)
        desc_key = f"desc_{self.lang}"
        desc = tool.get(desc_key, tool.get("desc_en", ""))
        if grid:
            if len(desc) > 80:
                desc = desc[:77] + "..."
            wrap = 185
        else:
            wrap = 900
        tk.Label(inner, text=desc, font=("Segoe UI", 8), bg=CARD_BG, fg=FG_DIM,
                 wraplength=wrap, justify="left", anchor="nw").pack(fill="x", pady=(2, 0))

        # Format tags
        formats = tool.get("formats", [])
        if formats:
            fmt_frame = tk.Frame(inner, bg=CARD_BG)
            fmt_frame.pack(fill="x", pady=(3, 0))
            for fmt in formats[:4]:  # max 4 tags in square card
                tk.Label(fmt_frame, text=fmt, font=("Consolas", 7), bg=BG3, fg=CYAN,
                         padx=3, pady=0).pack(side="left", padx=(0, 2))

        # Related guides (list view only)
        if not grid:
            guide_ids = tool.get("guide_ids", [])
            if guide_ids:
                gf = tk.Frame(inner, bg=CARD_BG)
                gf.pack(fill="x", pady=(3, 0))
                all_guides = self._get_all_guides()
                for gid in guide_ids:
                    guide = next((g for g in all_guides if g.get("id") == gid), None)
                    if guide:
                        title_key = f"title_{self.lang}"
                        gtitle = guide.get(title_key, guide.get("title_en", gid))
                        lbl = tk.Label(gf, text=f"\U0001f4d6 {gtitle}", font=("Segoe UI", 8),
                                       bg=CARD_BG, fg=BLUE, cursor="hand2")
                        lbl.pack(side="left", padx=(0, 8))
                        lbl.bind("<Button-1>", lambda e, g=guide: self._show_guide_preview(g))

        # Spacer to push buttons to bottom
        spacer = tk.Frame(inner, bg=CARD_BG)
        spacer.pack(fill="both", expand=True)

        # Action buttons (anchored at bottom)
        btn_frame = tk.Frame(inner, bg=CARD_BG)
        btn_frame.pack(fill="x", side="bottom")

        if found:
            # FOUND: only Launch button
            tk.Button(btn_frame, text=f"\u25b6 {self.t('launch')}", font=("Segoe UI", 9, "bold"),
                      bg=GREEN, fg="#111", relief="flat", padx=10, pady=3, cursor="hand2",
                      command=lambda t=tool: self._launch_tool(t)).pack(side="left")
        else:
            # NOT FOUND: Download + Browse side by side
            dl = tool.get("download")
            if dl:
                tk.Button(btn_frame, text=f"\u2B07 {self.t('download')}", font=("Segoe UI", 9),
                          bg=ORANGE, fg="#111", relief="flat", padx=10, pady=3, cursor="hand2",
                          command=lambda u=dl: webbrowser.open(u)).pack(side="left", padx=(0, 4))

            tk.Button(btn_frame, text=f"\U0001f4c2 {self.t('set_path')}", font=("Segoe UI", 9),
                      bg=BG3, fg=FG, relief="flat", padx=10, pady=3, cursor="hand2",
                      command=lambda t=tool: self._browse_tool_path(t)).pack(side="left")

        # Custom indicator
        if tool.get("custom"):
            tk.Label(btn_frame, text=self.t("custom"), font=("Segoe UI", 8),
                     bg=CARD_BG, fg=PURPLE).pack(side="right")

    def _browse_tool_path(self, tool):
        """Let user pick the tool path manually."""
        exts = "*.py *.exe" if not tool.get("filename") else f"*{os.path.splitext(tool['filename'])[1]}"
        path = filedialog.askopenfilename(
            title=f"Select {tool['name']}",
            filetypes=[("Tool files", exts), ("All files", "*.*")]
        )
        if path:
            tool_id = tool.get("id") or tool.get("name")
            self.cfg.setdefault("tool_paths", {})[tool_id] = path
            save_config(self.cfg)
            self._show_tools()

    def _add_tool_button(self, parent):
        btn = tk.Button(parent, text=self.t("add_tool"), font=("Segoe UI", 11),
                        bg=BG2, fg=GREEN, relief="flat", padx=16, pady=8, cursor="hand2",
                        command=self._add_tool_dialog)
        btn.pack(pady=12)

    # ────────────────────────────────────────────────────────
    # GUIDES TAB
    # ────────────────────────────────────────────────────────
    def _build_guides_tab(self):
        pane = tk.PanedWindow(self.guides_outer, orient="horizontal", bg=BG,
                               sashwidth=4, sashrelief="flat")
        pane.pack(fill="both", expand=True)

        left = tk.Frame(pane, bg=BG)
        pane.add(left, width=360, minsize=280)

        self.guide_preview = tk.Frame(pane, bg=BG)
        pane.add(self.guide_preview, minsize=400)

        list_canvas = tk.Canvas(left, bg=BG, highlightthickness=0)
        list_sb = tk.Scrollbar(left, orient="vertical", command=list_canvas.yview)
        self.guides_list_inner = tk.Frame(list_canvas, bg=BG)
        self.guides_list_inner.bind("<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        list_canvas.create_window((0, 0), window=self.guides_list_inner, anchor="nw")
        list_canvas.configure(yscrollcommand=list_sb.set)
        list_canvas.pack(side="left", fill="both", expand=True)
        list_sb.pack(side="right", fill="y")

        tk.Label(self.guide_preview, text="\U0001f4d6", font=("Segoe UI", 48), bg=BG, fg=BG3).pack(pady=(80, 10))
        tk.Label(self.guide_preview, text=self.t("preview"), font=("Segoe UI", 14), bg=BG, fg=FG_DIM).pack()

        self._show_guides()

    def _show_guides(self, query=None):
        for w in self.guides_list_inner.winfo_children():
            w.destroy()

        all_guides = self._get_all_guides()

        if query:
            filtered = []
            for g in all_guides:
                title = g.get(f"title_{self.lang}", g.get("title_en", ""))
                tags = " ".join(g.get("tags", []))
                searchable = f"{title} {tags}".lower()
                if query in searchable:
                    filtered.append(g)
            all_guides = filtered

        if not all_guides:
            tk.Label(self.guides_list_inner, text=self.t("no_results"),
                     font=("Segoe UI", 11), bg=BG, fg=FG_DIM).pack(pady=20)

        for guide in all_guides:
            self._create_guide_item(guide)

        tk.Button(self.guides_list_inner, text=self.t("add_guide"),
                  font=("Segoe UI", 10), bg=BG2, fg=GREEN, relief="flat",
                  padx=12, pady=6, cursor="hand2",
                  command=self._add_guide_dialog).pack(pady=10)

    def _create_guide_item(self, guide):
        title_key = f"title_{self.lang}"
        title = guide.get(title_key, guide.get("title_en", ""))
        icon = guide.get("icon", "\U0001f4d6")

        item = tk.Frame(self.guides_list_inner, bg=CARD_BG, highlightbackground=BORDER,
                         highlightthickness=1, padx=10, pady=8, cursor="hand2")
        item.pack(fill="x", padx=6, pady=3)

        tk.Label(item, text=f"{icon}  {title}", font=("Segoe UI", 10, "bold"),
                 bg=CARD_BG, fg=FG, anchor="w").pack(fill="x")

        tags = guide.get("tags", [])
        if tags:
            tag_text = " ".join(f"#{t}" for t in tags[:5])
            tk.Label(item, text=tag_text, font=("Segoe UI", 8), bg=CARD_BG, fg=FG_DIM,
                     anchor="w").pack(fill="x")

        if guide.get("auto_discovered"):
            tk.Label(item, text="\U0001f4c2 Auto", font=("Segoe UI", 8),
                     bg=CARD_BG, fg=GREEN, anchor="w").pack(fill="x")
        elif guide.get("custom"):
            tk.Label(item, text=self.t("custom"), font=("Segoe UI", 8),
                     bg=CARD_BG, fg=PURPLE, anchor="w").pack(fill="x")

        for widget in [item] + item.winfo_children():
            widget.bind("<Button-1>", lambda e, g=guide: self._show_guide_preview(g))
            widget.bind("<Double-Button-1>", lambda e, g=guide: self._show_guide_popup(g))

    def _show_guide_preview(self, guide):
        for w in self.guide_preview.winfo_children():
            w.destroy()

        title_key = f"title_{self.lang}"
        title = guide.get(title_key, guide.get("title_en", ""))
        icon = guide.get("icon", "\U0001f4d6")
        content = load_guide_content(guide, self.lang, self.guides_dir)

        hdr = tk.Frame(self.guide_preview, bg=BG2, padx=12, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{icon}  {title}", font=("Segoe UI", 13, "bold"),
                 bg=BG2, fg=FG).pack(side="left")
        tk.Button(hdr, text=self.t("open_full"), font=("Segoe UI", 9),
                  bg=BG3, fg=ACCENT, relief="flat", padx=8, pady=2, cursor="hand2",
                  command=lambda: self._show_guide_popup(guide)).pack(side="right")

        text = tk.Text(self.guide_preview, font=("Consolas", self.font_size), bg=BG, fg=FG,
                       wrap="word", relief="flat", padx=12, pady=8, insertbackground=FG,
                       selectbackground=BG3)
        text.pack(fill="both", expand=True)
        text.insert("1.0", content)
        text.config(state="disabled")

        self.notebook.select(1)

    def _show_guide_popup(self, guide):
        title_key = f"title_{self.lang}"
        title = guide.get(title_key, guide.get("title_en", ""))
        content = load_guide_content(guide, self.lang, self.guides_dir)

        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("850x700")
        popup.configure(bg=BG)

        hdr = tk.Frame(popup, bg=BG2, padx=12, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{guide.get('icon', '')}  {title}",
                 font=("Segoe UI", 14, "bold"), bg=BG2, fg=FG).pack(side="left")
        tk.Button(hdr, text=self.t("close"), font=("Segoe UI", 9),
                  bg=ACCENT, fg="#fff", relief="flat", padx=8, pady=2,
                  command=popup.destroy).pack(side="right")

        text = tk.Text(popup, font=("Consolas", self.font_size), bg=BG, fg=FG,
                       wrap="word", relief="flat", padx=16, pady=12,
                       selectbackground=BG3)
        sb = tk.Scrollbar(popup, command=text.yview)
        text.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        text.pack(fill="both", expand=True)
        text.insert("1.0", content)
        text.config(state="disabled")

    # ────────────────────────────────────────────────────────
    # TOOL MANAGEMENT
    # ────────────────────────────────────────────────────────
    def _get_all_tools(self):
        tools = list(BUILTIN_TOOLS)
        for ut in self.cfg.get("user_tools", []):
            ut["custom"] = True
            tools.append(ut)
        return tools

    def _get_all_guides(self):
        guides = list(BUILTIN_GUIDES)
        for ug in self.cfg.get("user_guides", []):
            ug["custom"] = True
            guides.append(ug)
        # Auto-discover new guides from folder
        discovered = self._scan_guides_folder(guides)
        guides.extend(discovered)
        return guides

    def _scan_guides_folder(self, existing_guides):
        """Scan guides folder for .txt/.md files not yet registered."""
        if not os.path.isdir(self.guides_dir):
            return []

        # Collect all filenames already known by built-in/user guides
        known_files = set()
        for g in existing_guides:
            for key in ("file_en", "file_de"):
                if key in g and g[key]:
                    known_files.add(g[key].lower())

        # Scan folder
        found_files = {}
        for fname in os.listdir(self.guides_dir):
            if not fname.lower().endswith((".txt", ".md")):
                continue
            if fname.lower() in known_files:
                continue
            # Group by base name (strip _en/_de suffix)
            base = fname
            lang_suffix = None
            name_no_ext = os.path.splitext(fname)[0]
            if name_no_ext.endswith("_en"):
                base = name_no_ext[:-3]
                lang_suffix = "en"
            elif name_no_ext.endswith("_de"):
                base = name_no_ext[:-3]
                lang_suffix = "de"
            else:
                base = name_no_ext
                lang_suffix = "en"  # default: treat as English

            if base not in found_files:
                found_files[base] = {"en": None, "de": None}
            found_files[base][lang_suffix] = fname

        # Create guide entries
        discovered = []
        for base, files in found_files.items():
            # Make a readable title from the filename
            title = base.replace("_", " ").replace("-", " ").strip()
            title = " ".join(w.capitalize() for w in title.split())

            guide = {
                "id": f"auto_{base.lower()}",
                "title_en": title,
                "title_de": title,
                "icon": "\U0001f4c4",
                "tags": [t.lower() for t in base.replace("-", "_").split("_") if len(t) > 2],
                "tool_ids": [],
                "custom": True,
                "auto_discovered": True,
            }

            if files["en"]:
                guide["file_en"] = files["en"]
            if files["de"]:
                guide["file_de"] = files["de"]

            # If only one language exists, use it for both
            if files["en"] and not files["de"]:
                guide["file_de"] = files["en"]
            elif files["de"] and not files["en"]:
                guide["file_en"] = files["de"]

            discovered.append(guide)

        return discovered

    def _find_tool_path(self, tool):
        saved = self.cfg.get("tool_paths", {}).get(tool.get("id") or tool.get("name"))
        if saved and os.path.exists(saved):
            return saved

        filename = tool.get("filename", "")
        if not filename:
            return None

        local = os.path.join(SCRIPT_DIR, filename)
        if os.path.exists(local):
            return local

        for sp in tool.get("search_paths", []):
            check = os.path.normpath(os.path.join(SCRIPT_DIR, sp, filename))
            if os.path.exists(check):
                return check

        cp = tool.get("tool_path")
        if cp and os.path.exists(cp):
            return cp

        return None

    def _launch_tool(self, tool):
        path = self._find_tool_path(tool)
        if not path:
            messagebox.showerror("Error", f"Tool not found: {tool.get('filename', '?')}")
            return

        try:
            if tool.get("type") == "python" or path.endswith(".py"):
                subprocess.Popen([sys.executable, path], cwd=os.path.dirname(path))
            else:
                subprocess.Popen([path], cwd=os.path.dirname(path))
        except Exception as e:
            messagebox.showerror("Launch Error", str(e))

    # ────────────────────────────────────────────────────────
    # ADD TOOL DIALOG
    # ────────────────────────────────────────────────────────
    def _add_tool_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(self.t("add_tool"))
        dlg.geometry("550x520")
        dlg.configure(bg=BG)
        dlg.transient(self.root)
        dlg.grab_set()

        fields = {}

        def add_field(label_key, row):
            tk.Label(dlg, text=self.t(label_key), font=("Segoe UI", 10),
                     bg=BG, fg=FG, anchor="w").grid(row=row, column=0, padx=12, pady=4, sticky="w")
            var = tk.StringVar()
            tk.Entry(dlg, textvariable=var, font=("Segoe UI", 10),
                     bg=BG2, fg=FG, insertbackground=FG, relief="flat").grid(row=row, column=1, padx=12, pady=4, sticky="ew")
            return var

        dlg.columnconfigure(1, weight=1)

        fields["name"] = add_field("tool_name", 0)
        fields["path"] = add_field("tool_path", 1)

        tk.Button(dlg, text=self.t("browse"), font=("Segoe UI", 9), bg=BG3, fg=FG,
                  relief="flat", padx=6, cursor="hand2",
                  command=lambda: fields["path"].set(
                      filedialog.askopenfilename(filetypes=[("Python/Exe", "*.py *.exe"), ("All", "*.*")])
                  )).grid(row=1, column=2, padx=(0, 12), pady=4)

        fields["formats"] = add_field("tool_formats", 2)
        fields["desc_en"] = add_field("tool_desc_en", 3)
        fields["desc_de"] = add_field("tool_desc_de", 4)
        fields["download"] = add_field("tool_download", 5)

        def do_save():
            name = fields["name"].get().strip()
            path = fields["path"].get().strip()
            if not name:
                messagebox.showwarning("Warning", "Name required")
                return

            tool = {
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "icon": "\U0001f527",
                "desc_en": fields["desc_en"].get().strip() or name,
                "desc_de": fields["desc_de"].get().strip() or fields["desc_en"].get().strip() or name,
                "filename": os.path.basename(path) if path else "",
                "tool_path": path,
                "formats": [f.strip() for f in fields["formats"].get().split(",") if f.strip()],
                "type": "python" if path.endswith(".py") else "exe",
                "download": fields["download"].get().strip() or None,
                "guide_ids": [],
                "custom": True,
            }
            self.cfg.setdefault("user_tools", []).append(tool)
            if path:
                self.cfg.setdefault("tool_paths", {})[tool["id"]] = path
            save_config(self.cfg)
            dlg.destroy()
            self._show_tools()

        tk.Button(dlg, text=self.t("save"), font=("Segoe UI", 11, "bold"),
                  bg=GREEN, fg="#111", relief="flat", padx=16, pady=6, cursor="hand2",
                  command=do_save).grid(row=7, column=0, columnspan=3, pady=16)

    # ────────────────────────────────────────────────────────
    # ADD GUIDE DIALOG
    # ────────────────────────────────────────────────────────
    def _add_guide_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(self.t("add_guide"))
        dlg.geometry("650x650")
        dlg.configure(bg=BG)
        dlg.transient(self.root)
        dlg.grab_set()

        fields = {}
        dlg.columnconfigure(1, weight=1)

        tk.Label(dlg, text=self.t("guide_title_en"), font=("Segoe UI", 10),
                 bg=BG, fg=FG, anchor="w").grid(row=0, column=0, padx=12, pady=4, sticky="w")
        fields["title_en"] = tk.StringVar()
        tk.Entry(dlg, textvariable=fields["title_en"], font=("Segoe UI", 10),
                 bg=BG2, fg=FG, insertbackground=FG, relief="flat").grid(row=0, column=1, padx=12, pady=4, sticky="ew")

        tk.Label(dlg, text=self.t("guide_title_de"), font=("Segoe UI", 10),
                 bg=BG, fg=FG, anchor="w").grid(row=1, column=0, padx=12, pady=4, sticky="w")
        fields["title_de"] = tk.StringVar()
        tk.Entry(dlg, textvariable=fields["title_de"], font=("Segoe UI", 10),
                 bg=BG2, fg=FG, insertbackground=FG, relief="flat").grid(row=1, column=1, padx=12, pady=4, sticky="ew")

        tk.Label(dlg, text=self.t("guide_tags"), font=("Segoe UI", 10),
                 bg=BG, fg=FG, anchor="w").grid(row=2, column=0, padx=12, pady=4, sticky="w")
        fields["tags"] = tk.StringVar()
        tk.Entry(dlg, textvariable=fields["tags"], font=("Segoe UI", 10),
                 bg=BG2, fg=FG, insertbackground=FG, relief="flat").grid(row=2, column=1, padx=12, pady=4, sticky="ew")

        tk.Label(dlg, text=self.t("guide_tools"), font=("Segoe UI", 10),
                 bg=BG, fg=FG, anchor="w").grid(row=3, column=0, padx=12, pady=4, sticky="w")
        fields["tools"] = tk.StringVar()
        tk.Entry(dlg, textvariable=fields["tools"], font=("Segoe UI", 10),
                 bg=BG2, fg=FG, insertbackground=FG, relief="flat").grid(row=3, column=1, padx=12, pady=4, sticky="ew")

        tk.Label(dlg, text=self.t("guide_content_en"), font=("Segoe UI", 10),
                 bg=BG, fg=FG, anchor="w").grid(row=4, column=0, padx=12, pady=4, sticky="nw")
        content_en_frame = tk.Frame(dlg, bg=BG)
        content_en_frame.grid(row=4, column=1, padx=12, pady=4, sticky="nsew")
        fields["content_en"] = tk.Text(content_en_frame, font=("Consolas", 9), bg=BG2, fg=FG,
                                        height=8, wrap="word", insertbackground=FG, relief="flat")
        fields["content_en"].pack(fill="both", expand=True)

        tk.Label(dlg, text=self.t("or_file"), font=("Segoe UI", 9), bg=BG, fg=FG_DIM).grid(row=5, column=0, padx=12, sticky="w")
        tk.Button(dlg, text=self.t("browse"), font=("Segoe UI", 9), bg=BG3, fg=FG,
                  relief="flat", padx=6, cursor="hand2",
                  command=lambda: self._load_guide_file(fields["content_en"])).grid(row=5, column=1, padx=12, sticky="w")

        tk.Label(dlg, text=self.t("guide_content_de"), font=("Segoe UI", 10),
                 bg=BG, fg=FG, anchor="w").grid(row=6, column=0, padx=12, pady=4, sticky="nw")
        content_de_frame = tk.Frame(dlg, bg=BG)
        content_de_frame.grid(row=6, column=1, padx=12, pady=4, sticky="nsew")
        fields["content_de"] = tk.Text(content_de_frame, font=("Consolas", 9), bg=BG2, fg=FG,
                                        height=8, wrap="word", insertbackground=FG, relief="flat")
        fields["content_de"].pack(fill="both", expand=True)

        tk.Button(dlg, text=self.t("browse"), font=("Segoe UI", 9), bg=BG3, fg=FG,
                  relief="flat", padx=6, cursor="hand2",
                  command=lambda: self._load_guide_file(fields["content_de"])).grid(row=7, column=1, padx=12, sticky="w")

        dlg.rowconfigure(4, weight=1)
        dlg.rowconfigure(6, weight=1)

        def do_save():
            title_en = fields["title_en"].get().strip()
            if not title_en:
                messagebox.showwarning("Warning", "English title required")
                return
            content_en = fields["content_en"].get("1.0", "end").strip()
            content_de = fields["content_de"].get("1.0", "end").strip()
            guide = {
                "id": title_en.lower().replace(" ", "_"),
                "title_en": title_en,
                "title_de": fields["title_de"].get().strip() or title_en,
                "icon": "\U0001f4d6",
                "tags": [t.strip() for t in fields["tags"].get().split(",") if t.strip()],
                "tool_ids": [t.strip().lower().replace(" ", "_") for t in fields["tools"].get().split(",") if t.strip()],
                "content_en": content_en or title_en,
                "content_de": content_de or content_en or title_en,
                "custom": True,
            }
            self.cfg.setdefault("user_guides", []).append(guide)
            save_config(self.cfg)
            dlg.destroy()
            self._show_guides()

        tk.Button(dlg, text=self.t("save"), font=("Segoe UI", 11, "bold"),
                  bg=GREEN, fg="#111", relief="flat", padx=16, pady=6, cursor="hand2",
                  command=do_save).grid(row=8, column=0, columnspan=2, pady=12)

    def _load_guide_file(self, text_widget):
        path = filedialog.askopenfilename(filetypes=[("Text/Markdown", "*.txt *.md"), ("All", "*.*")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                text_widget.delete("1.0", "end")
                text_widget.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ────────────────────────────────────────────────────────
    # SETTINGS PANEL
    # ────────────────────────────────────────────────────────
    def _show_settings(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(self.t("settings"))
        dlg.geometry("650x550")
        dlg.configure(bg=BG)
        dlg.transient(self.root)
        dlg.grab_set()

        # ─── General Settings ───
        tk.Label(dlg, text=f"\u2699  {self.t('general')}", font=("Segoe UI", 13, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w", padx=16, pady=(16, 8))

        gen_frame = tk.Frame(dlg, bg=BG)
        gen_frame.pack(fill="x", padx=16)

        # Language
        row = tk.Frame(gen_frame, bg=BG)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=self.t("language"), font=("Segoe UI", 10), bg=BG, fg=FG, width=20, anchor="w").pack(side="left")
        lang_var = tk.StringVar(value=self.lang)
        lang_menu = ttk.Combobox(row, textvariable=lang_var, values=["en", "de"], state="readonly", width=10)
        lang_menu.pack(side="left", padx=8)

        # Font size
        row2 = tk.Frame(gen_frame, bg=BG)
        row2.pack(fill="x", pady=4)
        tk.Label(row2, text=self.t("font_size"), font=("Segoe UI", 10), bg=BG, fg=FG, width=20, anchor="w").pack(side="left")
        font_var = tk.IntVar(value=self.font_size)
        font_spin = tk.Spinbox(row2, from_=8, to=18, textvariable=font_var, width=5,
                                font=("Segoe UI", 10), bg=BG2, fg=FG, insertbackground=FG, relief="flat")
        font_spin.pack(side="left", padx=8)

        # View mode
        row3 = tk.Frame(gen_frame, bg=BG)
        row3.pack(fill="x", pady=4)
        tk.Label(row3, text=self.t("view_mode"), font=("Segoe UI", 10), bg=BG, fg=FG, width=20, anchor="w").pack(side="left")
        view_var = tk.StringVar(value=self.view_mode)
        view_menu = ttk.Combobox(row3, textvariable=view_var, values=["grid", "list"], state="readonly", width=10)
        view_menu.pack(side="left", padx=8)

        # Guides folder
        row4 = tk.Frame(gen_frame, bg=BG)
        row4.pack(fill="x", pady=4)
        tk.Label(row4, text=self.t("guides_folder"), font=("Segoe UI", 10), bg=BG, fg=FG, width=20, anchor="w").pack(side="left")
        guides_var = tk.StringVar(value=self.guides_dir)
        tk.Entry(row4, textvariable=guides_var, font=("Segoe UI", 9), bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat", width=35).pack(side="left", padx=8)
        tk.Button(row4, text="...", font=("Segoe UI", 9), bg=BG3, fg=FG, relief="flat",
                  padx=6, cursor="hand2",
                  command=lambda: guides_var.set(filedialog.askdirectory() or guides_var.get())).pack(side="left")

        # ─── Tool Paths ───
        tk.Label(dlg, text=f"\U0001f527  {self.t('tool_paths_mgmt')}", font=("Segoe UI", 13, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w", padx=16, pady=(16, 8))

        paths_canvas = tk.Canvas(dlg, bg=BG, highlightthickness=0, height=200)
        paths_sb = tk.Scrollbar(dlg, orient="vertical", command=paths_canvas.yview)
        paths_inner = tk.Frame(paths_canvas, bg=BG)
        paths_inner.bind("<Configure>", lambda e: paths_canvas.configure(scrollregion=paths_canvas.bbox("all")))
        paths_canvas.create_window((0, 0), window=paths_inner, anchor="nw")
        paths_canvas.configure(yscrollcommand=paths_sb.set)
        paths_canvas.pack(fill="both", expand=True, padx=16, pady=4)
        paths_sb.pack(side="right", fill="y")

        path_vars = {}
        for tool in self._get_all_tools():
            tool_id = tool.get("id") or tool.get("name")
            found = self._find_tool_path(tool)
            trow = tk.Frame(paths_inner, bg=BG)
            trow.pack(fill="x", pady=2)

            status = "\u25cf" if found else "\u25cb"
            color = GREEN if found else RED
            tk.Label(trow, text=f"{status} {tool['name']}", font=("Segoe UI", 9),
                     bg=BG, fg=color, width=28, anchor="w").pack(side="left")

            pv = tk.StringVar(value=found or "")
            path_vars[tool_id] = pv
            tk.Entry(trow, textvariable=pv, font=("Segoe UI", 8), bg=BG2, fg=FG_DIM,
                     insertbackground=FG, relief="flat", width=30).pack(side="left", padx=4)

            tk.Button(trow, text="...", font=("Segoe UI", 8), bg=BG3, fg=FG, relief="flat",
                      padx=4, cursor="hand2",
                      command=lambda v=pv: v.set(filedialog.askopenfilename() or v.get())).pack(side="left")

            tk.Button(trow, text="x", font=("Segoe UI", 8), bg=BG3, fg=RED, relief="flat",
                      padx=4, cursor="hand2",
                      command=lambda v=pv: v.set("")).pack(side="left", padx=2)

        # Save button
        def save_settings():
            self.lang = lang_var.get()
            self.font_size = font_var.get()
            self.view_mode = view_var.get()
            self.guides_dir = guides_var.get()

            self.cfg["lang"] = self.lang
            self.cfg["font_size"] = self.font_size
            self.cfg["view_mode"] = self.view_mode
            self.cfg["guides_dir"] = self.guides_dir

            # Save tool paths
            for tool_id, pv in path_vars.items():
                val = pv.get().strip()
                if val:
                    self.cfg.setdefault("tool_paths", {})[tool_id] = val
                else:
                    self.cfg.get("tool_paths", {}).pop(tool_id, None)

            save_config(self.cfg)
            dlg.destroy()
            self.lang_btn.config(text="DE" if self.lang == "en" else "EN")
            self._refresh_ui()

        tk.Button(dlg, text=f"\u2714  {self.t('save')}", font=("Segoe UI", 11, "bold"),
                  bg=GREEN, fg="#111", relief="flat", padx=20, pady=8, cursor="hand2",
                  command=save_settings).pack(pady=12)

    # ────────────────────────────────────────────────────────
    # CREDITS
    # ────────────────────────────────────────────────────────
    def _show_credits(self):
        popup = tk.Toplevel(self.root)
        popup.title(self.t("credits"))
        popup.geometry("550x450")
        popup.configure(bg=BG)

        text = tk.Text(popup, font=("Consolas", self.font_size), bg=BG, fg=FG,
                       wrap="word", relief="flat", padx=16, pady=12)
        text.pack(fill="both", expand=True)
        text.insert("1.0", CREDITS.get(self.lang, CREDITS["en"]))
        text.config(state="disabled")

    # ────────────────────────────────────────────────────────
    # TOGGLE ACTIONS
    # ────────────────────────────────────────────────────────
    def _toggle_lang(self):
        self.lang = "de" if self.lang == "en" else "en"
        self.cfg["lang"] = self.lang
        save_config(self.cfg)
        self.lang_btn.config(text="DE" if self.lang == "en" else "EN")
        self._refresh_ui()

    def _toggle_view(self):
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        self.cfg["view_mode"] = self.view_mode
        save_config(self.cfg)
        self.view_btn.config(text=self.t("list_view") if self.view_mode == "grid" else self.t("grid_view"))
        self._show_tools()

    def _refresh_ui(self):
        self.notebook.tab(0, text=f"  \U0001f527 {self.t('tools')}  ")
        self.notebook.tab(1, text=f"  \U0001f4d6 {self.t('guides')}  ")
        self.view_btn.config(text=self.t("list_view") if self.view_mode == "grid" else self.t("grid_view"))

        if self.search_entry.get() in [LANG["search"]["en"], LANG["search"]["de"]]:
            self.search_entry.delete(0, "end")
            self.search_entry.insert(0, self.t("search"))

        self._show_tools()
        self._show_guides()

    # ────────────────────────────────────────────────────────
    # STATUS BAR
    # ────────────────────────────────────────────────────────
    def _build_statusbar(self):
        sb = tk.Frame(self.root, bg=BG2, padx=10, pady=4)
        sb.pack(fill="x", side="bottom")

        all_tools = self._get_all_tools()
        found_count = sum(1 for t in all_tools if self._find_tool_path(t))
        total = len(all_tools)
        guides_count = len(self._get_all_guides())
        formats_count = len(FILE_FORMATS)

        info = f"{found_count}/{total} tools found  |  {guides_count} guides  |  {formats_count} file formats documented"
        tk.Label(sb, text=info, font=("Segoe UI", 9), bg=BG2, fg=FG_DIM).pack(side="left")
        tk.Label(sb, text=f"v{VERSION}", font=("Segoe UI", 9), bg=BG2, fg=FG_DIM).pack(side="right")

    def _on_close(self):
        save_config(self.cfg)
        self.root.destroy()


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ModdingHub(root)
    root.mainloop()
