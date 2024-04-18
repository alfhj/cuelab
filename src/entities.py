
from enum import Enum


class CueType(Enum):
    TEXT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4


class Cue:
    type_emoji_map = {
        CueType.TEXT: "🔤",
        CueType.IMAGE: "🎨",
        CueType.VIDEO: "🎥",
        CueType.AUDIO: "🎵"
    }
    type_text_map = {
        CueType.TEXT: "text",
        CueType.IMAGE: "image",
        CueType.VIDEO: "video",
        CueType.AUDIO: "audio"
    }

    def __init__(self, name: str, type: CueType, duration: float, path: str):
        self.name = name
        self.type = type
        self.duration = duration
        self.path = path

    def get_emoji(self):
        return self.type_emoji_map[self.type]

    def toJSON(self):
        return {
            "name": self.name,
            "type": self.type_text_map[self.type],
            "duration": self.duration,
            "path": self.path
        }

    @classmethod
    def fromJSON(cls, obj: dict):
        type_map = {val: key for key, val in cls.type_text_map.items()}
        return cls(obj["name"], type_map[obj["type"]], obj["duration"], obj["path"])
