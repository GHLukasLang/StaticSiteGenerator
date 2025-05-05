import unittest

from blocktype import *

class TestBlocktype(unittest.TestCase):

    def test_blocktype_paragraph(self):
        md = "This is a markdown block without any formatting. \nIt has multiple lines, though. \nEven a third."
        result = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, result)


    def test_blocktype_heading(self):
        md = "### This is a heading"
        result = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, result)


    def test_blocktype_heading2(self):
        md = "### This is a heading\n #Another headline"
        result = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, result)
    
    def test_blocktype_code(self):
        md = "```CODEBLOCK\n \n \n with a lot of code\n on multiple lines.```"
        result = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, result)

    def test_blocktype_quote(self):
        md = ">quotations\n>upon quotations\n>open quotations"
        result = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, result)

    def test_unordered_list(self):
        md = "- first item\n- second item\n- third item"
        result = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, result)

    def test_ordered_list(self):
        md = "1. first item\n2. second item\n3. third item"
        result = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, result)


if __name__ == "__main__":
    unittest.main()


