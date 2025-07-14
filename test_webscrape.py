import unittest
from webscrape import *
from bs4 import BeautifulSoup
import pandas as pd
import os

class TestWebscrape(unittest.TestCase):
    def test_parse_star_cnt(self):
        self.assertEqual(parse_star_cnt('70.6k'), 70600)
        self.assertEqual(parse_star_cnt('1k'), 1000)
        self.assertEqual(parse_star_cnt('500'), 500)

    def test_get_repo_info(self):
        html = """
        <h1>
            <a href="/mrdoob">mrdoob</a> / <a href="/mrdoob/three.js" class="text-bold">three.js</a>
        </h1>
        <a class="social-count float-none">70.6k</a>
        """
        soup = BeautifulSoup(html, 'html.parser')
        h_tag = soup.find('h1')
        star_tag = soup.find('a', class_="social-count float-none")
        username, repositname, repourl, stars = get_repo_info(h_tag, star_tag)
        self.assertEqual(username, 'mrdoob')
        self.assertEqual(repositname, 'three.js')
        self.assertEqual(repourl, 'https://github.com/mrdoob/three.js')
        self.assertEqual(stars, 70600)

    def test_get_topic_doc(self):
        # This test will fail if github is down or changes its structure
        html = get_topic_doc("https://github.com/topics/3d")
        self.assertTrue(html)

    def test_get_topic_repo(self):
        # This test will fail if github is down or changes its structure
        html = get_topic_doc("https://github.com/topics/3d")
        df = get_topic_repo(html)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_scrape_topic_one(self):
        # This test will fail if github is down or changes its structure
        scrape_topic_one("https://github.com/topics/3d", "test_3d")
        self.assertTrue(os.path.exists("test_3d.csv"))
        os.remove("test_3d.csv")

    def test_get_topics(self):
        # This test will fail if github is down or changes its structure
        html = get_topic_doc("https://github.com/topics")
        topics = get_topics(html)
        self.assertIsInstance(topics, list)
        self.assertGreater(len(topics), 0)

    def test_get_descs(self):
        # This test will fail if github is down or changes its structure
        html = get_topic_doc("https://github.com/topics")
        descs = get_descs(html)
        self.assertIsInstance(descs, list)
        self.assertGreater(len(descs), 0)

    def test_get_urllist(self):
        # This test will fail if github is down or changes its structure
        html = get_topic_doc("https://github.com/topics")
        urls = get_urllist(html)
        self.assertIsInstance(urls, list)
        self.assertGreater(len(urls), 0)

    def test_scrape_topics(self):
        # This test will fail if github is down or changes its structure
        df = scrape_topics()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

if __name__ == '__main__':
    unittest.main()
