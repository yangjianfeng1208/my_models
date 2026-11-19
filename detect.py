import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst
import os

Gst.init([])

video_uri = Gst.filename_to_uri(os.path.join(os.path.dirname(__file__), "1192116-sd_640_360_30fps.mp4"))
model = os.path.expanduser("./models/yolo11n/FP16/yolo11n.xml")
pipeline = Gst.parse_launch(f"""
    urisourcebin buffer-size=4096 uri={video_uri} !
    decodebin3 !
    gvadetect model={model} device=GPU !
    queue !
    gvafpscounter !
    gvametaconvert format=json !
    gvametapublish file-format=json-lines file-path=output_from_python.json ! fakesink async=false
""")

pipeline.set_state(Gst.State.PLAYING)
bus = pipeline.get_bus()
bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS | Gst.MessageType.ERROR)
pipeline.set_state(Gst.State.NULL)