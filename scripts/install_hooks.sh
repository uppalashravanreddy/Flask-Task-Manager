#!/usr/bin/env bash
# Install git hooks from git-hooks/ into .git/hooks/
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SOURCE_DIR="$REPO_ROOT/git-hooks"

echo "Installing git hooks from $SOURCE_DIR -> $HOOKS_DIR"

for hook in "$SOURCE_DIR"/*; do
  name="$(basename "$hook")"
  dest="$HOOKS_DIR/$name"
  cp "$hook" "$dest"
  chmod +x "$dest"
  echo "  Installed: $name"
done

echo "Done. Git hooks installed successfully."
