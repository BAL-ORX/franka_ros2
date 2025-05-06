#!/usr/bin/env bash
# ------------------------------------------------------------------
# Run the OpenPose pipeline on the *current* contents of
#   ~/Bachelor Thesis/smplifyx-and-openpose-containers/data/images
# ------------------------------------------------------------------
set -euo pipefail

OPENPOSE_ROOT="$HOME/Bachelor Thesis/smplifyx-and-openpose-containers"

cd "$OPENPOSE_ROOT"
./run_openpose.sh     