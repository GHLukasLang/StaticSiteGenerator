import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a test node", TextType.ITALIC)
        node2 = TextNode("This is a test node", TextType.ITALIC, None)
        self.assertEqual(node, node2)
    
    def test_text_empty(self):
        with self.assertRaises(TypeError):
            node = TextNode(TextType.CODE)
    
    def test_different_texttypes(self):
        node = TextNode("", TextType.LINK)
        node2 = TextNode("", TextType.NORMAL)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_b(self):
        node = TextNode("This is a text node", TextType.BOLD, url="www.gooogle.com")
        html_node = text_node_to_html_node(node)
        #self.assertEqual(html_node.props, "www.google.com")
        self.assertEqual(html_node.tag, "b")
        
    def test_to_html_node_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="www.gooogle.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {'href': 'www.gooogle.com'})
        #self.assertEqual(html_node.tag, "b")

if __name__ == "__main__":
    unittest.main()
