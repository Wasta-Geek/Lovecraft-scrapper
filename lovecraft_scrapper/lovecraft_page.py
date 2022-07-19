"""Manage a Lovecraft page and it's parsing"""

import bs4
from .page import Page


class LovecraftPageUnavailable(RuntimeError):
    """
    Raised when the given website cannot be opened
    """


class LovecraftPage(Page):
    """
    A class to represent a Lovecraft page
    """

    def _fill_page_info(self) -> None:
        """

        """
        soup = bs4.BeautifulSoup(self._raw_webpage_content, 'html.parser')
        page_layout_div = soup.find('div', class_='pagelayout')
        navigation_tr = page_layout_div.find_next('tr')
        title_tr = navigation_tr.find_next_siblings('tr')[0]
        main_text_tr = title_tr.find_next('tr')

        title_text = title_tr.get_text().lstrip("\n")
        # main_text = main_text_tr.get_text()
        self._page_info.title = title_text

        center_list = main_text_tr.find_all("center")
        # blockquotes_list = main_text_tr.find_all("blockquote")

        chapter_list = []
        for center_element in center_list:
            if center_element.parent.name == "br":
                center_element_text = center_element.get_text()
                if center_element_text.find("\n") == -1:
                    chapter_list.append(center_element_text)
        self.page_info.chapter_count = len(chapter_list)
        print(self.page_info.url)
        print(self.page_info.title)
