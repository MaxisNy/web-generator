from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode(
        "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
        TextNode.text_type_text,
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes)

main()
