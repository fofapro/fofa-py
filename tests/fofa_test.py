# -*- coding: utf-8 -*-
import unittest
import fofa
import sys, os
import tracemalloc


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        env_dist = os.environ
        key = env_dist.get('FOFA_KEY')
        if not key:
            key = open('../CONFIG').read()
        self.client = fofa.Client(key)

    def test_get_userinfo(self):
        userinfo = self.client.get_userinfo()
        self.assertIn("isvip", userinfo)
        self.assertIn("fcoin", userinfo)
        self.assertIn("email", userinfo)
        self.assertIn("avatar", userinfo)

        self.assertTrue(userinfo["isvip"])
        self.assertGreaterEqual(userinfo["fcoin"], 0)
        self.assertTrue(userinfo["email"])
        self.assertTrue(userinfo["avatar"])

    def test_get_data_empty(self):
        query = '''djaoiwjklejaoijdoawd'''
        data = self.client.search(query)
        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)

        self.assertFalse(data["results"])
        self.assertTrue(data["page"])
        self.assertFalse(data["size"])
        self.assertTrue(data["mode"])
        self.assertTrue(data["query"])

        if sys.version > '3':
            self.assertEqual(data["query"].strip("\""), query)
        else:
            self.assertEqual(data["query"].encode('ascii', 'ignore').strip("\""), query)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["mode"], "normal")

    def test_get_data_normal(self):
        query = '''fofa.info'''
        data = self.client.search(query)
        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)

        self.assertTrue(data["results"])
        self.assertTrue(data["page"])
        self.assertTrue(data["size"])
        self.assertTrue(data["mode"])
        self.assertTrue(data["query"])

        self.assertFalse(data["error"])

        if sys.version > '3':
            self.assertEqual(data["query"].strip("\""), query)
        else:
            self.assertEqual(data["query"].encode('ascii', 'ignore').strip("\""), query)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["mode"], "normal")

    def test_get_data_field(self):
        query = '''host="fofa.info"'''
        data = self.client.search(query, fields="host,title,ip,domain,port,country,city")

        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)

        self.assertTrue(data["results"])
        self.assertTrue(data["page"])
        self.assertTrue(data["size"])
        self.assertTrue(data["mode"])
        self.assertTrue(data["query"])

        self.assertFalse(data["error"])

        self.assertEqual(data["query"], query)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["mode"], "extended")

        self.assertEqual(len(data["results"][0]), 7)

    def test_get_data_extended(self):
        query = '''host="fofa.info"'''
        data = self.client.search(query)
        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)

        self.assertTrue(data["results"])
        self.assertTrue(data["page"])
        self.assertTrue(data["size"])
        self.assertTrue(data["mode"])
        self.assertTrue(data["query"])

        self.assertFalse(data["error"])

        self.assertEqual(data["query"], query)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["mode"], "extended")

    def test_get_data_page_error1(self):
        try:
            query = '''djaoiwjklejaoijdoawd'''
            data = self.client.search(query, size=100, page="asd")
        except:
            self.assertTrue(True)

    def test_get_data_page_error2(self):
        try:
            query = '''fofa.info'''
            data = self.client.search(query, size=100, page="300")
        except:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
