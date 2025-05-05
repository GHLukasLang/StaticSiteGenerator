import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_complexity(self):
        # Create a complex nested structure
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "Italic text")

        # Create a parent with some leaves
        inner_parent = ParentNode("span", [leaf1, leaf2])

        # Create another parent with a leaf
        another_parent = ParentNode("em", [leaf3])

        # Create the outermost parent with both leaf and parent children
        outer_parent = ParentNode("div", [
            inner_parent,
            another_parent,
            LeafNode("p", "Paragraph text")
        ])
        result="<div><span><b>Bold text</b>Normal text</span><em><i>Italic text</i></em><p>Paragraph text</p></div>"
        self.assertEqual(outer_parent.to_html(), result)

    def test_no_children(self):
        with self.assertRaises(TypeError):
            node = ParentNode("p")

    def test_no_tag(self):
        leaf1 = LeafNode("b", "Bold text")
        with self.assertRaises(TypeError):
            node = ParentNode(leaf1)


if __name__ == "__main__":
    unittest.main()
