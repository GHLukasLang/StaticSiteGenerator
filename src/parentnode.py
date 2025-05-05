from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        string = ""
        for child in self.children:
            #if isinstance(child, LeafNode):
            string += child.to_html()
        return f"<{self.tag}>{string}</{self.tag}>"


