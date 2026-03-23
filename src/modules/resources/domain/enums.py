from enum import Enum


class MediaType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    TEXT = 'text'
    OTHER = 'other'
