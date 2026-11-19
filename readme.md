### Check if DLS working
```bash
gst-inspect-1.0 gvadetect
```

### Sample 1 Run a pipeline
```bash
gst-launch-1.0 \
  filesrc location=./1192116-sd_640_360_30fps.mp4 ! \
  decodebin3 ! \
  gvadetect model=./models/yolo11n/FP16/yolo11n.xml device=GPU ! \
  queue ! \
  gvawatermark ! \
  gvafpscounter ! \
  videoconvert ! autovideosink sync=false
```

### Sample 2 Out put to JSON
```
gst-launch-1.0 \
  filesrc location=./1192116-sd_640_360_30fps.mp4 ! \
  decodebin3 ! \
  gvadetect model=./models/yolo11n/FP16/yolo11n.xml device=GPU ! \
  queue ! \
  gvafpscounter ! \
  gvametaconvert format=json ! \
  gvametapublish file-format=json-lines file-path=output.json ! fakesink async=false
```

### Sample 3 See detect.py
```bash
python3 detect.py
```