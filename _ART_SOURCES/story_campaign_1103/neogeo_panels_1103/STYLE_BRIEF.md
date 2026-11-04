# Neo-Geo color-animation direction

Mike requested the color and shading of BOF's pilot intro. The existing aintro plates were exported from the actual game and inspected; they supply the saturated light/dark ramps and technological atmosphere. The opener also uses spotlight beds, rushing streaks and stepped colored bars. These references inform the background only. Cole remains the olive/blue-eyed pilot and Maverick remains neon green with aviators.

The new generated nine-theme sheet uses wide diagonal energy ribbons, near-black shadows, bright multi-band highlights and pixel dithering. Each native 96 x 96 tile uses 16 shared shades. Mirrored source repetition joins equal edge pixels. Source translation and gentle index-ramp color cycles are baked into 24 frames per pilot at 12fps. Runtime selects native frames; no gradient, blend, blur, color filter or opacity effect is added.
