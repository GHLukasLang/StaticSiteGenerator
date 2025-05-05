from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        if text_type not in TextType:
            raise ValueError(f"text_type must be a member of TextType, got {text_type}")
        self.text = text
        self.text_type = text_type
        self.url = url
    

    def __eq__(self, node):
        if not isinstance(node, TextNode):
            return False
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url
          
    def __repr__(self):
        url_part = f", {self.url}" if self.url is not None else ""
        return f"TextNode({self.text}, {self.text_type.value}, {url_part})"
    




def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Wrong TextType")
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, value=text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})


