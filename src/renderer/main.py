"""Entry point for the CPU software renderer.

Renders scene JSON files through the full graphics pipeline,
and writes output PNGs to the specified output directory.
"""

import argparse
import glob
import logging
import os
import sys

from renderer import render_scene
from scene import load_scene


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="CPU Software Rasterizer")
    parser.add_argument("--scene", type=str, help="Path to a specific scene JSON file to render")
    parser.add_argument(
        "--outdir", type=str, default="output", help="Directory to save output PNGs"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    scenes_dir = os.path.join(script_dir, "scenes")
    output_dir = os.path.abspath(args.outdir)

    os.makedirs(output_dir, exist_ok=True)

    if args.scene:
        scene_files = [args.scene]
    else:
        scene_files = sorted(glob.glob(os.path.join(scenes_dir, "*.json")))

    if not scene_files:
        logging.error("No scene files found.")
        sys.exit(1)

    logging.info(f"Found {len(scene_files)} scene(s) to render.")

    for scene_file in scene_files:
        scene_name = os.path.basename(scene_file)
        logging.info(f"Rendering: {scene_name}")

        scene_def = load_scene(scene_file)
        render_scene(scene_def, script_dir, output_dir)

    logging.info(f"All scenes rendered successfully to {output_dir}/")


if __name__ == "__main__":
    main()
