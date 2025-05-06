#!/usr/bin/env bash
# ------------------------------------------------------------------
# Copy the *most recent* OpenPose keypoints JSON **and** its image
#   from …/data/{keypoints,images}
#   into  ~/smplifyx_data/{keypoints,images}
# ------------------------------------------------------------------
set -euo pipefail
shopt -s nullglob

SRC_BASE="$HOME/Bachelor Thesis/smplifyx-and-openpose-containers/data"
DST_BASE="$HOME/smplifyx_data"

src_img_dir="$SRC_BASE/images"
src_kp_dir="$SRC_BASE/keypoints"

dst_img_dir="$DST_BASE/images"
dst_kp_dir="$DST_BASE/keypoints"

# find newest JPEG in images/
imgs=("$src_img_dir"/*.jpg)
[[ ${#imgs[@]} -eq 0 ]] && { echo "❌  No images in $src_img_dir" >&2; exit 1; }
latest_img="$(ls -t "${imgs[@]}" | head -n1)"

# find newest keypoints JSON in keypoints/
kps=("$src_kp_dir"/*_keypoints.json)
[[ ${#kps[@]} -eq 0 ]] && { echo "❌  No keypoints in $src_kp_dir" >&2; exit 1; }
latest_kp="$(ls -t "${kps[@]}" | head -n1)"

# make destination dirs
mkdir -p "$dst_img_dir" "$dst_kp_dir"

cp "$latest_img" "$dst_img_dir/"
cp "$latest_kp"  "$dst_kp_dir/"

echo "✅  Copied $(basename "$latest_img") → $dst_img_dir"
echo "✅  Copied $(basename "$latest_kp")  → $dst_kp_dir"
