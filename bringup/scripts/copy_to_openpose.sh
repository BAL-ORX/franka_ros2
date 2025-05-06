#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Copy the newest RealSense JPEG into the OpenPose images directory.
# Both paths use $HOME so the same script works on host AND container.
# ------------------------------------------------------------------

src="$HOME/Bachelor Thesis/realsense_pictures"
dst="$HOME/Bachelor Thesis/smplifyx-and-openpose-containers/data/images"

shopt -s nullglob               # empty glob → empty array, no literal *
files=("$src"/color_*.jpg)

if (( ${#files[@]} == 0 )); then
  echo "❌  No JPEGs found in \"$src\"." >&2
  exit 1
fi

latest="$(ls -t "${files[@]}" | head -n1)"

mkdir -p "$dst"                 # succeeds now because the path is mounted
cp "$latest" "$dst/"

echo "✅  Copied $(basename "$latest") → \"$dst\""
