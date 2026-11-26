# Reproduce the checks

Run both scripts with an existing Python 3.11 or compatible interpreter. They use its standard library.

    python3 -B -I scripts/verify_repository.py
    python3 -B -I verification/src/replay.py

The replay computes the four imset supports and checks the exact sink rewrite and midpoint. It checks nine larger connected instances and every possible labeled smaller skeleton. For each distinct changing sink pair through four vertices, it checks an integer functional exposing exactly that pair in the common-coordinate face.

Use Lean 4.30.0 with its bundled standard library for the partial certificate.

    lean -DwarningAsError=true formal/Q911Certificate.lean

The certificate checks the four small DAGs, the sink rewrite, distinct imsets, all midpoint equalities and which coordinates change from D to T. The geometric edge consequence, general lifts and minimality lie outside Lean coverage. [Build the paper](paper/BUILD.md) · [Render the GIF](visualization/README.md)
