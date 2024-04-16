
import logging


LOG_LEVEL_MAP = { #  map from mpv to built-in log levels
    "fatal": logging.CRITICAL,
    "error": logging.ERROR,
    "warn": logging.WARNING,
    "info": logging.INFO,
    "v": logging.DEBUG,
    "debug": logging.DEBUG,
    "trace": logging.DEBUG,
}
MEDIA_TYPE_EMOJI_MAP = {
    "text": "🔤",
    "image": "🖼",
    "video": "📽",
    "audio": "🎶"
}