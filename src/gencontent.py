import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

__home_path = "/Users/max/workspace/github.com/MaxisNy/web-generator"

def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    content_paths = get_inner_paths(dir_path_content)
    for path in content_paths:
        new_dest_dir_path = path.replace(dir_path_content, dest_dir_path)
        new_dest_dir_path = new_dest_dir_path.replace('.md', '.html')
        generate_page(path, template_path, new_dest_dir_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r')
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, 'r')
    template = template_file.read()
    template_file.close()

    html_src_content = markdown_to_html_node(markdown_content).to_html()
    page_title = extract_title(markdown_content)

    # check that the destination path is valid
    # otherwise, create missing directories
    check_dest_path(dest_path)

    with open(dest_path, 'w') as dest_file:
        template_lines = template.split('\n')
        for line_index in range(len(template_lines)):
            if template_lines[line_index].strip().startswith("<title>"):
                dest_file.write(template_lines[line_index].replace("{{ Title }}", page_title) + '\n')
            elif template_lines[line_index].strip().startswith("{{ Content }}"):
                dest_file.write(template_lines[line_index].replace("{{ Content }}", html_src_content) + '\n')
            else:
                dest_file.write(template_lines[line_index] + '\n')

def extract_title(md) -> str:
    for line in md.split('\n'):
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Invalid markdown: no title found")

def check_dest_path(dest_path):
    if not os.path.exists(dest_path):
        directories = dest_path.split(os.sep)
        i = 1
        new_directories = []
        while not os.path.isdir(os.sep.join(directories[:-i])):
            if os.sep.join(directories[:-i]) == __home_path:
                raise ValueError("Cannot create file outside of the project directory")
            new_directories.append(directories[-i-1])
            i += 1
        cur_valid_dir = os.sep.join(directories[:-i])
        new_directories.reverse()
        for new_dir in new_directories:
            if os.mkdir(os.path.join(cur_valid_dir, new_dir)) is None:
                cur_valid_dir = os.path.join(cur_valid_dir, new_dir)
            else:
                raise Exception(f"Cannot create directory: {new_dir}")

def get_inner_paths(abs_cur_path):
    paths_list = []
    for rel_path in os.listdir(abs_cur_path):
        new_path = os.path.join(abs_cur_path, rel_path)
        if os.path.isfile(new_path):
            paths_list.append(new_path)
        else:
            paths_list += get_inner_paths(new_path)
    return paths_list