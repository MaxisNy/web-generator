import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNode.text_type_text)
        node2 = TextNode("This is a text node", TextNode.text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextNode.text_type_text)
        node2 = TextNode("This is a text node", TextNode.text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextNode.text_type_text)
        node2 = TextNode("This is a text node2", TextNode.text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextNode.text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", TextNode.text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextNode.text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextNode.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextNode.text_type_code)
        self.assertEqual(
            new_nodes, [TextNode("This is text with a ", TextNode.text_type_text), TextNode("code block", TextNode.text_type_code), TextNode(" word", TextNode.text_type_text),]
        )
    
    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(
            [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")],
            extract_markdown_images(text)
        )
    
    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            [("link", "https://www.example.com"), ("another", "https://www.example.com/another")],
            extract_markdown_links(text)
        )


if __name__ == "__main__":
    unittest.main()