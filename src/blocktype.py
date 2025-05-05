from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block_text):
    if block_text.startswith('#') and ' ' in block_text and block_text.index(' ') <= 6:
        return BlockType.HEADING
    
    if block_text.startswith('```') and block_text.endswith('```'):
        return BlockType.CODE
    
    lines = block_text.split('\n')
    non_empty_lines = [line for line in lines if line]  
    
    if all(line.startswith('>') for line in non_empty_lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in non_empty_lines):
        return BlockType.UNORDERED_LIST
    
    if is_ordered_list(block_text):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def is_ordered_list(block_text):
    lines = block_text.split("\n")
    for i, line in enumerate(lines, 1):  
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            return False
    return True

    
    