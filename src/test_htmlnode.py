import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode("p", "hello world")
        props = node.props_to_html()
        self.assertEqual(props, "")
    
    def test_props(self):
        node = HTMLNode("p", "hello world", None, {"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()