from textnode import TextNode
from htmlnode import HTMLNode

def main():
    htmlnode1 = HTMLNode("a", "some link here", [], {"href": "https://www.google.com", "target": "_blank"})
    print(htmlnode1)
    htmlnode2 = HTMLNode("div", None, [htmlnode1], None)
    print(htmlnode2)

main()
