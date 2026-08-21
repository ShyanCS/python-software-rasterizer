"""Entry point for the CPU software renderer.

Discovers all scene JSON files in the scenes/ directory, renders each
one through the full graphics pipeline, and writes output PNGs to
the configured output directory (defaults to /app/output/).
"""

import os
import sys
import glob

from scene import load_scene
from renderer import render_scene


def main():
    """Load and render all scenes found in the scenes directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scenes_dir = os.path.join(script_dir, 'scenes')
    output_dir = os.environ.get('OUTPUT_DIR', '/app/output')

    scene_files = sorted(glob.glob(os.path.join(scenes_dir, '*.json')))

    if not scene_files:
        print(f"No scene files found in {scenes_dir}")
        sys.exit(1)

    print(f"Found {len(scene_files)} scene(s) to render.")

    for scene_file in scene_files:
        scene_name = os.path.basename(scene_file)
        print(f"\nRendering: {scene_name}")

        scene_def = load_scene(scene_file)
        render_scene(scene_def, script_dir, output_dir)

    print("\nAll scenes rendered successfully.")


if __name__ == '__main__':
    main()
