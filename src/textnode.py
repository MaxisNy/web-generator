from htmlnode import LeafNode
import re

class TextNode:

    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    valid_delimiters = ['*', '**', '`']

    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextNode.text_type_text:
            return LeafNode(None, text_node.text)  # No tag for plain text
        case TextNode.text_type_bold:
            return LeafNode("b", text_node.text)
        case TextNode.text_type_italic:
            return LeafNode("i", text_node.text)
        case TextNode.text_type_code:
            return LeafNode("code", text_node.text)
        case TextNode.text_type_link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextNode.text_type_image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case __:
            raise Exception(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextNode.text_type_text:
            if delimiter in TextNode.valid_delimiters:
                left_text, inner_text, right_text = node.text.split(delimiter)[0], node.text.split(delimiter)[1], node.text.split(delimiter)[2]
                new_nodes.extend([
                    TextNode(left_text, TextNode.text_type_text),
                    TextNode(inner_text, text_type),
                    TextNode(right_text, TextNode.text_type_text)
                ])
            else:
                raise ValueError(f"Invalid Markdown delimiter: {delimiter}")
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text) -> list:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        image_details = extract_markdown_images(text)
        if len(image_details) == 0:
            continue
        for i in range(len(image_details)):
            left_text, right_text = text.split(f"![{image_details[i][0]}]({image_details[i][1]})", 1)[0], text.split(f"![{image_details[i][0]}]({image_details[i][1]})", 1)[1]
            # append leftmost text node
            if left_text != "": new_nodes.append(TextNode(left_text, TextNode.text_type_text))
            new_nodes.append(TextNode(image_details[i][0], TextNode.text_type_image, image_details[i][1]))
            text = right_text
        # append rightmost text node
        if text != "": new_nodes.append(TextNode(text, TextNode.text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        link_details = extract_markdown_links(text)
        if len(link_details) == 0:
            continue
        for i in range(len(link_details)):
            left_text, right_text = text.split(f"![{link_details[i][0]}]({link_details[i][1]})", 1)[0], text.split(f"![{link_details[i][0]}]({link_details[i][1]})", 1)[1]
            # append leftmost text node
            if left_text != "": new_nodes.append(TextNode(left_text, TextNode.text_type_text))
            new_nodes.append(TextNode(link_details[i][0], TextNode.text_type_image, link_details[i][1]))
            text = right_text
        # append rightmost text node
        if text != "": new_nodes.append(TextNode(text, TextNode.text_type_text))
    return new_nodes
        