from textnode import *
from inline_markdown import *
from block_markdown import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text = """This is **bolded** paragraph
            
            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items"""
    for block in markdown_to_blocks(text):
        print(block)

main()
