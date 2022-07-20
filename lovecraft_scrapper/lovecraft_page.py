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

    @staticmethod
    def __extract_chapter_list(main_text_font_bs4: bs4.BeautifulSoup) -> [str]:
        """
        Scrap the given parameter to extract the chapter list for this webpage
        :param main_text_font_bs4: BeautifulSoup object
        :return: A list of string containing the chapter key (roman numeral)
        """
        center_list = main_text_font_bs4.find_all("center")
        chapter_list = []
        for center_element in center_list:
            center_element_text = center_element.get_text()
            if center_element_text.find("\n") == -1 and center_element_text.strip("—") != "":
                chapter_list.append(center_element_text)
        return chapter_list

    @staticmethod
    def __prepare_html_tree(main_text_font_bs4: bs4.BeautifulSoup) -> None:
        """
        Prepare the html tree and unwrap / edit some tag to be able to be parsed them easily

        :param main_text_font_bs4: BeautifulSoup object
        """
        for i in main_text_font_bs4.select("i"):
            i.unwrap()
        for font in main_text_font_bs4.select("font"):
            element = font
            while element.parent.name != "div" and element.parent.name is not None:
                parent = element.parent
                element.unwrap()
                element = parent
        main_text_font_bs4.smooth()

    def __build_chapter_dict(self, main_text_font_bs4: bs4.BeautifulSoup) -> None:
        """
        Scrap the given  BeautifulSoup object and return a dict containing the chapter (key)
        with all the paragraph associated (values)

        :param main_text_font_bs4: BeautifulSoup object
        :return: dict in the form chapter (key) : paragraph_list (value)
        """
        # Prepare the line list by unwrapping / editing some tag
        LovecraftPage.__prepare_html_tree(main_text_font_bs4)

        # Retrieve chapter list
        chapter_list = LovecraftPage.__extract_chapter_list(main_text_font_bs4)
        chapter_counter = -1

        # Init vars
        new_paragraph = True

        # Iter over the line list
        for string in main_text_font_bs4.strings:
            # Strip some characters
            string_stripped = string.strip("\n").strip('\r').strip("\r\n")
            # Sometimes there is separator lines so we want to skip them
            is_separator_line = string_stripped.strip("—") == ""
            # Check if it's an empty line of a separator line, then we skip
            if len(string_stripped) > 0 and not is_separator_line:
                # Detect if we begin a new chapter
                if chapter_counter < len(chapter_list) - 1 and \
                        string_stripped == chapter_list[chapter_counter + 1]:
                    chapter_counter = chapter_counter + 1
                    self._page_info.create_new_chapter(chapter_list[chapter_counter])
                else:
                    if new_paragraph:
                        # Push a new paragraph with the current content and current info
                        self._page_info.chapter_dict[chapter_list[chapter_counter]].\
                            create_new_paragraph(new_paragraph_text=string_stripped)
                    else:
                        # It's a blockquote or a special "display" in the paragraph
                        # so we need to add it to the last paragraph built
                        self._page_info.chapter_dict[chapter_list[chapter_counter]].\
                            append_text_to_last_paragraph("\n" + string_stripped)
                    new_paragraph = string_stripped.endswith((".", "?", "!", "\"", "”"))

        # compute page info
        self._page_info.compute_page()
        # Print info
        print(self._page_info)

    def _fill_page_info(self) -> None:
        """
        Extract all available info about the lovecraft webpage and
        store it inside the internal var _page_info
        """
        # beautifulSoup doesn't have any way to properly manage <br> tag so we just delete them
        self._raw_webpage_content.replace('<br>', '')
        self._raw_webpage_content.replace('<br/>', '')
        soup = bs4.BeautifulSoup(self._raw_webpage_content, 'html.parser')

        # Navigate through the tree to retrieve the element we want
        page_layout_div = soup.find('div', class_='pagelayout')
        navigation_tr = page_layout_div.find_next('tr')

        # Navigate through html tree and store title
        title_tr = navigation_tr.find_next_siblings('tr')[0]
        title_text = title_tr.get_text(separator='\n').lstrip("\r\n")
        self._page_info.title = title_text.split('\n')[0]

        # Navigate through html tree and find the main text part
        main_text_font = title_tr.find_next('tr').font

        # Parse the line list and retrieve a text_object
        # containing a key/value chapter : paragraph_list
        self.__build_chapter_dict(main_text_font)
