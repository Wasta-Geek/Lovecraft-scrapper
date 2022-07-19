"""Contains PageInfo class"""

from dataclasses import dataclass


@dataclass
class PageInfo:
    """
    Class model that represents available info on a given page
    """
    url: str = None
    title: str = None
    chapter_count: int = 0
    average_word_by_chapter: int = 0
    average_word_by_paragraph: int = 0
