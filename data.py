"""Was der Hub kennt: Werkzeuge, Anleitungen und Dateiformate.

Aus tw1_modding_hub.py 2.1 uebernommen (Marco 2026-02, erweitert 2026-09).
Nur Daten, keine Oberflaeche: das Fenster (modding_hub.py), das Guide-Fenster
(guidebook.py) und die Tests lesen daraus.

- TOOLS: id, name, icon, desc_en/de, filename, search_paths, formats, type
  ("exe" oder "python"), download, page, guide_ids
- GUIDES: id, title_en/de, tags, tool_ids, file_en/de (Datei im Ordner
  guides/), fallback_en/de
- FORMATS: Endung -> {en, de}
"""

TOOLS = [
    # ---- current tools by Alchemy Fox / MedievalDev (one exe each, no install;
    #      all of them: https://alchemy-fox.de/game/TW1_Tools/) ----
    {
        "id": "quest_creator",
        "name": "TW1 Dialog & Quest Creator",
        "icon": "\U0001f5d2",
        "desc_en": "Build your own quests and dialogues as a mod, in a node editor: quest timeline, checks before export, markers placed on the map, voice lines, and a finished .wd with one click. Guide inside (F1).",
        "desc_de": "Eigene Quests und Dialoge als Mod bauen, im Node-Editor: Quest-Zeitleiste, Pruefungen vor dem Export, Marker auf der Karte setzen, Sprachausgabe, fertige .wd mit einem Klick. Anleitung im Programm (F1).",
        "filename": "TW1QuestCreator.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".qtx", ".lan", ".lnd", ".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_DialogAndQuestCreator/releases/latest/download/TW1QuestCreator.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["map_to_mod_guide", "format_overview"],
    },
    {
        "id": "mod_manager",
        "name": "TW1 Mod Manager",
        "icon": "\U0001f4e6",
        "desc_en": "Install mods by dropping them on the window, switch them on and off like the in-game Mod Selector, see what each mod changes, and merge two mods into one. Nothing is ever deleted.",
        "desc_de": "Mods per Ziehen und Ablegen einlegen, ein- und ausschalten wie im Mod Selector des Spiels, sehen was jede Mod aendert und zwei Mods zu einer verschmelzen. Nichts wird je geloescht.",
        "filename": "TW1_Mod_Manager.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_ModManager/releases/latest/download/TW1_Mod_Manager.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["map_to_mod_guide"],
    },
    {
        "id": "wd_packer",
        "name": "TW1 WD Packer",
        "icon": "\U0001f5dc",
        "desc_en": "Drop a .wd on the window to unpack it, drop a folder to pack it. Every new archive is read back and compared with the folder before it replaces the old one. Built on buglord's WD Repacker.",
        "desc_de": "Eine .wd auf das Fenster ziehen: entpackt. Einen Ordner ziehen: gepackt. Jedes neue Archiv wird zurueckgelesen und mit dem Ordner verglichen, bevor es das alte ersetzt. Kern ist buglords WD Repacker.",
        "filename": "TW1_WD_Packer.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_WDPacker/releases/latest/download/TW1_WD_Packer.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["map_to_mod_guide", "format_overview"],
    },
    {
        "id": "par_editor_af",
        "name": "TW1 PAR Editor",
        "icon": "\U0001f4c8",
        "desc_en": "Edit the parameter database: every unit, weapon, spell and potion, with the SDK field names, groups and a live filter. Opens .wd archives directly and saves a mod .wd.",
        "desc_de": "Die Parameter-Datenbank bearbeiten: jede Einheit, Waffe, jeder Zauber und Trank, mit SDK-Feldnamen, Gruppen und Live-Filter. Oeffnet .wd-Archive direkt und speichert eine Mod-.wd.",
        "filename": "TW1_PAR_Editor.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".par", ".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_ParEditor/releases/latest/download/TW1_PAR_Editor.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["format_overview"],
    },
    {
        "id": "minimap_tool",
        "name": "TW1 Minimap Tool",
        "icon": "\U0001f5fa",
        "desc_en": "View, replace and create the minimap tiles, build a parchment world map and pack the result as a mod.",
        "desc_de": "Die Minimap-Kacheln ansehen, tauschen und neu anlegen, eine Pergament-Weltkarte bauen und das Ergebnis als Mod packen.",
        "filename": "TW1_Minimap_Tool.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".dds", ".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_MinimapTool/releases/latest/download/TW1_Minimap_Tool.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["map_to_mod_guide"],
    },
    {
        "id": "savegame_patcher",
        "name": "TW1 Savegame Patcher",
        "icon": "\U0001f4be",
        "desc_en": "Bring an existing save up to the mods you have enabled: script bytecode, quest tables and map markers inside the save - no new game.",
        "desc_de": "Einen bestehenden Spielstand auf die eingeschalteten Mods bringen: Skript-Bytecode, Questtabellen und Kartenmarker im Spielstand - ohne neues Spiel.",
        "filename": "TW1_Savegame_Patcher.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".sav"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_SavegamePatcher/releases/latest/download/TW1_Savegame_Patcher.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": [],
    },
    {
        "id": "dungeon_editor_af",
        "name": "TW1 Dungeon Editor",
        "icon": "\U0001f3f0",
        "desc_en": "Menu, toolbar and guide around Dungeons.exe from the SDK: paint the dungeon layout and export it for the Two Worlds Editor.",
        "desc_de": "Menue, Werkzeugleiste und Anleitung um Dungeons.exe aus dem SDK: Grundriss malen und fuer den Two Worlds Editor ausgeben.",
        "filename": "TW1DungeonEditor.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".lnd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_DungeonEditor/releases/latest/download/TW1DungeonEditor.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["dungeon_guide_part1", "dungeon_guide_part2"],
    },
    {
        "id": "quest_limit",
        "name": "TW1 Quest Limit Patcher",
        "icon": "\U0001f513",
        "desc_en": "Raises the quest limit of Two Worlds 1 from 400 to 600, installed as a mod, with one click. Only new games use the raised limit.",
        "desc_de": "Hebt die Questgrenze von Two Worlds 1 von 400 auf 600, als Mod, mit einem Klick. Nur neue Spiele nutzen die hoehere Grenze.",
        "filename": "TW1.Quest.Limit.Patcher.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [".wd"],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_QuestLimitPatcher/releases/latest/download/TW1.Quest.Limit.Patcher.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": ["map_to_mod_guide"],
    },
    {
        "id": "extended_settings",
        "name": "TW1 Extended Settings",
        "icon": "\u2699",
        "desc_en": "Fall, slide and lava damage, an immortal horse and the whistle range, set in a small window: a TWSE plugin plus its settings tool.",
        "desc_de": "Fall-, Rutsch- und Lavaschaden, unsterbliches Pferd und die Pfeifreichweite in einem kleinen Fenster: ein TWSE-Plugin und sein Einstellwerkzeug.",
        "filename": "tw1_Extendet-settings.exe",
        "search_paths": ["..", "../Tools", "../..", "../../Tools"],
        "formats": [],
        "type": "exe",
        "download": "https://github.com/MedievalDev/TW1_Extendet-settings/releases/latest/download/tw1_Extendet-settings.exe",
        "page": "https://alchemy-fox.de/game/TW1_Tools/",
        "guide_ids": [],
    },
    # ---- older python tools and SDK programs ----
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
        "id": "vdf_to_obj",
        "name": "TW1 VDF to OBJ",
        "icon": "\U0001f4d0",
        "desc_en": "Convert Two Worlds .vdf 3D models to standard .obj format. Export mesh geometry for use in Blender or other 3D editors.",
        "desc_de": "Konvertiert Two Worlds .vdf 3D-Modelle ins Standard .obj-Format. Mesh-Geometrie exportieren für Blender oder andere 3D-Editoren.",
        "filename": "tw1_vdf_to_obj.py",
        "formats": [".vdf", ".obj"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Two-Worlds-VDF-In-Export-Tool",
        "guide_ids": [],
    },
    {
        "id": "obj_to_vdf",
        "name": "TW1 OBJ to VDF",
        "icon": "\U0001f4d0",
        "desc_en": "Convert standard .obj 3D models to Two Worlds .vdf format. Import custom meshes into the game engine.",
        "desc_de": "Konvertiert Standard .obj 3D-Modelle ins Two Worlds .vdf-Format. Eigene Meshes in die Game-Engine importieren.",
        "filename": "tw1_obj_to_vdf.py",
        "formats": [".obj", ".vdf"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Two-Worlds-VDF-In-Export-Tool",
        "guide_ids": [],
    },
    {
        "id": "lnd_viewer",
        "name": "TW1 LND Viewer",
        "icon": "\U0001f5fa",
        "desc_en": "View Two Worlds .lnd level/map files. Inspect terrain data, textures, and map tile structure.",
        "desc_de": "Two Worlds .lnd Level/Map-Dateien anzeigen. Terrain-Daten, Texturen und Map-Tile-Struktur inspizieren.",
        "filename": "tw1_lnd_viewer.py",
        "formats": [".lnd"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Twor-Worlds-LND-Viewer",
        "guide_ids": ["editor_beginner_guide"],
    },
    {
        "id": "lnd_world_maps",
        "name": "TW1 LND World Maps Viewer",
        "icon": "\U0001f30d",
        "desc_en": "Export world map data from .lnd files — heightmaps, colormaps, and other terrain visualizations as image files.",
        "desc_de": "Weltkarten-Daten aus .lnd-Dateien exportieren — Heightmaps, Colormaps und andere Terrain-Visualisierungen als Bilddateien.",
        "filename": "tw1_lnd_world_maps.py",
        "formats": [".lnd"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Twor-Worlds-LND-Viewer",
        "guide_ids": ["editor_beginner_guide"],
    },
    {
        "id": "lnd_objects_exporter",
        "name": "TW1 LND Objects Exporter",
        "icon": "\U0001f4cb",
        "desc_en": "Export object data from .lnd files to CSV — position, scale, rotation, and object name for every placed object on a map tile.",
        "desc_de": "Objektdaten aus .lnd-Dateien als CSV exportieren — Position, Skalierung, Rotation und Objektname für jedes platzierte Objekt auf einem Map-Tile.",
        "filename": "tw1_lnd_objects_exporter.py",
        "formats": [".lnd", ".csv"],
        "type": "python",
        "download": "https://github.com/MedievalDev/Twor-Worlds-LND-Viewer",
        "guide_ids": [],
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

GUIDES = [
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
        "tool_ids": ["lan_viewer", "quest_editor", "par_tool", "vdf_to_obj", "obj_to_vdf", "lnd_viewer", "lnd_world_maps", "lnd_objects_exporter", "wd_repacker"],
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
.vdf    -> TW1 VDF to OBJ / TW1 OBJ to VDF
.lnd    -> TW1 LND Viewer / LND World Maps / LND Objects Exporter / TwoWorlds Editor
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
.vdf    -> TW1 VDF to OBJ / TW1 OBJ to VDF
.lnd    -> TW1 LND Viewer / LND World Maps / LND Objects Exporter / TwoWorlds Editor
.wd     -> WD Repacker / Mod Selector
.phx    -> Vom Editor generiert (PhysX-Kochen)
.lhc    -> Von LevelHeadersCacheGen.bat generiert
.bmp    -> Jeder Bildbetrachter""",
    },
]

FORMATS = {
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
