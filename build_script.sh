#!/usr/bin/env bash
set -euo pipefail

rime_dir="$HOME/.local/share/fcitx5/rime"

echo "==> Building Rime data for ${rime_dir}"
rime_deployer --build \
    "$rime_dir" \
    /usr/share/rime-data \
    "$rime_dir/build"

echo "==> Restarting fcitx5"
fcitx5-remote -r
sleep 1

echo "==> Switching to rime"
fcitx5-remote -s rime
fcitx5-remote -o

echo "==> Build complete"
ls -l --time-style=+'%Y-%m-%d %H:%M:%S' "$rime_dir/build/jyutping_nc."*
