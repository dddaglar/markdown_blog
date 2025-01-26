from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        block = block.strip()
        if block != "":
            res.append(block)
    return res

def block_to_block_type(block):
    if block[0] == "#":
        i, ctr = 1,1
        while block[i] == "#" and i < 6:
            ctr += 1
            i += 1
        return f"heading{ctr}"
    if len(block) > 3 and block[0:3] == "```" and block[-3:] == "```":
        return "code"
    if block[0] == ">":
        lines = block.split("\n")
        for line in lines:
            if line[0] != ">":
                raise Exception("invalid block syntax, neither quote nor paragraph")
        return "quote"
    if block[0] == "*" and block[1] == " ":
        lines = block.split("\n")
        for line in lines:
            line = line.strip()
            if line[0] != "*":
                raise Exception("invalid block syntax, neither unordered list nor paragraph")
        return "unordered_list"
    if block[0] == "-" and block[1] == " ":
        lines = block.split("\n")
        for line in lines:
            if line[0] != "-":
                raise Exception("invalid block syntax, neither unordered list nor paragraph")
        return "unordered_list"
    if block[0].isdigit() and block[1] == ".":
        lines = block.split("\n")
        for line in lines:
            line = line.strip()
            if not line[0].isdigit() or line[1] != ".":
                raise Exception("invalid block syntax, neither ordered list nor paragraph")
        return "ordered_list"
    return  "paragraph"

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    og_node = ParentNode("div",[])
    for block in blocks:
        b_type = block_to_block_type(block)
        tag = blocktype_to_tag(b_type)
        if tag[0] == "h":
            parent = md_block_to_parent(block,tag)
            og_node.children.append(parent)
        match tag:
            case "code":
                parent = md_block_to_parent(block,tag)
                parent2 = ParentNode("pre",[])
                parent2.children.append(parent)
                og_node.children.append(parent2)
            case "blockquote":
                parent = md_block_to_parent(block,tag)
                og_node.children.append(parent)
            case "ul":
                parent = md_block_to_parent_lists(block,tag)
                og_node.children.append(parent)
            case "ol":
                parent = md_block_to_parent_lists(block,tag)
                og_node.children.append(parent)
            case "p":
                html_inline = inline_text_to_html_nodes(block)
                html_leafnodes = [LeafNode(None,inline) for inline in html_inline]
                parent = ParentNode(tag,html_leafnodes)
                og_node.children.append(parent)
    return og_node

def blocktype_to_tag(blocktype):
    if blocktype[:7] == "heading":
        if blocktype[:7] == "heading":
            return f"h{blocktype[-1]}"
    match blocktype:
        case "code":
            return "code"
        case "quote":
            return "blockquote"
        case "unordered_list":
            return "ul"
        case "ordered_list":
            return "ol"
        case "paragraph":
            return "p"
        case _:
            return None

def text_without_markdown_symbols(text, tag):
    text = text.strip()
    if tag[0] == "h":
        return text.lstrip("# ")
    elif tag == "code":
        return text.strip("```")
    elif tag == "blockquote":
        lines = text.split("\n")
        res = []
        for line in lines:
            res.append(line.lstrip("> "))
        return "\n".join(res)
    elif tag == "ul":
        return text.lstrip("-*").lstrip()
    elif tag == "ol":
        return text.lstrip("1234567890").lstrip(".").lstrip()
    elif tag == "p":
        return text

def inline_text_to_html_nodes(text):
    textnode_list = text_to_textnodes(text)
    html_list = []
    for tnode in textnode_list:
        html_list.append(text_node_to_html_node(tnode).to_html())
    return html_list

def md_block_to_parent(block,tag):
    inline_text = text_without_markdown_symbols(block,tag)
    html_inline = inline_text_to_html_nodes(inline_text)
    html_leafnodes = [LeafNode(None,inline) for inline in html_inline]
    parent = ParentNode(tag,html_leafnodes)
    return parent

def md_block_to_parent_lists(block,tag):
    parent = ParentNode(tag,[])
    list_items = block.split("\n")
    for item in list_items:
        inline_text = text_without_markdown_symbols(item,tag)
        html_inline = inline_text_to_html_nodes(inline_text)
        html_leafnodes = [LeafNode(None,inline) for inline in html_inline]
        semi_parent = ParentNode("li",html_leafnodes)
        parent.children.append(semi_parent)
    return parent

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    found = 0
    for block in blocks:
        if block_to_block_type(block) == "heading1":
            found = 1
            return text_without_markdown_symbols(block,"h1").strip()
    if found == 0:
        raise Exception("no title")
    
