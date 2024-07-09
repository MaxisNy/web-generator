import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

pattern_to_type_dict = {
    r"#{1,6}\s\w+(\s\w+)*": block_type_heading,
    r"`{3}\n*.*\n*`{3}": block_type_code,
    r"(>.*\n)*(>.*)": block_type_quote,
    r"((\*|-)\s.*\n)*((\*|-)\s.*)": block_type_ulist,
    r"(\d+\.\s.*\n)*(\d+\.\s.*)": block_type_olist
}

def markdown_to_blocks(markdown):
    blocks_list = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        if block == '':
            continue
        block = block.strip()
        blocks_list.append(block)
    return blocks_list

def block_to_block_type(markdown_block):
    for pattern in pattern_to_type_dict:
        matches = re.search(pattern, markdown_block)
        if matches is not None and (len(matches.group()) == len(markdown_block)):
            return pattern_to_type_dict[pattern]
    return block_type_paragraph

def text_to_children(text) -> list:
    children = []
    children.extend(text_to_textnodes(text))
    return list(map(text_node_to_html_node, children))

def paragraph_to_html_node(markdown_block):
    p_lines = []
    for line in markdown_block.split('\n'):
        if line != "":
            p_lines.append(line)
    p_text = ' '.join(p_lines)
    children = text_to_children(p_text)
    return ParentNode("p", children)

def heading_to_html_node(markdown_block):
    level = 0
    while markdown_block[level] == '#':
        level += 1
    h_text = markdown_block[level + 1:]
    children = text_to_children(h_text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(markdown_block):
    children = text_to_children(markdown_block[4:len(markdown_block) - 4])
    return ParentNode("pre", [ParentNode("code", children)])

def ulist_to_html_node(markdown_block):
    list_item_blocks = markdown_block.split('\n')
    list_items = []
    for item_text in list_item_blocks:
        if item_text != "":
            list_items.append(ParentNode("li", text_to_children(item_text[2:])))
    return ParentNode("ul", list_items)

def olist_to_html_node(markdown_block):
    list_item_blocks = markdown_block.split('\n')
    list_items = []
    for item_text in list_item_blocks:
        if item_text != "":
            list_items.append(ParentNode("li", text_to_children(item_text[item_text.find('.') + 2:])))
    return ParentNode("ol", list_items)

def quote_to_html_node(markdown_block):
    quote_lines = []
    for quote_line in markdown_block.split('\n'):
        if quote_line != "":
            quote_lines.append(quote_line.lstrip('>').strip())
    children = text_to_children(' '.join(quote_lines))
    return ParentNode("blockquote", children)

def markdown_to_html_node(markdown):
    div_children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case "paragraph":
                div_children.append(paragraph_to_html_node(block))
                continue
            case "heading":
                div_children.append(heading_to_html_node(block))
                continue
            case "code":
                div_children.append(code_to_html_node(block))
                continue
            case "quote":
                div_children.append(quote_to_html_node(block))
                continue
            case "ordered_list":
                div_children.append(olist_to_html_node(block))
                continue
            case "unordered_list":
                div_children.append(ulist_to_html_node(block))
                continue
    return ParentNode("div", div_children)



