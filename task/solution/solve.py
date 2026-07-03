"""Oracle reference solution.

Repairs the CPU software renderer by restoring correct implementations
of the coverage, perspective-interpolation, and depth-reconstruction
stages, then re-renders every scene to /app/output/.
"""

import os
import shutil
import subprocess
import sys

SOLUTION_DIR = os.path.dirname(os.path.abspath(__file__))
FIXED_DIR = os.path.join(SOLUTION_DIR, "fixed_renderer")
RENDERER_DIR = "/app/renderer"

FIXED_FILES = ["geometry.py", "interpolation.py", "depth.py", "rasterizer.py"]


def main():
    for fname in FIXED_FILES:
        src = os.path.join(FIXED_DIR, fname)
        dst = os.path.join(RENDERER_DIR, fname)
        shutil.copyfile(src, dst)

    pycache = os.path.join(RENDERER_DIR, "__pycache__")
    if os.path.isdir(pycache):
        shutil.rmtree(pycache)

    env = os.environ.copy()
    env["OUTPUT_DIR"] = "/app/output"

    subprocess.run(
        [sys.executable, "main.py"],
        cwd=RENDERER_DIR,
        env=env,
        check=True,
    )


if __name__ == "__main__":
    main()