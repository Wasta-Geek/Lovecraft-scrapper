"""Contains PageInfo class"""

from dataclasses import dataclass
from typing import Union


def get_letter_count(text: str) -> int:
    """
Count the number of letters in a given text
    :param text:
    :return:
    """
    return len(text)


def get_word_count(text: str) -> int:
    """
    Count the number of words in a given text
    :param text:
    :return:
    """
    return len(text.split())


@dataclass
class BaseTextInfo:
    """
    Class model that represents available info for any generic text
    """
    letter_count: int = 0
    word_count: int = 0

    def feed_info(self, letter_count: int, word_count: int) -> None:
        """
        Add to the current class variables the respective letter/word_count values
        :param letter_count:
        :param word_count:
        :return:
        """
        self.feed_letter(letter_count)
        self.feed_word(word_count)

    def feed_letter(self, letter_count: int) -> None:
        """
        Add to the current class variable the letter_count value
        :param letter_count:
        :return:
        """
        self.letter_count = self.letter_count + letter_count

    def feed_word(self, word_count: int) -> None:
        """
        Add to the current class variable the word_count value
        :param word_count:
        :return:
        """
        self.word_count = self.word_count + word_count


def compute_average_info(list_object: [BaseTextInfo]) -> Union[int, int]:
    """
    Computer all average info for a list of BaseTextInfo given
    :param list_object:
    :return:
    """
    paragraph_count = len(list_object)
    average_word = 0.0
    average_letter = 0.0
    for info in list_object:
        average_letter = average_letter + info.letter_count / paragraph_count
        average_word = average_word + info.word_count / paragraph_count
    return int(average_letter), int(average_word)


@dataclass
class ParagraphInfo(BaseTextInfo):
    """
    Class model that represents available info for a given paragraph
    """
    paragraph_content: str = ""

    def append_new_text(self, new_text: str) -> None:
        """
        Append text to the internal_paragraph_content
        :param new_text:
        :return:
        """
        self.paragraph_content = self.paragraph_content + new_text

        self.feed_info(get_letter_count(new_text),
                       get_word_count(new_text))


@dataclass
class ChapterInfo(BaseTextInfo):
    """
    Class model that represents available info for a given chapter
    """
    paragraph_list_object: [ParagraphInfo] = None
    average_word: int = 0
    average_letter: int = 0

    def create_new_paragraph(self, new_paragraph_text: str) -> None:
        """
        Create a new paragraph with the given text
        :param new_paragraph_text:
        :return:
        """
        if self.paragraph_list_object is None:
            self.paragraph_list_object = []
        letter_count = get_letter_count(new_paragraph_text)
        word_count = get_word_count(new_paragraph_text)
        self.paragraph_list_object.append(ParagraphInfo(paragraph_content=new_paragraph_text,
                                                        letter_count=letter_count,
                                                        word_count=word_count))
        self.feed_info(letter_count, word_count)

    def append_text_to_last_paragraph(self, new_text):
        """
        Appends the given text to the last created paragraph
        :param new_text:
        :return:
        """
        if self.paragraph_list_object is not None and self.paragraph_list_object[-1] is not None:
            self.paragraph_list_object[-1].append_new_text(new_text)
            self.feed_info(self.paragraph_list_object[-1].letter_count,
                           self.paragraph_list_object[-1].word_count)

    def compute(self) -> None:
        """
        Compute all the internal info
        :return:
        """
        self.average_letter, self.average_letter = compute_average_info(self.paragraph_list_object)


@dataclass
class PageInfo(BaseTextInfo):
    """
    Class model that represents available info on a given page
    """
    # Page url
    url: str = None
    # Page title
    title: str = None
    # Dict in form chapter_key : [ChapterInfo]
    chapter_dict: dict = None
    # Average letter by chapter
    average_letter: int = 0
    # Average word by chapter
    average_word: int = 0
    # Average paragraph count by chapter
    average_paragraph_count: int = 0

    def create_new_chapter(self, chapter_key: str) -> None:
        """
        Create a new empty chapter (ChapterInfo)
        :param chapter_key:
        :return:
        """
        if self.chapter_dict is None:
            self.chapter_dict = {}
        self.chapter_dict[chapter_key] = ChapterInfo()

    def compute_page(self):
        """
        Compute all available info about page/chapter/paragraph ...
        Should be called at the end of retrieving data
        :return:
        """
        chapter_count = len(self.chapter_dict.keys())
        average_paragraph_count = 0.0
        # Compute each chapter
        for chapter in self.chapter_dict.values():
            chapter.compute()
            # Update letter / word count
            self.feed_info(chapter.letter_count,
                           chapter.word_count)
            # compute average paragraph count
            average_paragraph_count = average_paragraph_count \
                                      + len(chapter.paragraph_list_object) / chapter_count

        self.average_paragraph_count = int(average_paragraph_count)
        self.average_letter, self.average_word = compute_average_info(self.chapter_dict.values())
