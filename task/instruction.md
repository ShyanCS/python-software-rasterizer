<!--
  This file is the PROMPT handed verbatim to the model that will attempt your task.
  Replace everything in this comment with your task instruction, then delete the comment.

  Guidelines:
  - Write it yourself, as a domain expert. Do NOT generate it with an LLM.
  - It's a prompt, not a document — no title, no section headers, no excessive Markdown.
  - Write it the way you'd brief a skilled colleague.
  - Use absolute paths (e.g. /app/output.txt), never relative paths.
  - Be explicit about every expected output file and its exact format/schema.
  - Include everything the agent needs to solve the task — and nothing more (don't
    hint at or reveal your solution).
  - Keep it concise (<= 1500 tokens). State the goal and required outputs; skip
    backstory, roleplay, and filler.
-->

A CPU software rendering pipeline is implemented in Python under `/app/renderer`. It loads scene definitions (camera, meshes, textures) and renders them to PNG images, but the renderer currently contains defects that produce mathematically incorrect output. Although the rendered images may appear plausible, they do not match the correct rendering of the provided scenes.

Your task is to repair the renderer by correcting the rendering logic. The defects affect multiple stages of the rendering pipeline, and some of them interact, so correcting only part of the pipeline will not be sufficient. Inspect the implementation, identify the underlying causes, and restore correct rendering behavior.

The provided scene definitions, meshes, textures, camera parameters, and other assets under `/app/renderer` are part of the benchmark and must not be modified. Do not change the image resolution, output file names, or output format.

After repairing the renderer, rendering all provided scenes must produce these output files:

* `/app/output/colored_cube.png`
* `/app/output/textured_plane.png`
* `/app/output/overlapping_meshes.png`
* `/app/output/adjacent_triangles.png`

Each output must be a valid PNG in RGB format, with dimensions matching the corresponding scene's camera width and height. Rendering must be deterministic: repeated executions with the same inputs must produce identical outputs.

The generated images will be compared against reference renderings on a per-pixel, per-channel basis, using an absolute tolerance of approximately 0.004 — tight enough to allow for standard 8-bit rounding, but not to hide an incorrect implementation. Superficial approaches such as post-processing rendered images, hardcoding outputs, or special-casing individual scenes are not acceptable. The renderer itself must be corrected so that all provided scenes render correctly.

You have 3600 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.