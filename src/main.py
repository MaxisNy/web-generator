from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("This is text with a `code block` word", TextNode.text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", TextNode.text_type_code)
    print(new_nodes)

main()
