#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_ROOT="$REPO_ROOT/integrations/codex/seal-private-operations-v3"
RUNTIME_ROOT="$SKILL_ROOT/runtime"

python3 -m venv "$RUNTIME_ROOT/.venv"
PYTHON_BIN="$RUNTIME_ROOT/.venv/bin/python"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r "$REPO_ROOT/.devcontainer/requirements-workbench.txt"
"$PYTHON_BIN" -m pip install -e "$RUNTIME_ROOT" --no-deps
"$PYTHON_BIN" -m playwright install --with-deps chromium
npm install -g @openai/codex
npm ci --ignore-scripts --prefix "$RUNTIME_ROOT/tools"
node "$RUNTIME_ROOT/tools/node_modules/bun/install.js"
"$PYTHON_BIN" "$SKILL_ROOT/scripts/patch_redbook_runtime.py"

if [[ ! -f "$RUNTIME_ROOT/web/frontend/dist/index.html" ]]; then
  npm ci --ignore-scripts --prefix "$RUNTIME_ROOT/web/frontend"
  npm run build --prefix "$RUNTIME_ROOT/web/frontend"
fi
mkdir -p "$REPO_ROOT/.codex-runtime"
if [[ ! -f "$RUNTIME_ROOT/.env" ]]; then
  if [[ -f "$RUNTIME_ROOT/.env.example" ]]; then
    cp "$RUNTIME_ROOT/.env.example" "$RUNTIME_ROOT/.env"
  else
    touch "$RUNTIME_ROOT/.env"
  fi
  chmod 600 "$RUNTIME_ROOT/.env"
fi
printf '%s\n' 'Workspace installed. Run codex login --device-auth to connect your own Codex account.'
