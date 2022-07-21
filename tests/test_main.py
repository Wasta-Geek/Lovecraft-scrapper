"""
Test module focused on testing the main.py module
"""
import unittest
from unittest import mock
import argparse
from main import lovecraft_scrapper_main


class MainTestCase(unittest.TestCase):
    """
    Test class that test lovecraft_scrapper_main_function
    """
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://www.hplovecraft.com/writings/texts/fiction/mm.aspx"))
    def test_default_url(self, mocked):
        """
        Test the default url given in the test
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 0)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://hplovecraft.com/writings/texts/fiction/b.aspx"))
    def test_no_chapter_fiction_url(self, mocked):
        """
        Test a fiction that contains only one chapter (no chapter displayed in the webpage)
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 0)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://hplovecraft.com/writings/texts/fiction/hm.aspx"))
    def test_simple_fiction_url(self, mocked):
        """
        Test a simple fiction
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 0)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://hplovecraft.com/writings/texts/fiction/lf.aspx"))
    def test_another_simple_fiction_url(self, mocked):
        """
        Test another simple fiction
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 0)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="hplovecraft.com/writings/texts/fiction/tjr.aspx"))
    def test_fiction_url_without_scheme(self, mocked):
        """
        Test a simple fiction but the url doesn't contain http/https scheme
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 0)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://hplovecraft.com/writings/texts/fiction/foobar.aspx"))
    def test_wrong_url(self, mocked):
        """
        Test a wrong url (do not exist)
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 1)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="raclette_for_the_win"))
    def test_wrong_url_2(self, mocked):
        """
        Test a wrong url (not valid)
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 1)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://www.reddit.com/r/ProgrammerHumor/comments/soi384/why_but_why/"
                        "?utm_source=share&utm_medium=web2x&context=3"))
    def test_wrong_website(self, mocked):
        """
        Test a good URL but not a lovecraft fiction page
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 2)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    url="https://theuselessweb.com/"))
    def test_wrong_website_2(self, mocked):
        """
        Test another good URL but not a lovecraft fiction page
        """
        del mocked
        with self.assertRaises(SystemExit) as context_manager:
            lovecraft_scrapper_main()
        self.assertEqual(context_manager.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
