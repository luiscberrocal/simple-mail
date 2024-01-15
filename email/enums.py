from enum import Enum


class EmailFormat(str, Enum):
    TEXT = 'plain'
    HTML = 'html'
