# Explore the shared midpoint

[Download the offline explorer ZIP](https://raw.githubusercontent.com/DannyExperiments/characteristic-imset-sink-counterexample/v1.0.0/visualization/characteristic-imset-sink-counterexample-explorer.zip), extract it, and open index.html. Select D, T, U or V to inspect its arrows and the three varying imset coordinates. Drag Rotate to turn the affine plane.

The left graph highlights vertex 2. In D both arcs there point out, while in T they point in. The right diagram shows the actual affine plane of the four imsets. Relative to T, two equal coordinates turn on together (123 and 0123) and a third coordinate (024) varies independently. Their directions have lengths proportional to the square root of 2 and 1. The amber segment D–T and the mint segment U–V pass through the same white dot. A supporting face containing the dot would contain all four endpoints.

The graphic illustrates the exact witness. The paper supplies the general lift and the finite minimality check.

To render the GIF, use an existing Python environment with Pillow and Arial or DejaVu Sans available.

    python3 visualization/render.py
