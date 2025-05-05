import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_href(self):
        node = LeafNode("a", "Click Me!", {"href":"www.google.com"})
        self.assertEqual(node.to_html(), "<a href='www.google.com'>Click Me!</a>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some Text")
        self.assertEqual(node.to_html(), "Just some Text")
    
    def test_leaf_empty_value_error(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()




