#!/bin/sh
# Kullanım: sh tools/yayinla.sh "commit mesajı"
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
git add -A
git -c user.name="isatosun1073" -c user.email="isatosun1073@users.noreply.github.com" commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01S576Zj48hM72imku9vDUVN"
git push -q origin main
echo "yayında: $1"
