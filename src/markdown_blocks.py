import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

pattern_to_type_dict = {
    r"#{1,6}\s\w+(\s\w+)*": block_type_heading,
    r"`{3}.*`{3}": block_type_code,
    r"(>.*)+": block_type_quote,
    r"((\*|-)\s.*)+": block_type_ulist,
    r"(\d+\.\s.*)+": block_type_olist
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
        if matches is not None and len(matches.string) == len(markdown_block):
            return pattern_to_type_dict[pattern]
    return block_type_paragraph