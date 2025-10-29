# Repository Guidelines

## Project Structure & Module Organization
- Root scripts: `xyz_stage_control.py` handles the 3-axis demo, `circle.py` explores motion patterns, and `test.py` provides an integration smoke test.
- The core driver lives in `pyOptoSigma/pyOptoSigma.py`; companion usage examples sit in `pyOptoSigma/Double_test.py` and `pyOptoSigma/NotTCP_test.py`.
- Sphinx docs and mirrored samples reside under `pyOptoSigma/source/` and `pyOptoSigma/source/custom_scripts/`.
- TCP bridge and helper utilities are bundled with the library (`pyOptoSigma/tcp_server.py`, etc.), so keep related changes co-located.

## Build, Test, and Development Commands
- `uv sync` — create the local environment and install `pyserial` per `pyproject.toml`; run after cloning or updating dependencies.
- `uv run python xyz_stage_control.py` — exercise the standard 3-axis workflow (adjust the COM port before use).
- `uv run python test.py` — run the verbose integration script to verify velocity/position APIs end-to-end.
- Without `uv`, install locally via `python -m pip install -e pyOptoSigma` and invoke the scripts with `python ...`.

## Coding Style & Naming Conventions
- Follow PEP 8: 4-space indentation, snake_case for functions, UPPER_CASE for module constants, and descriptive Enum members (e.g., `OSMS26_100`).
- Keep controller and stage identifiers aligned with the OptoSigma manuals; expand enums with consistent prefixes.
- Prefer explicit waits (`wait_for_finish=True`) and note timing-sensitive sleeps with concise comments tied to hardware behavior.

## Testing Guidelines
- Hardware-in-the-loop checks live in `*_test.py`; keep new scenarios alongside the scripts they exercise.
- Before publishing, run `uv run python test.py` with the target controller connected and capture console output for the PR.
- Record required COM ports, travel bounds, and safety interlocks at the top of each test script to aid reviewers.

## Commit & Pull Request Guidelines
- Mirror the existing concise, imperative commit style (`fix wait_for_finish`, `3軸同時テスト`), adding bilingual context when it improves clarity.
- Reference affected hardware or axes in the body when changes rely on specific physical setups.
- PRs should list purpose, setup steps, linked issues, and evidence (logs/screenshots) of successful motion or communication tests.

## Serial & Safety Notes
- Call `stages.initialize()` before issuing moves; an `NG` response usually means the controller is still busy.
- Zero the stage with `set_origin()` after large moves and document any non-default speed profiles you activate.
