import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from enum import Enum

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        dummyprops = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        result1 ='href="https://www.google.com" target="_blank"'
        node = HTMLNode("p","dummytext",None,dummyprops)
        self.assertEqual(node.props_to_html(), result1)

    def test_repr(self):
        node = HTMLNode("a","dummycontent")
        self.assertEqual(node.__repr__(),"tag:a, value:dummycontent, children:None, props:None")

    def test_init(self):
        with self.assertRaises(ValueError):
            node = HTMLNode("p","dummyhtml","children")
        with self.assertRaises(ValueError):
            node = HTMLNode("p","dummyhtml",["child1","child2"],"props")
    
    def test_leaf_init(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p",None)

    def test_leaf_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        expected1 = "<p>This is a paragraph of text.</p>"
        expected2 = '<a href="https://www.google.com">Click me!</a>'
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result1 = node1.to_html()
        result2 = node2.to_html()
        self.assertEqual(result1,expected1)
        self.assertEqual(result2,expected2)

    def test_parent_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        sample = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(sample,expected)

    def test_parent_to_html_nested_parent(self):
        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node = ParentNode(
            "p",
            [
                node2,
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        sample = node.to_html()
        expected = "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(sample,expected)

    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                "p",
                [],
            )
            res = node.to_html()

    def test_text_to_html(self):
        text_node1 = TextNode("dummy","normal")
        html_node1 = text_node_to_html_node(text_node1).to_html()
        expected1 = "dummy"
        self.assertEqual(html_node1,expected1)

        text_node2 = TextNode("dummy","italic")
        html_node2 = text_node_to_html_node(text_node2).to_html()
        expected2 = "<i>dummy</i>"
        self.assertEqual(html_node2,expected2)

        text_node3 = TextNode("dummy","image","https://zeldawiki.wiki/wiki/File:EoW_Link_Render.png")
        html_node3 = text_node_to_html_node(text_node3).to_html()
        expected3 = '<img src="https://zeldawiki.wiki/wiki/File:EoW_Link_Render.png" alt="dummy">'
        self.assertEqual(html_node3,expected3)










