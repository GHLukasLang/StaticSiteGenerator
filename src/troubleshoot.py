from textnode import *
from main import *
from functions import *
from htmlnode import *
from leafnode import *
from parentnode import *




md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """


md = """
Hello
World
"""
node = markdown_to_html_node(md)
html = node.to_html()
print(html)
