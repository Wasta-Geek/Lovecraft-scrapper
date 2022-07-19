"""Manage a Lovecraft page and it's parsing"""

import urllib.request
import urllib.error
import urllib.response
from abc import ABC, abstractmethod
from .page_info import PageInfo


class PageUnavailable(RuntimeError):
    """
    Raised when the given website cannot be opened
    """


class Page(ABC):
    """
    An abstract class that represents a generic page
    """

    def __init__(self, url: str):
        if not url.startswith("http"):
            print(f"[info] Url '{url}' doesn't include any http(s) scheme,"
                  f" adding default http scheme")
            self._page_info = PageInfo( "http://" + url)
        else:
            self._page_info = PageInfo(url)
        self._raw_webpage_content = ''
        self._main_text = ''


    @property
    def raw_webpage_content(self) -> str:
        """
        Get raw_webpage_content variable
        :return: raw_webpage_content variable
        """
        return self._raw_webpage_content

    @property
    def page_info(self) -> PageInfo:
        """
        Getter for page_info
        :return: PageInfo object
        """
        return self._page_info

    def open_webpage(self) -> None:
        """
        Open a connection with the website and retrieve the page content

        """
        try:
            with urllib.request.urlopen(self.page_info.url) as response:
                self._raw_webpage_content = response.read()
                self._fill_page_info()
        except urllib.error.URLError as error:
            raise PageUnavailable() from error

    @abstractmethod
    def _fill_page_info(self) -> None:
        pass
