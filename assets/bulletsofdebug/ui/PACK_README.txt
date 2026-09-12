BULLETS OF DEBUG! — UI PACK (drop 0912f)
========================================

Generated with SpriteCook against the CF_BossModeAssets Vol.1 pack as a style reference, so the two
editors are visibly siblings: same industrial riveted construction, same bevelled arcade lettering,
same chunky pixel outlines. The ONE deliberate difference is the accent colour — Boss Mode is
orange/amber, Bullets of Debug is electric cyan/teal — so you can tell at a glance which editor a
screenshot came from.

FILES
-----
logo.png        1319x665   the "BULLETS OF DEBUG!" wordmark on its machine frame
window.png       973x814   a HOLLOW nine-patch window frame — the interior is genuinely
                           transparent, so the editor draws its own content inside
buttons.png     1001x1002  6 labels x 3 states  (idle / hover / pressed)
cursors.png     1024x1024  16 cursors, 4x4
icons.png       1024x1024  25 toolbar icons, 5x5
cur_*.png         32px     the 16 cursors cut out individually, for CSS `cursor:url(...)`
*.json                     cut maps in the SAME shape assets/bossmode/bossmode.js already reads
cursors_hotspots.json      per-cursor hotspot in the cut file's own pixels

THE CUT MAPS
------------
Each <name>.json matches the format loadAtlas/rectOf/cellRule in assets/bossmode/bossmode.js
expects:

    { asset, frame_count, atlas:{columns, rows, cell, rects:[{frame,x,y,w,h}]},
      items:[{index, name, source_rect, placement, visible_size}] }

rectOf(sheet, itemName) finds items[i] by NAME and returns atlas.rects[i] at the same index, so the
two arrays are parallel. That means the editor can reuse the Boss Mode CSS generator unchanged —
point it at this folder and the rules build themselves.

NAMES
-----
buttons   spawn / waves / enemy / stage / sprite / apply,
          each also as -hover and -down          (18)
cursors   pointer pointer-active link text
          move grab grabbing precision
          resize-horizontal resize-vertical resize-nwse resize-nesw
          rotate zoom-in zoom-out unavailable    (16)
icons     enemy waves projectile background background-alt
          play pause stop reload reload-alt
          target fov select path path-alt
          save open export import delete
          brush eyedropper grid settings settings-alt   (25)

TRAPS, RECORDED SO THEY ARE NOT REDISCOVERED
--------------------------------------------
1. NEITHER SPRITECOOK URL IS USABLE ALONE.
   pixel_url has real alpha but is smart-cropped and downscaled — the window came back 98x98 from a
   2K render, and the button sheet came back as a 92px-wide sliver of a 6x3 grid.
   raw_url is full resolution but has NO alpha: transparency is rendered as a light grey
   CHECKERBOARD, which a luminance key bakes into the sprite.
   _BUILD_SOURCE/sc_fetch.py handles both: it takes colour from raw and alpha from pixel, or with
   --keycheck floods the checkerboard out of raw from the borders inward. A hollow nine-patch like
   window.png also needs --centre, or the enclosed interior never gets reached and comes back
   opaque white.

2. SLICE BY GRID, NOT BY ALPHA ISLAND.
   The first cut used island segmentation. It matched on buttons (18/18) and failed on cursors —
   19 pieces for 16 cursors, because the accent burst beside the active arrow, the I-beam's serifs
   and the rotate arrow's plus are each their own island. Both sheets are perfectly regular
   lattices; the grid is the slicer, and each cell is then trimmed to its own ink.

3. THE ICON SHEET IS 5x5, NOT THE 5x4 THAT WAS ASKED FOR.
   The generator added a fifth column of variants (a second landscape, a cyan reload, a second
   path, a second gear). They are kept and named -alt. The name list reflects what the art IS, not
   what the prompt requested — which is why the slicer refuses to write a map whose cell count does
   not match its names.

REGENERATING
------------
  python _BUILD_SOURCE/sc_fetch.py out.png --raw <url> --pixel <url>      # colour+alpha
  python _BUILD_SOURCE/sc_fetch.py out.png --keycheck [--centre] --raw <url>
  python _BUILD_SOURCE/bod_pack_map_0912f.py --check                       # cut, report, write nothing
  python _BUILD_SOURCE/bod_pack_map_0912f.py                               # write the maps
