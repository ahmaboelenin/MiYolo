import os
import sys
from time import sleep
from threading import Thread, enumerate
from cv2 import cv2
from PIL import Image, ImageTk
import numpy as np
import requests
import mimetypes
import validators
import pafy
import screeninfo


class ThreadedTask(Thread):
    def __init__(self, target, args=None):
        if args is not None:
            super().__init__(target=target, args=(args, ), daemon=True)
        else:
            super().__init__(target=target, daemon=True)
        self.start()


def resource_path(relative_path):
    import os
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except:
        base_path = os.path.abspath("GUI")
    return os.path.join(base_path, relative_path)


def get_os():
    if os.name == 'nt':
        # Windows
        return 'win'
    else:
        return 'linux'


"""____Monitors_Functions___"""


def get_monitor_size(monitor='primary'):
    monitors = screeninfo.get_monitors()

    if monitor == 'primary':
        for monitor in monitors:
            if monitor.is_primary:
                return monitor.width, monitor.height
    else:
        for monitor in monitors:
            if not monitor.is_primary:
                return monitor.width, monitor.height


def get_monitor_coord(monitor='primary'):
    monitors = screeninfo.get_monitors()

    if monitor == 'primary':
        for monitor in monitors:
            if monitor.is_primary:
                return monitor.x, monitor.y
    else:
        for monitor in monitors:
            if not monitor.is_primary:
                return monitor.x, monitor.y


def get_monitor_info(monitor='primary'):
    monitors = screeninfo.get_monitors()

    if monitor == 'primary':
        for monitor in monitors:
            if monitor.is_primary:
                return monitor.x, monitor.y, monitor.width, monitor.height
    else:
        for monitor in monitors:
            if not monitor.is_primary:
                return monitor.x, monitor.y, monitor.width, monitor.height


def get_monitor_center(monitor='primary'):
    if monitor == 'primary':
        x, y, width, height = get_monitor_info('primary')
    else:
        x, y, width, height = get_monitor_info('secondary')
    return x + int(width/2), y + int(height/2)


"""____Media_Functions___"""


def check_frame_shape(height, width, monitor):
    max_width, max_height = get_monitor_size(monitor)
    max_width, max_height = max_width - 270, max_height - 80

    ratio = height / width
    if ratio < 1:
        if width > max_width:
            width, height = max_width, int(max_width * ratio)
        if height > max_height:
            width, height = int(max_height / ratio), max_height
        return width, height
    else:
        if height > max_height:
            width, height = int(max_height / ratio), max_height
        if width > max_width:
            width, height = max_width, int(max_width * ratio)
        return width, height


def is_media_file(file_name):
    """This function assume the file type by its extension and don't open the actual file, it is based only on the file
    extension"""
    mimetypes.init()

    mime_start = mimetypes.guess_type(file_name)[0]

    if mime_start is not None:
        mime_start = mime_start.split('/')[0]

        if mime_start in ['video', 'image']:
            return True
    return False


def get_media_type(file_name):
    from pymediainfo import MediaInfo

    media_info = MediaInfo.parse(file_name)
    for track in media_info.tracks:
        if track.track_type in ['Video', 'Image']:
            return track.track_type.lower()
    return False


def is_image_url(url):
    response = requests.get(url)
    if response.headers["content-type"].split('/')[0] == 'image':
        image = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    return False


def get_media(link):
    if validators.url(link):
        media = is_image_url(link)
        if media:
            media_type = 'image'
        else:
            media = load_video_from_youtube_url(link)
            if media:
                media_type = 'video'
            else:
                media_type = 'unsupported-url'
    else:
        media_type = get_media_type(link)
        if media_type == 'image':
            media = load_image(link)
        elif media_type == 'video':
            media = load_video(link)
        else:
            media = None
            media_type = 'unsupported-file'
    return media_type, media


"""____Load_Media_Functions___"""


def load_video_from_youtube_url(url):
    """Creates a new video streaming object to extract video frame by frame to make prediction on.
    :return: opencv2 video capture object, with lowest quality frame available for video."""
    try:
        play = pafy.new(url).streams[-1]
        assert play is not None
    except ValueError:
        return
    return cv2.VideoCapture(play.url)


def load_video(path):
    """Creates a new video streaming object to extract video frame by frame to make prediction on.
    :return: opencv2 video capture object."""
    return cv2.VideoCapture(path)


def load_image(path):
    image = cv2.imread(path)
    return image

