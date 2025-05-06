#!/usr/bin/env bash
set -euo pipefail

DATA="$HOME/smplifyx_data"
IMAGE="humanoidsctu/smplifyx:internal_pipeline"

docker run --rm \
  -v "$DATA":/workspace/data \
  "$IMAGE" \
  bash -c "
    cd /home/infant_pose_estimation/smplify-x-master && \
    python smplifyx/main.py \
      --config cfg_files/fit_smplx.yaml \
      --img_folder /workspace/data/images \
      --keyp_folder /workspace/data/keypoints \
      --output_folder /workspace/data/out \
      --model_folder /home/infant_pose_estimation/smplx-main/models \
      --model_type smplx \
      --vposer_ckpt /home/infant_pose_estimation/vposer_models \
      --gender male \
      --use_cuda False \
      --visualize False \
      --save_meshes True \
      --result_folder /workspace/data/out \
      --focal_length 432
  "
