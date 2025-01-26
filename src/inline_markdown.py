from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        old_text_type = node.text_type
        if old_text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError("Invalid markdown, section not closed")
        for i,piece in enumerate(splitted):
            if piece == "":
                continue
            if i % 2 == 0:
                new_node = TextNode(piece,TextType.NORMAL)
                new_nodes.append(new_node)
            elif i % 2 == 1:
                new_node = TextNode(piece,text_type)
                new_nodes.append(new_node)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            if node.text.strip() != "":
                new_nodes.append(node)
            continue
        splitted = node.text
        for image in images:
            splitted = splitted.split(f"![{image[0]}]({image[1]})",1)
            inter_new_nodes = []
            if splitted[0].strip() != "":
                new_node_before = TextNode(splitted[0],TextType.NORMAL)
                inter_new_nodes.append(new_node_before)
            new_node_image = TextNode(image[0],TextType.IMAGE, image[1])
            inter_new_nodes.append(new_node_image)
            splitted = splitted[1]
            new_nodes.extend(inter_new_nodes)
        if splitted.strip() != "":
            new_node_after = TextNode(splitted,TextType.NORMAL)
            new_nodes.append(new_node_after)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            if node.text.strip() != "":
                new_nodes.append(node)
            continue
        splitted = node.text
        for link in links:
            splitted = splitted.split(f"[{link[0]}]({link[1]})",1)
            inter_new_nodes = []
            if splitted[0].strip() != "":
                new_node_before = TextNode(splitted[0],TextType.NORMAL)
                inter_new_nodes.append(new_node_before)
            new_node_link = TextNode(link[0],TextType.LINK, link[1])
            inter_new_nodes.append(new_node_link)
            splitted = splitted[1]
            new_nodes.extend(inter_new_nodes)
        if splitted.strip() != "":
            new_node_after = TextNode(splitted,TextType.NORMAL)
            new_nodes.append(new_node_after)
    return new_nodes
    
def text_to_textnodes(text):
    old_node = TextNode(text,TextType.NORMAL)
    boldened = list(split_nodes_delimiter([old_node],"**",TextType.BOLD))
    italicized = split_nodes_delimiter(boldened,"*",TextType.ITALIC)
    code_added = split_nodes_delimiter(italicized,"`",TextType.CODE)
    image_added = split_nodes_image(code_added)
    link_added = split_nodes_link(image_added)
    italicized2 = split_nodes_delimiter(link_added,"_",TextType.ITALIC)
    return italicized2


