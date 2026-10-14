#!/usr/bin/env bash
# Installs the amnesia-gitster theme and prompt-color-picker into oh-my-zsh's custom dir.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

mkdir -p "$CUSTOM/themes" "$CUSTOM/prompt-color-picker"
cp "$SRC/amnesia-gitster.zsh-theme" "$CUSTOM/themes/"
cp "$SRC/prompt-color-picker.zsh" "$CUSTOM/"
cp "$SRC/prompt-color-picker/server.py" "$CUSTOM/prompt-color-picker/"

echo "Installed. Set ZSH_THEME=\"amnesia-gitster\" in ~/.zshrc, then open a new terminal."
