# Building Block: Configuration and Paths

## Goal

Understand how to load settings and build file paths without hardcoding values.

## Core Ideas

- Keep defaults in code so the app still works when a key is missing.
- Read overrides from a JSON file.
- Resolve paths from a known root directory.
- Validate required files early with clear error messages.

## Configuration Precedence Model

Use explicit precedence so behavior is predictable:

1. In-code defaults.
2. Config file values.
3. Runtime overrides (CLI/GUI arguments).

Document this order and do not change it silently.

## Beginner Implementation Steps

1. Create a default settings dictionary in Python.
2. Locate candidate config file paths.
3. Load the first existing file.
4. Merge loaded settings over defaults.
5. Convert folder settings to Path objects.
6. Check directories/files before processing.

## Path Safety Rules

- Normalize every path with `Path.resolve()` before use.
- Keep all runtime paths anchored to a trusted root.
- Avoid depending on the current working directory.
- Separate read paths and write paths in config to reduce accidental overwrite risks.

## Validation Strategy

1. Validate key presence.
2. Validate value types (string/list/bool).
3. Validate semantic rules (supported extension starts with `.`).
4. Fail fast for invalid configuration that would produce wrong outputs.
5. Fall back only for optional keys.

## Common Mistakes

- Using relative paths from the current terminal directory.
- Failing silently when config keys are missing.
- Assuming packaged and source layouts are identical.

## When To Keep It Simpler

- If the script is single-use and local-only, a small inline config dictionary can be acceptable.
- For reusable or shared tooling, keep file-based config and explicit validation.
