import unittest
from datetime import datetime
import pandas as pd

from src.detection_rules import has_robots_txt_request, has_bot_name_in_user_agent


class TestDetectionRules(unittest.TestCase):
    def setUp(self):
        # TODO : refactor, this way of creating the fixtures is not ideal
        self.fixture_dataframe = pd.DataFrame(
            {
                "host": ["127.0.0.1", "172.168.1.24"],
                "timestamp": [
                    datetime.strptime("09/19/18 13:55:26", "%m/%d/%y %H:%M:%S"),
                    datetime.strptime("09/19/18 13:55:29", "%m/%d/%y %H:%M:%S"),
                ],
                "request": [
                    "POST /administrator/index.php HTTP/1.0",
                    "GET /robots.txt HTTP/1.0",
                ],
                "status": ["200", "404"],
                "size": ["4481", "283"],
                "referrer": ["-", "http://google.com"],
                "user_agent": [
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                ],
            }
        )

    def test_has_robots_txt_request(self):
        df_bots = has_robots_txt_request(self.fixture_dataframe)
        self.assertEqual(1, len(df_bots))
        self.assertEqual(df_bots[0], "172.168.1.24")

    def test_has_bot_name_in_user_agent(self):
        df_bots = has_bot_name_in_user_agent(self.fixture_dataframe)
        self.assertEqual(1, len(df_bots))
        self.assertEqual(df_bots[0], "172.168.1.24")


if __name__ == "__main__":
    unittest.main()
