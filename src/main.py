from textnode import *
from inline_markdown import *
from markdown_blocks import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    heading = "# sample heading"
    print(block_to_block_type(heading))
    code = "``` sample code ```"
    print(block_to_block_type(code))
    quote = """> quote one
    > quote two"""
    print(block_to_block_type(quote))
    ul = """* line one
    - line two"""
    print(block_to_block_type(ul))
    ol = """1. line one
    2. line two"""
    print(block_to_block_type(ol))
    par = "sample paragraph here"
    print(block_to_block_type(par))

main()
