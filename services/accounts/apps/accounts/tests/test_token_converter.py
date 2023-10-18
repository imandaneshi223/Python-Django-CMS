import re

from django.test import TestCase

from ..urls import TokenConverter


class TokenConverterTest(TestCase):
    def test_if_regex_is_matching_valid_token(self):
        pattern = re.compile(TokenConverter.regex)
        self.assertTrue(pattern.match("a9dfbde116af89e8a4ec46ce4e7fe94381dcd899"))
        self.assertFalse(pattern.match("1b51e2fc-77bc-437d-9430-fb806e6cf0c0"))
