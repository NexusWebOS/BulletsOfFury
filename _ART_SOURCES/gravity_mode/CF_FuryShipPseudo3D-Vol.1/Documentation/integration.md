# Integration

- Draw `FuryThrusters256` behind `FuryShip256` only when the current frame marks both engine sockets visible.
- Use 20 FPS (50 ms per frame) for an 800 ms somersault.
- Play frames 01 through 16 for a forward somersault; reverse order after frame 01 for a backward somersault.
- Anchor every ship frame at the center pivot. Keep sprite root motion at zero.
- Use nearest-neighbor sampling, pixel-snapped screen positions, and no mipmaps.
- At 640x360 or 640x480, start with the 128px set at 1x or the 256px set at 0.5x.
- Rotate the world collider continuously using the ship quaternion. Do not derive collision from sprite alpha or swap collider shapes per frame.
- The four missiles are baked as a fully-loaded visual state. Add loaded-state swaps before hiding individual missiles after launch.
