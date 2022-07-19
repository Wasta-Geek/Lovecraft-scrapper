"""Manage a Lovecraft page and it's parsing"""

import urllib.request
import urllib.error
import urllib.response


class LovecraftPageUnavailable(RuntimeError):
    """
    Raised when the given website cannot be opened
    """


class LovecraftPage:
    """
    A class to represent a Lovecraft page
    """

    def __init__(self, url: str):
        if not url.startswith("http"):
            print(f"[info] Url '{url}' doesn't include any http(s) scheme,"
                  f" adding default http scheme")
            self.__url = "http://" + url
        else:
            self.__url = url
        self.__raw_webpage_content = ''

    @property
    def raw_webpage_content(self) -> str:
        """
        Get raw_webpage_content variable
        :return: raw_webpage_content variable
        """
        return self.__raw_webpage_content

    def open_webpage(self) -> None:
        """
        Open a connection with the website and retrieve the page content

        :return: A string containing the webpage content
        """
        try:
            with urllib.request.urlopen(self.__url) as response:
                self.__raw_webpage_content = response.read()
        except urllib.error.URLError as error:
            raise LovecraftPageUnavailable() from error
