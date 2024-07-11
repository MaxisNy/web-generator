from textnode import *
from inline_markdown import *
from markdown_blocks import *
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import datetime
import shutil
from gencontent import generate_page, generate_page_recursively

__home_path = "/Users/max/workspace/github.com/MaxisNy/web-generator"
__log_filename = "weblog_" + str(datetime.datetime.now())[:-7].replace(' ', '_') + ".txt"
__log_filepath = os.path.join(__home_path, "tmp", __log_filename)

def get_paths(dir_path, home_path=__home_path) -> list:
    abs_dir_path = os.path.join(home_path, dir_path)
    paths_dict = {}
    for rel_path in os.listdir(abs_dir_path):
        cur_path = os.path.join(abs_dir_path, rel_path)
        if os.path.isfile(cur_path):
            paths_dict[rel_path] = None
        else:
            paths_dict[rel_path] = get_paths(rel_path, abs_dir_path)
    return paths_dict

def migrate_contents(paths_dict, abs_src_path, abs_dest_path):
    with open(__log_filepath, 'a') as log_file:
        for node in paths_dict:
            if paths_dict[node] is None:
                if shutil.copy(os.path.join(abs_src_path, node), abs_dest_path) == os.path.join(abs_dest_path, node):
                    log_file.write(f"copy: '{os.path.join(abs_src_path, node)}' to '{abs_dest_path}'\n")
            else:
                if os.mkdir(os.path.join(abs_dest_path, node)) is None:
                    log_file.write(f"create new directory: '{os.path.join(abs_dest_path, node)}'\n")
                migrate_contents(paths_dict[node], os.path.join(abs_src_path, node), os.path.join(abs_dest_path, node))

def copy_directory(src_path, destination_path="public") -> str:
    abs_src_path = os.path.join(__home_path, src_path)
    abs_dest_path = os.path.join(__home_path, destination_path)
    if os.path.exists(abs_dest_path):
        if os.path.exists(abs_src_path):
            log_filename = "weblog_" + str(datetime.datetime.now())[:-7].replace(' ', '_')
            log_filepath = os.path.join(__home_path, "tmp", log_filename)
            # get paths to all the files inside the source directory
            src_paths_tree = get_paths(src_path)
            # remove contents of destination directory
            shutil.rmtree(abs_dest_path)
            # create a new public directory
            os.mkdir(abs_dest_path)
            # copy contents of the source directory into destination directory
            migrate_contents(src_paths_tree, abs_src_path, abs_dest_path)
            return log_filepath
        raise ValueError(f"Invalid source path: {abs_src_path}")
    raise ValueError(f"Invalid destination path: {abs_dest_path}")

def main():
    copy_directory("static", "public")
    # generate_page(os.path.join(__home_path, "content/majesty/index.md"), os.path.join(__home_path, "template.html"), os.path.join(__home_path, "public/index.html"))
    generate_page_recursively(os.path.join(__home_path, "content"), os.path.join(__home_path, "template.html"), os.path.join(__home_path, "public"))
main()