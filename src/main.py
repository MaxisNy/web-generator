from textnode import *
from inline_markdown import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("This is text with a **bolded** word and **another**", TextNode.text_type_text)
    new_nodes = split_nodes_delimiter([node], "**", TextNode.text_type_bold)
    for node in new_nodes:
        print(node)

main()
