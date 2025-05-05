import unittest

from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node, extract_title
from textnode import TextNode, TextType

class TestFunction(unittest.TestCase):
    

    
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result= [TextNode("This is text with a ", TextType.NORMAL), TextNode("code block", TextType.CODE), TextNode(" word", TextType.NORMAL),]
        self.assertEqual(new_nodes, result)

    def test_multi(self):
        node = TextNode("This is a text with **bold** and __italic__ formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", TextType.ITALIC)
        result= [
    TextNode("This is a text with ", TextType.NORMAL),
    TextNode("bold", TextType.BOLD),
    TextNode(" and ", TextType.NORMAL),
    TextNode("italic", TextType.ITALIC),
    TextNode(" formatting", TextType.NORMAL)
    ]
        self.assertEqual(new_nodes, result)

    def test_nested(self):
        node = TextNode("This is a text with **bold and __italic__** formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", TextType.ITALIC)
        result= [
    TextNode("This is a text with ", TextType.NORMAL),
    TextNode("bold and __italic__", TextType.BOLD),
    TextNode(" formatting", TextType.NORMAL)
    ]
        self.assertEqual(new_nodes, result)
        


    def test_nested_wrong_order(self):
        node = TextNode("This is a text with **bold and __italic__** formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        result= [
    TextNode("This is a text with **bold and ", TextType.NORMAL),
    TextNode("italic", TextType.ITALIC),
    TextNode("** formatting", TextType.NORMAL)
    ]
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertTrue("No closing delimiter" in str(context.exception))
        #self.assertEqual(new_nodes, result)



    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links(
        "This is text without a link"
    )
        self.assertListEqual([], matches)



    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL,
    )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.NORMAL,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
    )

    def test_no_link(self):
        node = TextNode("This is text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text", TextType.NORMAL)
            ],
            new_nodes
        )


    def test_no_image(self):
        node = TextNode("This is text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text", TextType.NORMAL)
            ],
            new_nodes
        )

    def test_only_image(self):
        node = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )

 
    def test_only_link(self):
        node = TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )

   

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)" 
        nodes = [
    TextNode("This is ", TextType.NORMAL),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.NORMAL),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.NORMAL),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.NORMAL),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.NORMAL),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
        result = text_to_textnodes(text)
        self.assertListEqual(nodes, result)


    def test_text_to_textnodes_empty(self):
        text = ""
        nodes = []
        result = text_to_textnodes(text)
        self.assertListEqual(nodes, result)


    def test_text_to_textnodes_no_format(self):
        text = "This is text"
        nodes = [TextNode("This is text", TextType.NORMAL)]
        result = text_to_textnodes(text)
        self.assertListEqual(nodes, result)



    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )


    def test_markdown_to_blocks_empty(self):
        md = ""
        print(md)
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_headings(self):
        md = """
    ### This is **bolded** heading

    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is <b>bolded</b> heading</h3><p>text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )



    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item with **bold**
    3. Third item with _italic_ and `code`
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i> and <code>code</code></li></ol></div>",
        )


    def test_unordered_list(self):
        md = """
    - First item
    - Second item with **bold**
    - Third item with _italic_ and `code`
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i> and <code>code</code></li></ul></div>",
        )

    def test_blockquote(self):
        md = """
    > This is a blockquote with **bold** text
    > and _italic_ and `code` as well.
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <b>bold</b> text and <i>italic</i> and <code>code</code> as well.</blockquote></div>",
        )


    def test_header_extraction(self):
        md = "# This is a header"

        title_extract = extract_title(md)
        
        self.assertEqual(
            title_extract,
            "This is a header",
        )
    
    def test_header_extraction_no_header(self):
        md = "This is no header"             
        
        with self.assertRaises(Exception) as context:
            title_extract = extract_title(md)
        self.assertTrue("No Header Found" in str(context.exception))
        



if __name__ == "__main__":
    unittest.main()

