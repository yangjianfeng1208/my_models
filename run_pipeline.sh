#!/bin/bash
# Usage: ./run_pipeline.sh [processes] [streams_per_process] [batch_size]

cd "$(dirname "$0")"

PROCS=${1:-1}
STREAMS=${2:-1}
BATCH=${3:-1}

cleanup() { kill $(jobs -p) 2>/dev/null; wait; }
trap cleanup INT TERM

for ((p = 0; p < PROCS; p++)); do
  cmd=(gst-launch-1.0)
  for ((s = 0; s < STREAMS; s++)); do
    cmd+=(
      filesrc location=./1192116-sd_640_360_30fps.mp4 !
      decodebin3 !
      gvadetect model=./models/yolo11n/FP16/yolo11n.xml device=GPU
        pre-process-backend=va-surface-sharing batch-size="$BATCH" model-instance-id="inst${p}" !
      queue !
      gvawatermark !
      gvafpscounter !
      fakesink async=false
    )
  done
  "${cmd[@]}" &
done

wait
