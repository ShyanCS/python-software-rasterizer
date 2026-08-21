# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Full CPU software rasterizer pipeline: vertex processing, homogeneous clipping, perspective divide, viewport transform, rasterization, fragment shading, depth testing.
- Modular strategy interfaces (`CoverageStrategy`, `DepthStrategy`, `InterpolationStrategy`) via `Protocol` classes in `pipeline_types.py`.
- CLI entrypoint (`src/renderer/main.py`) with `--scene` and `--outdir` arguments.
- Scene loading from JSON files with validation (`SceneLoadError`).
- OBJ mesh loading (`Mesh.load_obj`).
- Texture support: load from file or generate procedural checkerboard.
- Structured logging via `logging_config.py`.
- CI pipeline (GitHub Actions): separate lint (ruff, black) and test (pytest + coverage ≥ 70%) jobs.
- Docker support: `Dockerfile` and `docker-compose.yml` for one-command execution.
- Dependabot configuration for weekly dependency updates.
- Full unit test suite covering camera, clipping, geometry, math3d, mesh, scene, and texture modules.
