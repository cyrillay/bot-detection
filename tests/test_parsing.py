import unittest

from src.parsing import _parser


class TestParsing(unittest.TestCase):
    def test_parser(self):
        log_line = (
            '91.121.185.43 - - [21/Mar/2020:17:17:51 +0100] "GET /apache-log/access.log HTTP/1.0" 200 654800 '
            '"http://xenicale.cmonsite.fr" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299" "-" '
        )
        parsed_log = _parser(log_line)
        host, time, request, status, size, referrer, user_agent = parsed_log
        self.assertEqual(host, "91.121.185.43")
        self.assertEqual(status, "200")
        self.assertEqual(request, "GET /apache-log/access.log HTTP/1.0")


# if __name__ == "__main__":
#     unittest.main()
