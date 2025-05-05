import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    

    
    def test_repr(self):
        node = HTMLNode("h1", "This is a test", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(repr(node), "HTMLNode(tag=h1, value=This is a test, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})")

    def test_default(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)


    
    def test_props_to_html(self):
        node = HTMLNode("h1", "This is a test", None, {"href": "https://www.google.com","target": "_blank",})
        expected = " href='https://www.google.com' target='_blank'"
        self.assertEqual(node.props_to_html(), expected)





if __name__ == "__main__":
    unittest.main()

