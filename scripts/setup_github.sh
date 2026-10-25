#!/usr/bin/env bash
# Menyiapkan repository GitHub: branch main berisi .gitignore saja, lalu dikirim ke remote.
# Pemakaian:  bash scripts/setup_github.sh https://github.com/USERNAME/NAMA-REPO.git
set -euo pipefail

REMOTE="${1:-}"
if [ -z "$REMOTE" ]; then
  echo "Pemakaian: bash scripts/setup_github.sh <URL-repository-GitHub>"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
cp "$ROOT/.gitignore" "$TMP/.gitignore"
cd "$TMP"
git init -q -b main
git add .gitignore
git commit -q -m "Inisialisasi repository: .gitignore"
git remote add origin "$REMOTE"
git push -u origin main
echo
echo "Selesai. Branch main sudah ada di GitHub."
echo "Sekarang tiap anggota mengikuti docs/PANDUAN_GITHUB.md (Langkah 1)."
rm -rf "$TMP"
