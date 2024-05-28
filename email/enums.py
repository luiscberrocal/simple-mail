from enum import Enum


class EmailFormat(str, Enum):  # noqa: D101
    TEXT = "plain"
    HTML = "html"
