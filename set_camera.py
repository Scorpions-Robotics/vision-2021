import os


def set_camera():
    os.system(
        "v4l2-ctl --set-fmt-video=width=800,height=600,pixelformat=0 --set-parm=30 -c exposure_auto=1 -c exposure_absolute=3"
    )
