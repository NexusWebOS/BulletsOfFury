PixelLab masters and source-preserving Aseprite export.

GENERATIONS.json records the actual jobs, seeds, selected candidate, costs and normalization; briefs summarize the generation requests. inputs.json holds exact measured pivots, angle corrections, selected poses and native smoke crop sources. Provider rotation was not a uniform full turn; the valid first-half views supply32 normalized angles with their offline-rotated opposites. All source masters, editable .aseprite banks and hashed output manifest are retained. Runtime uses fixed-cell source-over blits only.
