from htmlnode import LeafNode

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