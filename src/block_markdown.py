def markdown_to_blocks(markdown):
    blocks_list = []
    cur_block = ""
    for block in markdown.split("\n"):
        block = block.strip(" ")
        if block != "":
            cur_block += block + '\n'
        else:
            blocks_list.append(cur_block)
            cur_block = ""
    blocks_list.append(cur_block.rstrip('\n'))
    return blocks_list