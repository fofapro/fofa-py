# -*- coding: utf-8 -*-
import unittest
import fofa


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        config = open('../CONFIG').read()
        email,key = config.split("\n")
        self.client = fofa.Client(email, key)

    def test_get_userinfo(self):
        userinfo = self.client.get_userinfo()
        self.assertIn("isvip",userinfo)
        self.assertIn("fcoin", userinfo)
        self.assertIn("email", userinfo)
        self.assertIn("avatar", userinfo)

        self.assertTrue(userinfo["isvip"])
        self.assertTrue(userinfo["fcoin"])
        self.assertTrue(userinfo["email"])
        self.assertTrue(userinfo["avatar"])



    def test_get_data_empty(self):
        query = '''djaoiwjklejaoijdoawd'''
        data = self.client.get_data(query)
        self.assertIn("results",data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)

        self.assertFalse(data["results"])
        self.assertTrue(data["page"])
        self.assertFalse(data["size"])
        self.assertTrue(data["mode"])
        self.assertTrue(data["query"])

        self.assertEqual(data["query"], query)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["mode"], "normal")

    def test_get_data_normal(self):
        query = '''fofa.so'''
        data =  self.client.get_data(query )
        self.assertIn("results",data)
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

        self.assertEqual(data["query"],query)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["mode"], "normal")

    def test_get_data_field(self):
        query = '''host="fofa.so"'''
        data = self.client.get_data(query,fields="host,title,ip,domain,port,country,city")

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

        self.assertEqual(len(data["results"][0]),7)

    def test_get_data_extended(self):
        query = '''host="fofa.so"'''
        data = self.client.get_data(query)
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
            data = self.client.get_json_data(query, page="asd")
        except:
            self.assertTrue(True)


    def test_get_data_page_error2(self):
        try:
            query = '''fofa.so'''
            data = self.client.get_json_data(query, page="300")
        except:
            self.assertTrue(True)


if __name__ =='__main__':
  unittest.main()