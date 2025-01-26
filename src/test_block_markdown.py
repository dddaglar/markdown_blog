import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    blocktype_to_tag,
    text_without_markdown_symbols,
    inline_text_to_html_nodes,
    md_block_to_parent,
    md_block_to_parent_lists,
    markdown_to_html_node,
    extract_title
)
from htmlnode import ParentNode


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        input1 = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""

        expected = [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        """* This is the first list item in a list block
        * This is a list item
        * This is another list item""",
        ]
        result1 = markdown_to_blocks(input1)

        self.assertEqual(result1,expected)

    def test_block_to_blocktype(self):
        sample = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""

        expected = ["heading1","paragraph","unordered_list"]

        blocks = markdown_to_blocks(sample)
        res = []
        for block in blocks:
            res.append(block_to_block_type(block))
        self.assertEqual(res, expected)

    def test_blocktype_to_tag(self):
        self.assertEqual(blocktype_to_tag("heading1"), "h1")
        self.assertEqual(blocktype_to_tag("heading2"), "h2")
        self.assertEqual(blocktype_to_tag("heading3"), "h3")
        self.assertEqual(blocktype_to_tag("code"), "code")
        self.assertEqual(blocktype_to_tag("quote"), "blockquote")
        self.assertEqual(blocktype_to_tag("unordered_list"), "ul")
        self.assertEqual(blocktype_to_tag("ordered_list"), "ol")
        self.assertEqual(blocktype_to_tag("paragraph"), "p")
        self.assertIsNone(blocktype_to_tag("something_else"))

    def test_text_without_markdown_symbols(self):
        """Ensure leading '#' is removed when tag starts with 'h'."""
        text = "## This is a heading"
        result = text_without_markdown_symbols(text, "h2")
        self.assertEqual(result, " This is a heading")

        """Ensure triple backticks are stripped for 'code' tag."""
        text2 = "```print('Hello')```"
        result2 = text_without_markdown_symbols(text2, "code")
        self.assertEqual(result2, "print('Hello')")

        text3 = "> This is a quote\n> More quote"
        result3 = text_without_markdown_symbols(text3, "blockquote")
        self.assertEqual(result3, " This is a quote\n More quote")

    def test_text_without_markdown_symbols_ul(self):
        text = "- List item"
        result = text_without_markdown_symbols(text, "ul")
        self.assertEqual(result, "List item")

        text2 = "* Another item"
        result2 = text_without_markdown_symbols(text2, "ul")
        self.assertEqual(result2, "Another item")
    
    def test_text_without_markdown_symbols_ol(self):
        text = "1. First item"
        result = text_without_markdown_symbols(text, "ol")
        self.assertEqual(result, "First item")

        text2 = "10. Tenth item"
        result2 = text_without_markdown_symbols(text2, "ol")
        self.assertEqual(result2, "Tenth item")
    
    def test_text_without_markdown_symbols_paragraph(self):
        text = "Just a paragraph."
        result = text_without_markdown_symbols(text, "p")
        self.assertEqual(result, text)


    def test_inline_text_to_html_nodes(self):
        sample = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = inline_text_to_html_nodes(sample)
        expected = [
            "This is ",
            "<b>text</b>",
            " with an ",
            "<i>italic</i>",
            " word and a ",
            "<code>code block</code>",
            " and an ",
            '<img src="https://i.imgur.com/fJRm4Vk.jpeg" alt="obi wan image">',
            " and a ",
            '<a href="https://boot.dev">link</a>'
        ]
        self.assertEqual(result, expected)

    def test_md_block_to_parent(self):
        block = "## Some heading text"
        tag = "h2"
        parent = md_block_to_parent(block, tag)
        # parent should be a ParentNode with:
        #    tag = "h2"
        #    children = results of inline_text_to_html_nodes on " Some heading text"
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "h2")
        self.assertIsInstance(parent.children, list)

    def test_md_block_to_parent_lists(self):
        block = "- Item one\n- Item two"
        tag = "ul"
        parent = md_block_to_parent_lists(block, tag)

        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "ul")
        self.assertEqual(len(parent.children), 2)

        # Each child should be a <li> ParentNode
        self.assertTrue(all(child.tag == "li" for child in parent.children))

    def test_markdown_to_html_node(self):

        markdown = """# Heading 1

        This is a paragraph with **bold** text.

        > This is a quote

        * Bullet item 1
        * Bullet item 2

        1. Ordered item 1
        2. Ordered item 2

        ```print("Hello, World!")```

"""
        root_node = markdown_to_html_node(markdown)

        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")

        self.assertGreaterEqual(len(root_node.children), 6, 
        "Expected at least 6 blocks from the sample markdown")

        heading_node = root_node.children[0]
        self.assertEqual(heading_node.tag, "h1")
        self.assertEqual(len(heading_node.children), 1)
        self.assertIn("Heading 1", heading_node.children[0])

        paragraph_node = root_node.children[1]
        self.assertEqual(paragraph_node.tag, "p")
        
        quote_node = root_node.children[2]
        self.assertEqual(quote_node.tag, "blockquote")
        self.assertTrue(any("This is a quote" in str(child) for child in quote_node.children),
                        "Expected quote text in the blockquote node")
        
        ul_node = root_node.children[3]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 2)

        ol_node = root_node.children[4]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 2)

        code_node = root_node.children[5]
        self.assertEqual(code_node.tag, "pre")
        self.assertTrue(any("print(\"Hello, World!\")" in str(child) for child in code_node.children),
                        "Expected code text in code node")

    def test_extract_title(self):
        result = extract_title("# Hello")
        expected = "Hello"
        self.assertEqual(result, expected)