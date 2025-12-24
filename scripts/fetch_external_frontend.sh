#!/usr/bin/env bash
set -euo pipefail
REPO_URL="https://github.com/sidpan89/aura-guard"
TARGET_DIR="external/aura-guard"

echo "[info] Preparing directory ${TARGET_DIR}" >&2
mkdir -p external

if [ -d "${TARGET_DIR}/.git" ]; then
  echo "[info] Repository already present; pulling latest" >&2
  git -C "${TARGET_DIR}" pull --ff-only
else
  echo "[info] Cloning ${REPO_URL} into ${TARGET_DIR}" >&2
  git clone "${REPO_URL}" "${TARGET_DIR}"
fi

echo "[info] Set FRONTEND_DIR=${TARGET_DIR} in your .env to use the external UI" >&2
