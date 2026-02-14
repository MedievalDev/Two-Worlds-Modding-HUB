# Two Worlds 1 — Editor Console Command Guide

**Version 1.0** — Comprehensive reference for the Two Worlds Editor console commands, workflows, and batch scripting.

> This guide documents how Reality Pump's internal editor commands work together.
> It covers individual command syntax, parameter details, and — most importantly —
> the correct **command sequences and workflows** needed to accomplish common tasks.
> Much of this information has never been publicly documented before.

---

## Table of Contents

1. [Console Basics](#1-console-basics)
2. [Batch Scripting with foreachlevel](#2-batch-scripting-with-foreachlevel)
3. [Terrain & Heightmaps](#3-terrain--heightmaps)
4. [Texturing](#4-texturing)
5. [Auto-Texturing & Texture Mixing](#5-auto-texturing--texture-mixing)
6. [Grass System](#6-grass-system)
7. [Object Placement](#7-object-placement)
8. [Markers](#8-markers)
9. [Level Management](#9-level-management)
10. [Connected Levels & World Building](#10-connected-levels--world-building)
11. [Underground System](#11-underground-system)
12. [Inside House System](#12-inside-house-system)
13. [Water & Fog](#13-water--fog)
14. [Camera & Viewport](#14-camera--viewport)
15. [World Map Export](#15-world-map-export)
16. [Particle System](#16-particle-system)
17. [Cleanup & Maintenance](#17-cleanup--maintenance)
18. [Complete Workflow Examples](#18-complete-workflow-examples)
19. [Parameter Reference](#19-parameter-reference)
20. [Tips & Gotchas](#20-tips--gotchas)

---

## 1. Console Basics

### Opening the Console

The Two Worlds Editor has a built-in console accessible via a configurable key (default: `C`). The console accepts commands in the format:

```
CommandName parameter1 parameter2 ...
```

Commands are **case-insensitive** — `editor.savelevel`, `Editor.SaveLevel`, and `EDITOR.SAVELEVEL` all work. However, file paths and string parameters may be case-sensitive depending on the filesystem.

### Command Structure

Commands follow a namespace pattern:

| Prefix | Domain |
|--------|--------|
| `Editor.*` | Level editing, terrain, objects, markers |
| `editor.*` | Lower-level editor functions (same domain, alternate casing) |
| `Engine.*` | Rendering engine, atmosphere, weather |
| `Graph.*` / `graph.*` | Graphics, display, mesh loading |
| `SkyBox.*` | Sky rendering, fog, weather effects |
| `Stats.*` | Performance statistics |
| `display.*` | On-screen display |
| `settings.*` | Application settings |
| `ParticleEdit.*` | Particle system editor |

### Reading vs Writing

Many commands serve dual purposes depending on whether you provide a parameter:

- **Without parameter** → reads/prints the current value to the console
- **With parameter** → sets the value

Example:
```
editor.setwaterh          → prints current water height
editor.setwaterh 850      → sets water height to 850
```

This is how the "Read Defaults" feature in the CMD Injector works — it sends commands without values to capture the current state.

### Inline Execution vs Scripts

Commands can be entered one at a time in the console, or combined into script files that are executed with `editor.foreachlevel` (see Section 2). For complex workflows involving multiple levels, batch scripts are essential.

---

## 2. Batch Scripting with foreachlevel

The most powerful feature in the editor console is the ability to run scripts across all levels automatically. This is how Reality Pump processed the entire game world — applying texture fixes, syncing level borders, and performing cleanup operations across all 108+ tiles at once.

### The Three Scope Commands

```
editor.foreachlevel @scriptfile.txt
```
Executes every command in `scriptfile.txt` on **every level** in the world (surface + underground).

```
editor.foreachsurfacelevel @scriptfile.txt
```
Executes only on **surface levels** (the overworld).

```
editor.foreachundergroundlevel @scriptfile.txt
```
Executes only on **underground levels** (dungeons, caves).

There is also a variant for levels containing water:
```
Editor.ForEachLevelWithWater @scriptfile.txt
```

### Script File Format

Script files are plain text files with one command per line. They must be placed in the game's working directory (typically the `Game\` folder where the editor executable is located).

Example: `edtex.txt`
```
Editor.LoadRightConnectedLevel
Editor.LoadBottomConnectedLevel
Editor.CopyEdgeFromConnected
Editor.CopyColorFromConnected
Editor.CleanupInvisibleTextures 1
Editor.CopyTexturesFromConnected
Editor.SaveAllLevels
```

When this script runs via `editor.foreachlevel @edtex.txt`, the editor:
1. Loads the first level
2. Executes all 7 commands in order
3. Moves to the next level
4. Repeats until every level has been processed

### Writing Your Own Scripts

You can create custom scripts for any repetitive task. Some guidelines:

- One command per line
- Empty lines and comments are generally ignored, but avoid special characters
- Always include `Editor.SaveAllLevels` or `editor.savelevel` at the end if you modify data
- Test your script on a single level first before running on the entire world
- Keep scripts focused — separate terrain scripts from texture scripts from object scripts

### Using foreachlevel with the CMD Injector

The CMD Injector can send `foreachlevel` commands directly to the editor console. The workflow:

1. Create your script file (e.g., `my_cleanup.txt`) in the editor's game directory
2. In the CMD Injector, create a button with the command: `editor.foreachlevel @my_cleanup.txt`
3. Click the button — the editor processes every level automatically

This is orders of magnitude faster than manually processing levels one at a time.

---

## 3. Terrain & Heightmaps

### Importing Heightmaps

The editor supports two heightmap formats: BMP and RAW.

#### BMP Import

```
Editor.LoadBmp file.bmp factor
```

| Parameter | Description |
|-----------|-------------|
| `file.bmp` | Grayscale BMP file located in `game\Editor\Heightmaps\` |
| `factor` | Height multiplier — scales the difference between lightest and darkest pixels |

**Constraints:**
- Must be grayscale BMP format
- BMP dimensions must be ≤ 4× the level size (e.g., for a 128×128 level, BMP can be up to 512×512)
- The BMP is applied to the currently loaded level

**Example:**
```
Editor.LoadBmp terrain_valley.bmp 2.5
```
This loads `game\Editor\Heightmaps\terrain_valley.bmp` and applies it with a height multiplier of 2.5.

#### RAW Import

```
editor.LoadRaw filename.raw BitsCnt HeaderSize TotalSizeX TotalSizeY StartX StartY StartAltitudeG HeightScaleG
```

| Parameter | Description |
|-----------|-------------|
| `filename.raw` | RAW file in `game\Editor\Heightmaps\` |
| `BitsCnt` | Bit depth: `8` or `16` |
| `HeaderSize` | Header size to skip (usually `0`) |
| `TotalSizeX` | Total width of the RAW data in pixels |
| `TotalSizeY` | Total height of the RAW data in pixels |
| `StartX` | X offset — which pixel to start copying from |
| `StartY` | Y offset — which pixel to start copying from |
| `StartAltitudeG` | Minimum height in grid units (the height a black pixel maps to) |
| `HeightScaleG` | Height range (white pixel height = StartAltitudeG + HeightScaleG) |

**Critical constraints:**
- `StartAltitudeG` must be ≥ 2
- `StartAltitudeG + HeightScaleG` must be < 128
- Heights are measured in grid units (1 grid unit = 16 game units vertically)

**Example:**
```
editor.loadraw 3a.raw 16 0 513 513 0 0 16 10
```
This imports a 16-bit RAW heightmap of size 513×513, with no header, starting at pixel (0,0), mapping black to altitude 16 and white to altitude 26.

**Using StartX/StartY for large terrains:**
If your heightmap covers the entire world (e.g., 4096×4096) but you're editing a single level, use StartX and StartY to select the correct region:
```
editor.loadraw world_height.raw 16 0 4096 4096 512 256 16 80
```
This reads from a 4096×4096 heightmap but starts at position (512, 256) within it.

### Exporting Heightmaps

```
Editor.saveRaw filename.raw BitsCnt HeaderSize TotalSizeX TotalSizeY StartX StartY StartAltitudeG HeightScaleG
```

Parameters match the import command. The export writes the current level's terrain to a RAW file.

**Example:**
```
Editor.saveRaw Map_C01.raw 16 0 512 512 0 0 0 1
```
Exports the current level as a 16-bit RAW, 512×512, with full height range (altitude 0 to 1 grid unit per value).

### Terrain Smoothing

```
Editor.SetSquareAltitudesAverage avrgRange factor
```

Also aliased as:
```
Editor.MakeAverageAltitude avrgRange factor
```

| Parameter | Description |
|-----------|-------------|
| `avrgRange` | Radius of the smoothing kernel: 0 = minimal, 1 = medium, 2+ = aggressive |
| `factor` | Smoothing intensity multiplier: 0.5 = gentle, 1.0 = full |

**Examples:**
```
Editor.MakeAverageAltitude 1 0.5    → gentle smoothing (good for fine terrain)
Editor.MakeAverageAltitude 2 1      → aggressive smoothing (flattens terrain significantly)
Editor.MakeAverageAltitude 0 1      → minimal smoothing (removes single-vertex spikes)
```

**Workflow — Progressive Smoothing:**
For natural-looking terrain, apply smoothing in stages rather than a single aggressive pass:
```
Editor.MakeAverageAltitude 0 1
Editor.MakeAverageAltitude 1 0.5
Editor.MakeAverageAltitude 1 0.3
```

### Global Height Adjustment

```
Editor.AddZToAll offset
```

Raises or lowers the entire level by `offset` height units.

```
Editor.AddZToAll 500     → raise entire level by 500 units
Editor.AddZToAll -200    → lower entire level by 200 units
```

There is also a variant:
```
Editor.AddZToAll2 offset
```
The exact difference is not documented, but it likely applies to a secondary height layer or uses a different calculation method.

### Plane Height

```
Editor.InitPlaneHeight
Editor.IncPlaneHeight
```

These control the reference plane used for certain terrain operations. `InitPlaneHeight` resets it, `IncPlaneHeight` raises it incrementally. Used internally during terrain editing operations.

### Terrain Generation

```
Editor.GenTerrain
```

Procedurally generates terrain geometry. Parameters are controlled by related settings:
```
Editor.PikePower       → controls terrain spike intensity
Editor.SharpAngle      → controls slope sharpness
Editor.MarginLine      → controls edge margins
```

---

## 4. Texturing

### Texture Indices

The Two Worlds editor uses a numbered texture slot system. Each level has texture slots (typically 0-15 or more) mapped to DDS texture files. Understanding the index system is critical for all texture commands:

- Textures are referenced by **index number** (0, 1, 2, etc.)
- Each index maps to a DDS file (e.g., `terrains\Texture_01.dds`)
- The `ReplaceTexSet` command maps by **filename**, not index
- The `ReplaceTexture` command swaps by **index number**

### Replacing Textures

#### By Filename

```
Editor.ReplaceTexSet "old_texture.dds" "new_texture.dds"
```

Replaces all occurrences of one texture with another by DDS filename. Use quotes around filenames containing spaces.

**Examples:**
```
Editor.ReplaceTexSet terrains\Texture_28.dds terrains\Texture_03.dds
Editor.ReplaceTexSet "terrains\Texture_04 copy.dds" terrains\Texture_04.dds
```

#### By Index

```
Editor.ReplaceTexture oldNum newNum
```

Swaps texture slot assignments. Every vertex painted with texture `oldNum` becomes texture `newNum`.

**Example:**
```
Editor.ReplaceTexture 7 3
```

### Texture Locking

```
Editor.LockTexture textureNum locked
```

| Parameter | Description |
|-----------|-------------|
| `textureNum` | Texture slot index |
| `locked` | `1` = locked (cannot be painted over), `0` = unlocked |

**Example:**
```
Editor.LockTexture 7 1     → lock texture 7 (e.g., road texture)
Editor.LockTexture 7 0     → unlock texture 7
```

Locking is useful when you want to auto-texture or mix textures without overwriting roads, paths, or other manually placed textures.

### Painting Textures from Images

#### Basic

```
Editor.TextureFromBitmap filename.bmp
```

Applies a BMP as a texture map to the level. The BMP must be in an accessible location.

#### Extended (with offset)

```
Editor.TextureFromBitmapEx filename.bmp startX startY
```

| Parameter | Description |
|-----------|-------------|
| `filename.bmp` | BMP file with indexed colors matching texture slots |
| `startX` | X pixel offset to start reading from |
| `startY` | Y pixel offset to start reading from |

**Example:**
```
Editor.TextureFromBitmapEx GENtexture.bmp 1024 2048
```

This is used for large texture maps covering the entire world — each level reads its section using the offset.

### Texture Edge Fixing

```
Editor.FixupTextureEdges
```

Automatically corrects texture seam artifacts at level boundaries. This is a non-destructive cleanup operation and should be run after any major texture changes.

### Cleaning Invisible Textures

```
Editor.CleanupInvisibleTextures mode
```

| Parameter | Description |
|-----------|-------------|
| `mode` | `1` = remove textures with zero alpha (fully transparent/hidden) |

Removes texture data that has no visual effect, reducing level file size and improving performance.

### Color Operations

```
Editor.ColorFill color
```
Fills the level's color map with a solid color.

```
Editor.FillWorldWithColor color
```
Fills with color (used extensively for underground initialization).

```
Editor.ReplaceColor oldColor newColor
```
Replaces one color with another in the level's color map.

```
Editor.ReplaceColorOnDisabledTerrain color1 color2 range
```
Replaces colors only on disabled (non-passable) terrain.

Colors use the format `0xAARRGGBB` (hex with alpha):
- `0xFFFFFFFF` = white, fully opaque
- `0xFF000000` = black, fully opaque
- `0x00000000` = black, fully transparent

---

## 5. Auto-Texturing & Texture Mixing

### Auto-Texture by Slope

```
Editor.AutoTextureEx angle1 tex1_0 tex1_1 percent1 angle2 tex2_0 tex2_1 percent2 angle3 tex3_0 tex3_1 percent3 angle4 tex4_0 tex4_1 percent4
```

This command automatically assigns textures based on **terrain slope angle**. It defines up to 4 angle thresholds, each with a pair of textures and a blend percentage.

| Parameter Group | Description |
|----------------|-------------|
| `angleN` | Slope threshold (0.0 = flat, 1.0 = vertical) |
| `texN_0` | Primary texture index for this slope range |
| `texN_1` | Secondary/blend texture index |
| `percentN` | Blend percentage between the two textures |

**How it works:**
- Terrain vertices with slope < angle1 get texture pair (tex1_0, tex1_1)
- Slopes between angle1 and angle2 get (tex2_0, tex2_1)
- And so on for angle3 and angle4
- The `percent` controls the random blend ratio between the two textures in each band

**Example:**
```
Editor.AutoTextureEx 0.1 1 2 0.2 2 3 0.4 9 10 0.5 9 10
```
This creates:
- Slopes 0-0.1 (nearly flat): blend between texture 1 and 2
- Slopes 0.1-0.2 (gentle): blend between texture 2 and 3
- Slopes 0.2-0.4 (moderate): blend between texture 9 and 10
- Slopes 0.4-0.5 (steep): blend between texture 9 and 10

**Workflow — Natural Terrain Texturing:**
1. Lock special textures (roads, paths) first: `Editor.LockTexture 5 1`
2. Run auto-texture: `Editor.AutoTextureEx 0.1 1 2 0.15 2 3 0.35 8 9 0.6 8 9`
3. Unlock: `Editor.LockTexture 5 0`
4. Fix edges: `Editor.FixupTextureEdges`
5. Clean up: `Editor.CleanupInvisibleTextures 1`

### Texture Mixer (Random Distribution)

#### TexMixerEx1 — Global Mix

```
Editor.TexMixerEx1 tex1 pct1 tex2 pct2 tex3 pct3 tex4 pct4 intensity
```

Randomly distributes up to 4 textures across the level with specified probabilities.

| Parameter | Description |
|-----------|-------------|
| `texN` | Texture slot index |
| `pctN` | Probability/weight (higher = more frequent) |
| `intensity` | Overall mixing strength (0-100) |

**Example:**
```
Editor.TexMixerEx1 1 30 2 30 3 30 4 30 100
```
Mixes textures 1-4 with equal probability at full intensity.

#### TexMixerEx2 — Conditional Mix

```
Editor.TexMixerEx2 tex1 pct1 tex2 pct2 tex3 pct3 tex4 pct4 intensity whereTextureExist
```

Same as TexMixerEx1, but **only applies where a specific texture already exists**. The extra parameter `whereTextureExist` is the texture index that must be present.

**Example:**
```
Editor.TexMixerEx2 1 30 2 30 3 30 4 30 8 10
```
Mixes textures 1-4 only where texture 10 currently exists, at intensity 8.

**Workflow — Layered Texture Mixing:**
```
// Step 1: Base coat with TexMixerEx1
Editor.TexMixerEx1 1 50 2 30 3 20 4 10 80

// Step 2: Add detail only on grass areas (texture 1)
Editor.TexMixerEx2 5 40 6 30 7 20 8 10 60 1

// Step 3: Clean up
Editor.CleanupInvisibleTextures 1
Editor.FixupTextureEdges
```

---

## 6. Grass System

The Two Worlds grass system paints grass billboards on terrain based on texture presence. Understanding the index system and the correct workflow order is essential.

### Critical: Grass Indices Start at 1

**Grass indices start at 1, not 0!** This is unlike texture indices which start at 0. The valid range is 1-8 (8 grass types per level). Using index 0 will produce unexpected results or errors.

The special index `-1` means **all grasses** in commands that support it.

### Adding Grass on Textures

```
editor.AddGrassOnTexture texNum minTexAlpha grassNum grassQuantity multiplyGrassTexAlpha
```

| Parameter | Description |
|-----------|-------------|
| `texNum` | Texture slot index to paint grass on |
| `minTexAlpha` | Minimum texture alpha (1-255) — only paint where texture alpha exceeds this |
| `grassNum` | Grass slot index (**1-8**, not 0!) |
| `grassQuantity` | Density: -1.0 to 1.0 (negative = remove grass) |
| `multiplyGrassTexAlpha` | `0` = flat quantity, `1` = multiply by texture alpha (creates natural falloff) |

**Examples:**
```
// Paint dense grass type 1 on texture 3 (grass texture)
editor.AddGrassOnTexture 3 1 1 0.8 1

// Paint sparse flowers (grass 4) on texture 2 (meadow)
editor.AddGrassOnTexture 2 50 4 0.3 1

// Remove grass type 2 from texture 7 (road)
editor.AddGrassOnTexture 7 1 2 -1.0 0
```

### Blurring Grass

```
Editor.BlurGrass grassNum steps
```

| Parameter | Description |
|-----------|-------------|
| `grassNum` | Grass index (1-8) or `-1` for all grasses |
| `steps` | Number of blur iterations (more = smoother distribution) |

Blurring softens the hard edges of grass placement, creating natural-looking transitions.

**Examples:**
```
Editor.BlurGrass 1 10      → blur grass 1 with 10 steps
Editor.BlurGrass -1 10     → blur ALL grasses with 10 steps
Editor.BlurGrass 3 5       → gentle blur on grass 3
```

### Clamping Grass Density

```
Editor.ClampGrassToLimit grassNum limit
```

| Parameter | Description |
|-----------|-------------|
| `grassNum` | Grass index (1-8) |
| `limit` | Maximum density: 0.0 to 1.0 |

Ensures grass density never exceeds the specified limit. Useful for performance control.

**Example:**
```
Editor.ClampGrassToLimit 1 0.5    → cap grass 1 at 50% density
Editor.ClampGrassToLimit 3 0.8    → cap grass 3 at 80% density
```

### Removing Grass

#### From Water Areas

```
Editor.RemoveGrassWhereWater
```

Removes all grass from areas covered by water. **Always run this after any grass painting operation** — grass growing from underwater looks wrong and wastes performance.

#### From Specific Textures

```
Editor.RemoveGrassWhereTexture textureNum grassNum respectAlpha
```

| Parameter | Description |
|-----------|-------------|
| `textureNum` | Texture index to clear grass from |
| `grassNum` | Which grass to remove (1-8) |
| `respectAlpha` | `1` = only remove where texture alpha is high, `0` = remove everywhere |

**Example:**
```
Editor.RemoveGrassWhereTexture 5 1 1    → remove grass 1 from texture 5 (e.g., road)
```

### Replacing Grass Types

```
editor.ReplaceGrass oldNum newNum
```

Swaps all instances of one grass type with another.

### Changing Grass Textures

```
editor.setgrasstexture slotNum texturePath
```

Changes which DDS texture a grass slot uses.

**Example:**
```
editor.setgrasstexture 8 grasses/fern.dds
```

### Complete Grass Workflow

This is the recommended order for grass operations:

```
// Step 1: Paint grass based on terrain textures
editor.AddGrassOnTexture 1 1 1 0.7 1        // grass on main terrain
editor.AddGrassOnTexture 2 1 2 0.5 1        // different grass on meadow
editor.AddGrassOnTexture 3 50 3 0.3 1       // flowers on specific texture

// Step 2: Remove from inappropriate areas
Editor.RemoveGrassWhereTexture 5 1 1         // no grass on roads
Editor.RemoveGrassWhereTexture 5 2 1         // no grass on roads
Editor.RemoveGrassWhereTexture 9 1 1         // no grass on rock
Editor.RemoveGrassWhereWater                 // no grass underwater

// Step 3: Smooth distribution
Editor.BlurGrass -1 10                       // blur all grasses

// Step 4: Cap density for performance
Editor.ClampGrassToLimit 1 0.6
Editor.ClampGrassToLimit 2 0.5
Editor.ClampGrassToLimit 3 0.3

// Step 5: Final water cleanup (blur may have re-introduced some)
Editor.RemoveGrassWhereWater
```

---

## 7. Object Placement

The editor provides a powerful automated object placement system. Objects (trees, rocks, buildings, decorations) can be distributed across the terrain with constraints on where they appear, how densely they're packed, and what surface types they attach to.

### Object Placement Pipeline

The correct order for automated object placement is:

1. **Define the area** (SetCreateRect)
2. **Define height constraints** (SetCreateMinMaxZ)
3. **Define exclusion zones** (AddCreateObjectsLockedTexture)
4. **Define surface types** (SetCreateObjectsOnType)
5. **Place objects** (CreateObjectsOnArea)
6. **Reset** (ResetCreateObjectsOnArea)

### Setting the Placement Area

```
editor.SetCreateRect left top right bottom [MinZ MaxZ]
```

Defines a rectangular area where objects can be placed. Coordinates are in world units. The optional MinZ/MaxZ constrains vertical placement.

```
editor.SetCreateMinMaxZ MinZ MaxZ
```

Sets the Z (height) range separately. Use `0 0` to disable the height limit.

**Examples:**
```
editor.SetCreateRect 100 100 500 500         // 400×400 unit area
editor.SetCreateMinMaxZ 10 30.5              // only place between height 10 and 30.5
editor.SetCreateMinMaxZ 0 0                  // no height restriction
```

### Texture Exclusion Zones

```
editor.AddCreateObjectsLockedTexture texNum minTexAlpha
```

Prevents objects from being placed on the specified texture. Multiple textures can be locked.

| Parameter | Description |
|-----------|-------------|
| `texNum` | Texture index to exclude |
| `minTexAlpha` | Minimum alpha threshold (1-255) |

**Example — Keep roads and water clear:**
```
editor.AddCreateObjectsLockedTexture 5 50     // no objects on road texture
editor.AddCreateObjectsLockedTexture 9 50     // no objects on water texture
editor.AddCreateObjectsLockedTexture 12 100   // no objects on path texture
```

**To clear all locked textures:**
```
editor.AddCreateObjectsLockedTexture clear
```

### Surface Type Constraints

```
Editor.SetCreateObjectsOnType bWater bObjects bWalkable bInsideHouses bNotPassable bUnitNotWalkable
```

Each parameter is a boolean (`0` or `1`):

| Parameter | Description |
|-----------|-------------|
| `bWater` | Allow placement on water? |
| `bObjects` | Allow placement on top of other objects? |
| `bWalkable` | Allow on walkable objects? |
| `bInsideHouses` | Allow inside house interiors? |
| `bNotPassable` | Allow on non-passable terrain? |
| `bUnitNotWalkable` | Allow where units cannot walk? |

**Example — Forest placement (safe defaults):**
```
Editor.SetCreateObjectsOnType 0 0 1 0 0 0
```
This places objects only on walkable ground — no water, no stacking, no interiors, no impassable terrain.

### Placing Objects

```
editor.CreateObjectsOnArea objectID count minRange [standMask]
```

| Parameter | Description |
|-----------|-------------|
| `objectID` | Object ID string (e.g., `OBJ_ID_TREE_OAK_01`) |
| `count` | Number of objects to place. Use `0` to only define minRange without placing. |
| `minRange` | Minimum distance between objects (in grid units) |
| `standMask` | Optional bitfield controlling attachment (see below) |

**standMask values:**
| Value | Effect |
|-------|--------|
| `0x7` | Glue to ground — objects snap to terrain surface |
| `0x100` | Box to lowest ground — object's bounding box aligns to the lowest terrain point beneath it |

**Examples:**
```
// Place 50 oak trees with minimum 3 unit spacing, glued to ground
editor.CreateObjectsOnArea OBJ_ID_TREE_OAK_01 50 3 0x7

// Define spacing for rocks without placing yet
editor.CreateObjectsOnArea OBJ_ID_ROCK_01 0 2

// Place 20 rocks using previously defined spacing
editor.CreateObjectsOnArea OBJ_ID_ROCK_01 20 2 0x7
```

### Placing Objects Near Other Objects

```
editor.CreateObjectsNearObjectsOnArea objectID nearObjectID count minRange maxRange [standMask]
```

Places objects near existing objects of a specific type. Useful for creating natural clusters.

| Parameter | Description |
|-----------|-------------|
| `objectID` | Object to place |
| `nearObjectID` | Object to cluster near |
| `count` | Number to place |
| `minRange` | Minimum distance from the "near" object |
| `maxRange` | Maximum distance from the "near" object |
| `standMask` | Attachment flags (0x7 or 0x100) |

**Note:** If `minRange` or `maxRange` > 32, the engine switches to "small coordinates" mode (a different unit scale).

**Example — Bushes near trees:**
```
editor.CreateObjectsNearObjectsOnArea OBJ_ID_BUSH_01 OBJ_ID_TREE_OAK_01 30 1 5 0x7
```
This places 30 bushes, each between 1 and 5 units from the nearest oak tree.

### Painting Textures on Object Areas

```
editor.SetTextureOnObjects objectID texNum count fullRange maxRange
```

Paints a texture around placed objects. Useful for adding ground detail (dirt around trees, etc.).

| Parameter | Description |
|-----------|-------------|
| `objectID` | Object type to paint around |
| `texNum` | Texture index to apply |
| `count` | Number of objects to process (`-1` = all) |
| `fullRange` | Radius of full-alpha application |
| `maxRange` | Radius at which alpha reaches zero (creates falloff) |

**Note:** If `fullRange`/`maxRange` > 32, "small coordinates" mode applies.

**Example:**
```
editor.SetTextureOnObjects OBJ_ID_TREE_OAK_01 3 -1 2 6
```
Paints texture 3 around every oak tree — full intensity within 2 units, fading to zero at 6 units.

### Deleting Objects

```
Editor.DeleteAllObjects objectID
```
Deletes all instances of the specified object type from the level.

```
editor.DeleteObjectsOnArea objectID count
```
Deletes objects within the currently set area (from SetCreateRect).

| Parameter | Special values |
|-----------|---------------|
| `objectID` | `NULL` = all objects, `Created` = objects placed by CreateObjectsOnArea |
| `count` | `-1` = delete all matching |

```
Editor.DeleteObjectsOnEdges
```
Removes objects at level boundaries (prevents overlap with neighboring levels).

```
Editor.DeleteObjectsOnEdgesMargin margin
```
Same, with configurable margin: `32` = 0.5m, `256` = 4m.

### Direct Object Creation

```
createEd x y z alpha [beta phi] objectID [meshVariant] [meshScale]
```

Places a single object at specific coordinates.

| Parameter | Description |
|-----------|-------------|
| `x, y` | World coordinates |
| `z` | Height: `0` = ground level. Offset: `z - ground = 16 × 256` |
| `alpha` | Rotation angle in degrees |
| `beta, phi` | Optional additional rotation axes |
| `objectID` | Object ID string |
| `meshVariant` | Optional mesh variant index |
| `meshScale` | Optional scale multiplier |

### Resetting Placement State

```
editor.ResetCreateObjectsOnArea
```

Clears the create rect, min/max Z, and locked textures. **Always call this when switching between different object placement tasks** to avoid leftover constraints.

### Complete Object Placement Workflow

```
// Step 1: Define area (entire level)
editor.SetCreateRect 0 0 2048 2048

// Step 2: No height restriction
editor.SetCreateMinMaxZ 0 0

// Step 3: Lock roads and water
editor.AddCreateObjectsLockedTexture 5 50      // road
editor.AddCreateObjectsLockedTexture 9 50      // water
editor.AddCreateObjectsLockedTexture 11 100    // path

// Step 4: Only on walkable ground
Editor.SetCreateObjectsOnType 0 0 1 0 0 0

// Step 5: Place trees
editor.CreateObjectsOnArea OBJ_ID_TREE_OAK_01 100 4 0x7
editor.CreateObjectsOnArea OBJ_ID_TREE_PINE_01 80 5 0x7

// Step 6: Place bushes near trees
editor.CreateObjectsNearObjectsOnArea OBJ_ID_BUSH_01 OBJ_ID_TREE_OAK_01 50 1 4 0x7

// Step 7: Paint dirt around trees
editor.SetTextureOnObjects OBJ_ID_TREE_OAK_01 4 -1 1 3

// Step 8: Add ground grass
editor.AddGrassOnTexture 1 1 1 0.6 1
Editor.RemoveGrassWhereWater

// Step 9: Remove edge objects for clean level transitions
Editor.DeleteObjectsOnEdgesMargin 64

// Step 10: Reset placement state
editor.ResetCreateObjectsOnArea
editor.AddCreateObjectsLockedTexture clear

// Step 11: Save
editor.savelevel 0
```

---

## 8. Markers

Markers are positioned points in the level used for gameplay logic — spawn points, quest locations, teleporters, enemy zones, etc.

### Deleting Markers

```
editor.DeleteMarker markerID num
editor.DeleteMarker markerID minNum maxNum
```

Deletes markers by ID and number/range.

```
Editor.DeleteBadMarkers
```
Removes all invalid/orphaned markers from the level.

```
Editor.DeleteBadObjectMarkers markerID
```
Removes invalid markers for a specific marker type.

```
Editor.SetMissingObjectMarkersNumbers
```
Auto-assigns numbers to markers that are missing them.

### Visualizing Markers on Map

```
Editor.SetDrawMapMarkers MARKER_ID color [MARKER_ID color ...]
```

Draws markers on the editor's map view with specified colors.

**Example:**
```
Editor.SetDrawMapMarkers MARKER_ENEMY_* 0xFFFF0000 MARKER_B_WOODCUT 0xFFFFFF00
```
This shows enemy markers in red and woodcutting markers in yellow. Wildcard `*` patterns are supported.

**To turn off marker display:**
```
Editor.SetDrawMapMarkers x
```

```
editor.MapMarkerSize 2
```
Sets the display size of markers on the map (default is quite small).

### Visualizing Objects on Map

```
Editor.SetDrawMapObjects OBJ_ID_* color [OBJ_ID_* color ...]
```

Similar to markers but for placed objects.

```
Editor.UpdateDrawMapObjects
```
Refreshes the object display after changes.

**To turn off:**
```
Editor.SetDrawMapObjects x
```

---

## 9. Level Management

### Saving and Loading

```
editor.savelevel 0
```
Saves the current level. The `0` parameter confirms the save.

```
Editor.SaveAllLevels
```
Saves all currently loaded levels (including connected levels).

```
editor.LoadLevel level.lnd
```
Loads a specific level file.

### Level BMP Export

```
editor.SaveLevelBmp
```
Exports the current level as a BMP image. Useful for creating overview maps or debugging terrain.

### Resizing Levels

```
editor.setlevelsize Level.lnd newWidth newHeight offsetDx offsetDy NewLevel.lnd
```

| Parameter | Description |
|-----------|-------------|
| `Level.lnd` | Input level file |
| `newWidth` | New width in grid units |
| `newHeight` | New height in grid units |
| `offsetDx` | X offset for existing data within the new size |
| `offsetDy` | Y offset for existing data within the new size |
| `NewLevel.lnd` | Output level file |

**Example:**
```
editor.setlevelsize Net_P_01.lnd 128 128 16 16 Net_P_01new.lnd
```
Resizes Net_P_01.lnd to 128×128 and shifts the existing content by (16, 16), saving as a new file.

### Joining Levels

```
editor.joinlevels LevelA.lnd LevelB.lnd LevelC.lnd LevelD.lnd Output.lnd
```

Combines four levels into one. The levels are arranged in a 2×2 grid.

**Critical requirement:** Textures between the levels must be synchronized first! If levels use different texture sets, the result will have incorrect texturing. Always run the level sync workflow (Section 10) before joining.

**Example:**
```
editor.joinlevels Map_E03.lnd Map_F03.lnd Map_E04.lnd Map_F04.lnd Joined_EF34.lnd
```

### Level Properties

```
Editor.SetLevelSpecialFlags flags
Editor.GetLevelSpecialFlags
Editor.SetLevelInfoText "text"
Editor.GetLevelInfoText
```

### Saving Levels to Texture Images

```
editor.SaveAllLevelsToTexture layer mode output.tga fillColor ORcolor [texParams...]
```

Exports level data as TGA images, useful for creating world overview maps.

| Parameter | Description |
|-----------|-------------|
| `layer` | 0 = surface, 1 = underground |
| `mode` | 0 = texture-based, 1 = color-based, 2 = locked areas, 3 = not-locked areas |
| `output.tga` | Output filename |
| `fillColor` | Background fill color (0xAARRGGBB) |
| `ORcolor` | OR-blended color / locked color marker |

**Examples:**
```
// Surface roads map (based on a specific texture)
editor.SaveAllLevelsToTexture 0 0 WorldRoads.tga 0x00000000 0 terrains\texture_01.dds 0xFFFFFFFF 120

// Underground color map
editor.SaveAllLevelsToTexture 1 1 WorldUndergroundColors.tga 0x00000000 0xFFFFFFFF

// Underground locked areas
editor.SaveAllLevelsToTexture 1 2 WorldUndergroundLocked.tga 0x00000000 0xFFFFFFFF

// Underground non-locked areas
editor.SaveAllLevelsToTexture 1 3 WorldUndergroundNotLocked.tga 0x00000000 0xFFFFFFFF
```

---

## 10. Connected Levels & World Building

Two Worlds' open world is built from a grid of connected levels (tiles). When editing one tile, changes at the borders must be synchronized with neighboring tiles to prevent visible seams. The editor has a complete pipeline for this.

### Loading Connected Levels

```
Editor.LoadRightConnectedLevel
Editor.LoadLeftConnectedLevel
Editor.LoadBottomConnectedLevel
Editor.LoadTopConnectedLevel
Editor.LoadObjectsForConnectedLevel 0/1
```

These load the neighboring level data. `LoadObjectsForConnectedLevel` controls whether to also load the neighbor's objects (0=no, 1=yes).

### Locking Vertices at Borders

```
Editor.LockVertexesWithConnectedLevel size
```

Locks terrain vertices near the border so they match the connected level. The `size` parameter controls how many vertex rows are locked.

### Copying Data from Connected Levels

```
Editor.CopyAltitudeFromConnected size mode
```

| Parameter | Description |
|-----------|-------------|
| `size` | Number of vertex rows to copy |
| `mode` | Blending mode: `0`=flat, `1`=mirror, `2`=mirror inverted, `3`=linear interpolation |

```
Editor.CopyEdgeFromConnected
```
Copies the last additional vertex line from the right/upper edge of the connected level. This ensures the visual edge perfectly matches.

```
Editor.CopyColorFromConnected
```
Copies the color map from the connected level's border.

```
Editor.CopyTexturesFromConnected
```
Copies texture data from the connected level's border.

```
Editor.ClearLockedVertexes
```
Unlocks all previously locked vertices.

### The Complete Level Sync Workflow (edtex.txt)

This is the script Reality Pump used to synchronize all levels in the world. It should be run on every level after terrain or texture changes:

```
Editor.LoadRightConnectedLevel
Editor.LoadBottomConnectedLevel
Editor.CopyEdgeFromConnected
Editor.CopyColorFromConnected
Editor.CleanupInvisibleTextures 1
Editor.CopyTexturesFromConnected
Editor.SaveAllLevels
```

**As a batch:**
```
editor.foreachlevel @edtex.txt
```

**Order matters!** The sequence is:
1. Load neighbors first (right + bottom, because the sync goes left→right, top→bottom)
2. Copy geometry edges
3. Copy color data
4. Clean up invisible textures
5. Copy texture data
6. Save everything

If you reverse the order or skip steps, you get visible seams between levels.

### Understanding the Altitude Copy Modes

When using `Editor.CopyAltitudeFromConnected size mode`:

| Mode | Effect | Use Case |
|------|--------|----------|
| 0 — Flat | Terrain at the border becomes flat at the neighbor's edge height | Quick fix, looks unnatural |
| 1 — Mirror | Border terrain mirrors the neighbor's terrain | Smooth transition, most common |
| 2 — Mirror Inverted | Border terrain mirrors inverted | Valleys between levels |
| 3 — Linear Approximation | Linearly interpolates between the two levels | Most natural for gentle terrain |

**Recommended for most cases:**
```
Editor.CopyAltitudeFromConnected 4 3
```
This copies 4 vertex rows using linear interpolation — the smoothest transition.

---

## 11. Underground System

The underground (caves, dungeons) uses a different initialization workflow than the surface. The key difference is that underground areas start with **disabled terrain** (non-walkable black) and you **paint** walkable areas.

### Underground Initialization Workflow

**Step 1: Fill all underground levels with white (enabled) color**
```
Editor.foreachundergroundlevel Editor.FillWorldWithColor 0xFFFFFFFF
```

**Step 2: Apply the underground script on each level**

Create `edundgr.txt`:
```
Editor.ReplaceColor 0xFF000000 0xFFFFFFFF
editor.LabelNotDisabledPassableFromMarkers MARKER_TELEPORT_DEST_FROMUPPER MARKER_TELEPORT_DEST_FROMLOWER
Editor.ReplaceColorOnDisabledTerrain 0xFFFFFFFF 0xFF000000 4
editor.savelevel
```

Run:
```
Editor.foreachundergroundlevel @edundgr.txt
```

### What Each Step Does

1. **ReplaceColor**: Converts any remaining black (disabled) to white (enabled) as base
2. **LabelNotDisabledPassableFromMarkers**: Marks areas reachable from teleport destinations. The markers `MARKER_TELEPORT_DEST_FROMUPPER` (entry from surface) and `MARKER_TELEPORT_DEST_FROMLOWER` (entry from deeper level) define where players can enter the underground
3. **ReplaceColorOnDisabledTerrain**: Converts white back to black on terrain that's been flagged as disabled, with a range parameter of 4. This creates the final passable/impassable map
4. **savelevel**: Saves the result

### Related Commands

```
Editor.ClearDisabled
```
Clears all disabled terrain flags.

```
Editor.TextureWherePassable
```
Applies textures only to passable areas.

---

## 12. Inside House System

The editor has a system for managing objects inside house interiors. This creates definition files that describe what objects go inside each house, enabling bulk operations.

### Workflow

**Step 1: Analyze existing houses and build definitions**
```
editor.BuildInsideHouseObjectsDef
```
Scans all houses in the level and builds internal definitions of their contents.

**Step 2: Export definitions to a file**
```
editor.WriteInsideHouseObjectsDef houses.txt
```
Writes the object placement data to a text file for review/editing.

**Step 3: Modify the definition file**
Edit `houses.txt` to add, remove, or rearrange objects inside houses.

**Step 4: Load modified definitions**
```
editor.LoadInsideHouseObjectsDef houses.txt
```

**Step 5: Clear existing house interiors**
```
editor.ClearObjectsInsideHouse
```
Removes all objects currently inside houses.

**Step 6: Recreate from definitions**
```
editor.CreateObjectsInsideHouseFromDef
```
Places objects according to the loaded definitions.

### Use Cases

- **Furnishing many houses at once**: Build definitions from one well-furnished house, then apply to all similar houses
- **Standardizing interiors**: Ensure all houses of a certain type have the same furniture layout
- **Bulk modification**: Change all candles to torches, replace all chairs with benches, etc.

---

## 13. Water & Fog

### Water Height

```
editor.setwaterh height
```

Sets the global water height for the current level. All water surfaces in the level sit at this Y coordinate.

**Example:**
```
editor.setwaterh 850       // set water to height 850
editor.setwaterh            // query current water height (no parameter)
```

### Water Color

```
Editor.SetWaterColor r g b
```

Sets the water tint color.

**Example:**
```
Editor.SetWaterColor 1 0 0     // red water (lava?)
Editor.SetWaterColor 0 0 1     // blue water
```

### Fog

```
Editor.RemoveLocalFog
```

Removes local fog volumes from the current level. This is useful when fog placement has become messy or when you want to start fresh with fog.

Related engine fog commands:
```
graph.fogenable 0/1          // toggle global fog
graph.enablefog 0/1          // alternative toggle
graph.fogcolor r g b          // set fog color
Engine.SetFogParams ...       // detailed fog parameters
Engine.SetFogColor ...        // fog color via engine
SkyBox.FogHazePower value     // haze intensity
SkyBox.FogHazeFactor value    // haze distance factor
SkyBox.FogHazePowFactor value // haze power curve
```

---

## 14. Camera & Viewport

### Scroll Speed

```
editor.ScrollDistDiv value
editor.ScrollDistDivMin value
editor.ScrollDistDivMax value
```

Controls the camera scroll speed (and its min/max limits). Lower `Div` values = faster scrolling.

### Zoom Speed

```
editor.ZoomDistDiv value
editor.ZoomDistDivMin value
editor.ZoomDistDivMax value
```

Controls the camera zoom speed and limits.

### Input Methods

The editor supports multiple input modes for camera control:
```
editor.KbdScroll 0/1         // keyboard scroll
editor.KbdView 0/1           // keyboard view rotation
editor.KbdRotate 0/1         // keyboard terrain rotation
editor.KbdZoom 0/1           // keyboard zoom
editor.MouseScroll 0/1       // mouse scroll
editor.MButtonScroll 0/1     // middle button scroll
editor.WheelZoom 0/1         // scroll wheel zoom
editor.MouseRotate 0/1       // mouse rotation
editor.MouseView 0/1         // mouse view control
editor.MouseZoom 0/1         // mouse zoom
```

---

## 15. World Map Export

### Tracing Used Objects

```
editor.foreachlevel editor.TraceUsedObjects output.txt [objectID]
```

Scans all levels and writes a list of used objects to a file. If `objectID` is specified, only traces that specific object type. Without it, traces all objects.

**Example:**
```
editor.foreachlevel editor.TraceUsedObjects AllObjects.txt
editor.foreachlevel editor.TraceUsedObjects TreeUsage.txt OBJ_ID_TREE_*
```

### Level BMP Export

```
editor.SaveLevelBmp
```

Exports the current level as a BMP. Can be combined with `foreachlevel` to export every level:
```
editor.foreachlevel editor.SaveLevelBmp
```

### World Texture Export

See Section 9 for `editor.SaveAllLevelsToTexture` — exports the entire world as TGA images showing roads, underground layout, locked areas, etc.

---

## 16. Particle System

```
ParticleEdit.PrintUsedFiles
```

Writes a list of all particle effect files used in the game to `Z:\Game\ParticleEditUsedFiles.txt`. Useful for asset management and finding unused particle files.

---

## 17. Cleanup & Maintenance

### Essential Cleanup Commands

| Command | Effect |
|---------|--------|
| `Editor.DeleteBadMarkers` | Removes invalid/orphaned markers |
| `Editor.DeleteBadObjectMarkers markerID` | Removes invalid markers of a specific type |
| `Editor.CleanupInvisibleTextures 1` | Removes zero-alpha texture data |
| `Editor.FixupTextureEdges` | Fixes texture seam artifacts |
| `Editor.RemoveGrassWhereWater` | Removes underwater grass |
| `Editor.DeleteObjectsOnEdges` | Removes objects at level borders |
| `Editor.RemoveLocalFog` | Clears local fog volumes |
| `editor.ResetCreateObjectsOnArea` | Resets placement constraints |
| `editor.AddCreateObjectsLockedTexture clear` | Clears texture locks |

### Recommended Cleanup Script

Save as `cleanup.txt`:
```
Editor.DeleteBadMarkers
Editor.CleanupInvisibleTextures 1
Editor.FixupTextureEdges
Editor.RemoveGrassWhereWater
Editor.DeleteObjectsOnEdges
editor.savelevel
```

Run on all levels:
```
editor.foreachlevel @cleanup.txt
```

### Deep Cleanup Script

A more thorough cleanup that also handles connected level borders:
```
Editor.LoadRightConnectedLevel
Editor.LoadBottomConnectedLevel
Editor.DeleteBadMarkers
Editor.CleanupInvisibleTextures 1
Editor.FixupTextureEdges
Editor.CopyEdgeFromConnected
Editor.CopyColorFromConnected
Editor.CopyTexturesFromConnected
Editor.RemoveGrassWhereWater
Editor.DeleteObjectsOnEdgesMargin 64
Editor.SaveAllLevels
```

---

## 18. Complete Workflow Examples

### Workflow A: Creating a New Forest Area

This workflow creates a complete forest area from scratch on an empty level.

```
// === TERRAIN ===
// Import heightmap
Editor.LoadBmp forest_heights.bmp 3.0

// Smooth terrain for natural look
Editor.MakeAverageAltitude 1 0.5
Editor.MakeAverageAltitude 2 0.3

// === TEXTURES ===
// Lock road textures before auto-texturing
Editor.LockTexture 5 1

// Auto-texture by slope: flat=grass, gentle=dirt, steep=rock, cliff=rock
Editor.AutoTextureEx 0.1 1 2 0.15 2 3 0.35 8 9 0.6 8 9

// Unlock roads
Editor.LockTexture 5 0

// Add variety with mixer (only on grass areas)
Editor.TexMixerEx2 1 40 2 30 3 20 4 10 50 1

// Fix edges
Editor.FixupTextureEdges
Editor.CleanupInvisibleTextures 1

// === OBJECTS ===
// Set up placement area (entire level)
editor.SetCreateRect 0 0 2048 2048
editor.SetCreateMinMaxZ 0 0

// Exclude roads from object placement
editor.AddCreateObjectsLockedTexture 5 50
Editor.SetCreateObjectsOnType 0 0 1 0 0 0

// Place trees
editor.CreateObjectsOnArea OBJ_ID_TREE_OAK_01 120 4 0x7
editor.CreateObjectsOnArea OBJ_ID_TREE_PINE_01 80 5 0x7
editor.CreateObjectsOnArea OBJ_ID_TREE_BIRCH_01 40 6 0x7

// Place undergrowth near trees
editor.CreateObjectsNearObjectsOnArea OBJ_ID_BUSH_01 OBJ_ID_TREE_OAK_01 60 1 4 0x7
editor.CreateObjectsNearObjectsOnArea OBJ_ID_BUSH_02 OBJ_ID_TREE_PINE_01 40 1 3 0x7

// Place rocks
editor.CreateObjectsOnArea OBJ_ID_ROCK_01 30 8 0x7
editor.CreateObjectsOnArea OBJ_ID_ROCK_02 20 10 0x7

// Paint dirt around trees
editor.SetTextureOnObjects OBJ_ID_TREE_OAK_01 4 -1 1 3

// Clean up
editor.ResetCreateObjectsOnArea
editor.AddCreateObjectsLockedTexture clear
Editor.DeleteObjectsOnEdgesMargin 64

// === GRASS ===
editor.AddGrassOnTexture 1 1 1 0.7 1       // grass on terrain
editor.AddGrassOnTexture 2 1 2 0.4 1       // different grass on meadow
editor.AddGrassOnTexture 1 50 3 0.2 1      // flowers sparse on terrain
Editor.RemoveGrassWhereTexture 5 1 1        // no grass on road
Editor.RemoveGrassWhereTexture 9 1 1        // no grass on rock
Editor.RemoveGrassWhereWater
Editor.BlurGrass -1 10
Editor.ClampGrassToLimit 1 0.6
Editor.ClampGrassToLimit 2 0.5
Editor.ClampGrassToLimit 3 0.3
Editor.RemoveGrassWhereWater               // repeat after blur

// === SAVE ===
editor.savelevel 0
```

### Workflow B: World-Wide Texture Update

When you change a texture across the entire game world:

**Step 1: Replace the texture**
```
editor.foreachlevel Editor.ReplaceTexSet terrains\Texture_28.dds terrains\Texture_03.dds
```

**Step 2: Sync all level borders**
```
editor.foreachlevel @edtex.txt
```

**Step 3: Clean up**
```
editor.foreachlevel @cleanup.txt
```

### Workflow C: Underground Dungeon Setup

```
// Step 1: Initialize all underground levels
Editor.foreachundergroundlevel Editor.FillWorldWithColor 0xFFFFFFFF

// Step 2: Process each underground level
// (Save as edundgr.txt and run via foreachundergroundlevel)
Editor.ReplaceColor 0xFF000000 0xFFFFFFFF
editor.LabelNotDisabledPassableFromMarkers MARKER_TELEPORT_DEST_FROMUPPER MARKER_TELEPORT_DEST_FROMLOWER
Editor.ReplaceColorOnDisabledTerrain 0xFFFFFFFF 0xFF000000 4
editor.savelevel

// Step 3: Run
Editor.foreachundergroundlevel @edundgr.txt
```

### Workflow D: Mass Object Cleanup

When you need to remove all objects of a specific type and replace them:

```
// Remove old trees
Editor.DeleteAllObjects OBJ_ID_TREE_OLD_01

// Set up for replacement
editor.SetCreateRect 0 0 2048 2048
editor.SetCreateMinMaxZ 0 0
editor.AddCreateObjectsLockedTexture 5 50
editor.AddCreateObjectsLockedTexture 9 50
Editor.SetCreateObjectsOnType 0 0 1 0 0 0

// Place new trees
editor.CreateObjectsOnArea OBJ_ID_TREE_NEW_01 100 4 0x7

// Or replace directly (if 1:1 swap)
Editor.ReplaceObject OBJ_ID_TREE_OLD_01 OBJ_ID_TREE_NEW_01

// Clean up
editor.ResetCreateObjectsOnArea
editor.AddCreateObjectsLockedTexture clear
editor.savelevel 0
```

### Workflow E: Preparing Levels for Joining

Before using `editor.joinlevels`, the four levels must be synchronized:

```
// Step 1: Sync textures on all four levels
// Load each level and run the sync script
editor.LoadLevel Map_E03.lnd
Editor.LoadRightConnectedLevel
Editor.LoadBottomConnectedLevel
Editor.CopyEdgeFromConnected
Editor.CopyColorFromConnected
Editor.CopyTexturesFromConnected
Editor.SaveAllLevels

// Repeat for Map_F03, Map_E04, Map_F04...

// Step 2: Join
editor.joinlevels Map_E03.lnd Map_F03.lnd Map_E04.lnd Map_F04.lnd Joined_EF34.lnd
```

---

## 19. Parameter Reference

### Color Format

Colors throughout the editor use hexadecimal `0xAARRGGBB` format:

| Component | Position | Range |
|-----------|----------|-------|
| Alpha (A) | Bits 24-31 | 00 (transparent) — FF (opaque) |
| Red (R) | Bits 16-23 | 00-FF |
| Green (G) | Bits 8-15 | 00-FF |
| Blue (B) | Bits 0-7 | 00-FF |

Common values:
| Color | Hex |
|-------|-----|
| White opaque | `0xFFFFFFFF` |
| Black opaque | `0xFF000000` |
| Black transparent | `0x00000000` |
| Red opaque | `0xFFFF0000` |
| Green opaque | `0xFF00FF00` |
| Blue opaque | `0xFF0000FF` |
| Yellow opaque | `0xFFFFFF00` |

### Height / Altitude Units

The Two Worlds editor uses a grid-based height system:

| Unit | Relation |
|------|----------|
| 1 grid unit | 16 game units vertically |
| Ground level | z = 0 (or the current terrain height) |
| z-to-ground conversion | `z - ground = 16 × 256` |

For heightmap import:
- `StartAltitudeG` must be ≥ 2
- `StartAltitudeG + HeightScaleG` must be < 128
- These are in grid units, so the total height range is about 126 grid units (≈ 2016 game units)

### Coordinate Systems

| Context | Unit | Note |
|---------|------|------|
| Level coordinates | Grid units | Used by SetCreateRect, heightmaps |
| Object coordinates | World units | Used by createEd |
| "Small coordinates" | Triggered when range > 32 | Used in CreateObjectsOnArea, SetTextureOnObjects |
| Edge margins | Game units | 32 = 0.5m, 256 = 4m |

### standMask Bitfield

Used in `CreateObjectsOnArea` and related commands:

| Bit | Value | Effect |
|-----|-------|--------|
| 0-2 | `0x7` | Glue to ground (snap to terrain) |
| 8 | `0x100` | Box to lowest ground (align bounding box bottom) |

These can be combined: `0x107` = glue to ground + box to lowest.

### Grass System

| Property | Value |
|----------|-------|
| Index range | **1 to 8** (not 0!) |
| Special index | `-1` = all grasses |
| Quantity range | -1.0 (full remove) to 1.0 (full density) |
| Blur steps | Higher = smoother, 10 is a good default |
| Clamp limit | 0.0 to 1.0 (density cap) |

---

## 20. Tips & Gotchas

### Common Mistakes

1. **Grass index 0**: Grass indices start at 1. Using 0 produces errors or silent failures.

2. **Forgetting to save**: After any batch operation, always include `editor.savelevel 0` or `Editor.SaveAllLevels`. Unsaved changes are lost when the editor loads the next level.

3. **Order matters in scripts**: The level sync workflow (`edtex.txt`) must load connected levels *before* copying from them. Copy operations must run *before* save.

4. **Texture sync before joining**: `editor.joinlevels` assumes all four levels use the same texture set. Joining unsynchronized levels produces texture glitches.

5. **ResetCreateObjectsOnArea**: Always reset after object placement to avoid leftover constraints affecting future operations.

6. **Heightmap altitude limits**: StartAltitudeG must be ≥ 2 and StartAltitudeG + HeightScaleG must be < 128. Exceeding these causes terrain corruption.

7. **foreachlevel script location**: Script files referenced by `@filename.txt` must be in the editor's working directory (usually the Game folder), not in the level folder.

8. **"Small coordinates" threshold**: When range values in object placement commands exceed 32, the engine switches to a different coordinate scale. This is not well-documented and can produce unexpected results if you're not aware of it.

### Performance Tips

- Use `Editor.ClampGrassToLimit` to cap grass density. Excessive grass is the primary performance killer.
- `Editor.DeleteObjectsOnEdgesMargin 64` prevents redundant objects at level borders.
- `Editor.CleanupInvisibleTextures 1` removes zero-alpha texture layers, reducing file size and draw calls.
- Process levels in batches with `foreachlevel` instead of manually — it's faster and ensures consistency.

### Debugging Tips

- Use `editor.setwaterh` without parameters to check current water height
- Use `Editor.SetDrawMapMarkers` and `Editor.SetDrawMapObjects` to visualize placement
- Use `editor.SaveLevelBmp` to export and inspect levels visually
- Use `editor.foreachlevel editor.TraceUsedObjects output.txt` to audit object usage
- Use `Stats.PE`, `Stats.ObjCnt`, `Stats.MemCnt` to monitor performance
- Use `display.FPS` to show framerate while testing

### Workflow Best Practices

1. **Always work on copies**: Before running batch scripts on the entire world, back up your level files.

2. **Test on one level first**: Before using `foreachlevel`, test your script on a single level with `editor.LoadLevel`.

3. **Script in stages**: Separate terrain, texture, grass, and object operations into individual scripts. Run them in order rather than combining everything into one massive script.

4. **Save often**: Include save commands at the end of every script.

5. **Lock before auto-operations**: Use `Editor.LockTexture` to protect road/path textures before auto-texturing. Use `editor.AddCreateObjectsLockedTexture` to keep objects off roads before auto-placing.

6. **Clean up last**: Run cleanup operations (FixupTextureEdges, CleanupInvisibleTextures, RemoveGrassWhereWater) as the final step after all creative work is done.

7. **Sync borders after changes**: Any change to terrain, textures, or colors near level edges requires running the connected level sync workflow.

---

## Appendix: Quick Command Reference

### Most-Used Commands

| Command | Purpose |
|---------|---------|
| `editor.savelevel 0` | Save current level |
| `Editor.SaveAllLevels` | Save all loaded levels |
| `editor.SaveLevelBmp` | Export level as BMP |
| `editor.LoadLevel file.lnd` | Load a level |
| `Editor.MakeAverageAltitude range factor` | Smooth terrain |
| `Editor.AddZToAll offset` | Raise/lower entire level |
| `editor.setwaterh height` | Set water height |
| `Editor.FixupTextureEdges` | Fix texture seams |
| `Editor.CleanupInvisibleTextures 1` | Remove hidden textures |
| `Editor.DeleteBadMarkers` | Remove invalid markers |
| `Editor.DeleteObjectsOnEdges` | Remove border objects |
| `Editor.RemoveGrassWhereWater` | Remove underwater grass |
| `Editor.BlurGrass -1 10` | Smooth all grass |
| `editor.foreachlevel @script.txt` | Run script on all levels |

### File Locations

| File Type | Location |
|-----------|----------|
| Heightmap BMPs | `game\Editor\Heightmaps\` |
| Heightmap RAWs | `game\Editor\Heightmaps\` |
| Batch scripts | Editor working directory (`Game\` folder) |
| Level files (.lnd) | `game\Data\Levels\` or mod folder |
| Texture files (.dds) | `game\Data\terrains\` |
| Grass textures | `game\Data\grasses\` |
| ParticleEdit output | `Z:\Game\ParticleEditUsedFiles.txt` |

---

*This guide was compiled from Reality Pump's internal SDK documentation and reverse engineering of the Two Worlds Editor. For the latest tools and utilities, visit the TW Modding Community.*
