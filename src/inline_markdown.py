from textnode import TextNode
import re

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        # check for text nodes WITH inner delimiters
        if (node.text_type == TextNode.text_type_text) and len(node.text.split(delimiter)) > 1:
            section = node.text.split(delimiter)
            if len(section) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            split_nodes = []
            for i in range(len(section)):
                if section[i] == "":
                    continue
                # section of the plain text type
                if i % 2 == 0:
                    split_nodes.append(TextNode(section[i], TextNode.text_type_text))
                else:
                    split_nodes.append(TextNode(section[i], text_type))
            new_nodes.extend(split_nodes) 
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text) -> list:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        text = node.text
        image_details = extract_markdown_images(text)
        if len(image_details) == 0:
            new_nodes.append(node)
            continue
        for i in range(len(image_details)):
            try:
                left_text, right_text = text.split(f"![{image_details[i][0]}]({image_details[i][1]})", 1)[0], text.split(f"![{image_details[i][0]}]({image_details[i][1]})", 1)[1]
            except IndexError:
                raise ValueError("Invalid markdown, image section not closed")
            # append leftmost text node
            if left_text != "": new_nodes.append(TextNode(left_text, TextNode.text_type_text))
            new_nodes.append(TextNode(image_details[i][0], TextNode.text_type_image, image_details[i][1]))
            text = right_text
        # append rightmost text node
        if text != "": new_nodes.append(TextNode(text, TextNode.text_type_text))
    return new_nodes

def split_nodes_link(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        text = node.text
        link_details = extract_markdown_links(text)
        if len(link_details) == 0:
            new_nodes.append(node)
            continue
        for i in range(len(link_details)):
            try:
                left_text, right_text = text.split(f"[{link_details[i][0]}]({link_details[i][1]})", 1)[0], text.split(f"[{link_details[i][0]}]({link_details[i][1]})", 1)[1]
            except IndexError:
                raise ValueError("Invalid markdown, link section not closed")
            # append leftmost text node
            if left_text != "": new_nodes.append(TextNode(left_text, TextNode.text_type_text))
            new_nodes.append(TextNode(link_details[i][0], TextNode.text_type_link, link_details[i][1]))
            text = right_text
        # append rightmost text node
        if text != "": new_nodes.append(TextNode(text, TextNode.text_type_text))
    return new_nodes

def text_to_textnodes(text) -> list:
    new_nodes = [TextNode(text, TextNode.text_type_text)]
    for delim, type in TextNode.valid_delimiters.items():
        new_nodes = split_nodes_delimiter(new_nodes, delim, type)
    return split_nodes_link(split_nodes_image(new_nodes))

        