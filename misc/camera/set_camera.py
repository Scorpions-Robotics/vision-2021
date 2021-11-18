import os
from decouple import config


exposure = config("LINUX_EXPOSURE")


def set_exposure():
    os.system(f"v4l2-ctl -c exposure_auto=1 -c exposure_absolute={exposure}")


def set_format():
    os.system(
        "v4l2-ctl --set-fmt-video=width=800,height=600,pixelformat=0 --set-parm=30 -c exposure_auto=3"
    )
