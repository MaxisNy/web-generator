from textnode import *
from inline_markdown import *
from markdown_blocks import *
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

pattern_to_type_dict = {
    r"#{1,6}\s\w+(\s\w+)*": block_type_heading,
    r"`{3}\n*.*`{3}": block_type_code,
    r"(>.*\n)*(>.*)": block_type_quote,
    r"((\*|-)\s.*\n)*((\*|-)\s.*)": block_type_ulist,
    r"(\d+\.\s.*)+": block_type_olist
}

def main():
    block = "* list\n* items"
    pattern = r"((\*|-)\s.*\n)*((\*|-)\s.*)"
    print(re.search(pattern, block))

main()
