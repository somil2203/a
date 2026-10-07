#!/usr/bin/env bash
# One-shot HyperFrames setup for a fresh cloud container.
# Installs the CLI, downloads Chrome Headless Shell, and checks the install.
# The agent skills are committed under .claude/skills, so they load automatically.
set -euo pipefail
npm i -g hyperframes
hyperframes browser ensure
hyperframes doctor || true
