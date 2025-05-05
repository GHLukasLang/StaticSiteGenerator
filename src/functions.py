import re
import textwrap

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from blocktype import *
from parentnode import ParentNode
from leafnode import LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.NORMAL:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            while delimiter in text:
                start_index = text.find(delimiter)
                if start_index > 0:
                    new_nodes.append(TextNode(text[:start_index], TextType.NORMAL))

                end_index = text.find(delimiter, start_index + len(delimiter))
                if end_index == -1:
                    raise Exception(f"No closing delimiter {delimiter} found")

                content = text[start_index +len(delimiter):end_index]
                new_nodes.append(TextNode(content, text_type))

                text = text[end_index + len(delimiter):]
            
            if text:
                new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        #do we need this?
        #if one of the nodes is a texttype bold?
        if old_node.text_type is not TextType.NORMAL:
            new_nodes.append(old_node)
        else:
            #get the images from the node
            match = extract_markdown_images(old_node.text) #gets a list of tuples
            
            text = old_node.text
            if not match:  # If no images were found
                new_nodes.append(old_node)  # Keep the original node
            else:
    # Your existing image processing code
            #as long as there is something in match, we are not done yet
                while match != []:
                    alt_text, alt_link = match[0]
                    sections = text.split(f"![{alt_text}]({alt_link})", 1) #list of strings
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, alt_link))
                    text = sections[1]
                    del match[0]
                    # After the while loop
                if text:  # Only append if text is not empty
                    new_nodes.append(TextNode(text, TextType.NORMAL))
             

    return new_nodes     

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        #do we need this?
        #if one of the nodes is a texttype bold?
        if old_node.text_type is not TextType.NORMAL:
            new_nodes.append(old_node)
        else:
            #get the images from the node
            match = extract_markdown_links(old_node.text) #gets a list of tuples
            
            text = old_node.text
            if not match:  # If no images were found
                new_nodes.append(old_node)  # Keep the original node
            else:
    # Your existing image processing code
            #as long as there is something in match, we are not done yet
                while match != []:
                    alt_text, alt_link = match[0]
                    sections = text.split(f"[{alt_text}]({alt_link})", 1) #list of strings
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, alt_link))
                    text = sections[1]
                    del match[0]
                    # After the while loop
                if text:  # Only append if text is not empty
                    new_nodes.append(TextNode(text, TextType.NORMAL))
             

    return new_nodes   


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
       
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches



def text_to_textnodes(text):

    text_node = TextNode(text, TextType.NORMAL)

    bold = split_nodes_delimiter([text_node], "**", TextType.BOLD)

    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)

    code = split_nodes_delimiter(italic, "`", TextType.CODE)

    image = split_nodes_image(code)

    link = split_nodes_link(image)

    return link



def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    cleaned_sections = []
    for section in sections:
        cleaned_section = section.strip()
        dedented = textwrap.dedent(cleaned_section)

        if dedented:
            # Split into lines, strip each line, then rejoin
            lines = [line.strip() for line in dedented.split("\n")]
            dedented_cleaned_section = "\n".join(lines)
            cleaned_sections.append(dedented_cleaned_section)
    return cleaned_sections


def markdown_to_html_node(markdown):
    children_nodes = []
    ##split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    ##loop over each block
    for block in blocks:

        ##determine the blocktype
        type_of_block = block_to_block_type(block)

        ##Based on the type of block, create a new HTMLNode with the proper data
        if type_of_block == BlockType.PARAGRAPH:
            paragraph_node = md_to_html_paragraph(block)
            children_nodes.append(paragraph_node)

        if type_of_block == BlockType.HEADING:
            heading_node = md_to_html_heading(block)
            children_nodes.append(heading_node)

        if type_of_block == BlockType.QUOTE:
            quote_node = md_to_html_quote(block)
            children_nodes.append(quote_node)
        
        if type_of_block == BlockType.UNORDERED_LIST:
            unorderedlist_node = md_to_html_unorderedlist(block)
            children_nodes.append(unorderedlist_node)
        
        if type_of_block == BlockType.ORDERED_LIST:
            orderedlist_node = md_to_html_orderedlist(block)
            children_nodes.append(orderedlist_node)
        
        if type_of_block == BlockType.CODE:
            code_node = md_to_html_code(block)
            children_nodes.append(code_node)

    return ParentNode(tag="div", children= children_nodes)
        


def md_to_html_paragraph(paragraph):
    lines = paragraph.splitlines()
    joined = " ".join(line.strip() for line in lines)   
    return ParentNode(tag="p", children = text_to_children(joined))



def md_to_html_heading(heading):
    children_nodes = []
    heading_text = heading.split(' ', 1)[1].strip()
    html_children = text_to_children(heading_text)
    children_nodes.extend(html_children)
    return ParentNode(tag=f"h{heading.index(" ")}", children= children_nodes)
  



def md_to_html_quote(quote):
    children_nodes = []

    lines = quote.split('\n')
    format_removed = [line[1:].lstrip() for line in lines]
    non_empty_lines = [line for line in format_removed if line]  


    body_text = " ".join(non_empty_lines)
    children_nodes = text_to_children(body_text)

    return ParentNode(tag="blockquote", children= children_nodes)
    


def md_to_html_unorderedlist(unordered_list):
    children_nodes = []
    lines = unordered_list.split('\n')
    format_removed = [line[1:].lstrip() for line in lines]
    non_empty_lines = [line for line in format_removed if line]  


    for line in non_empty_lines:
        html_children = text_to_children(line)
        li_node = ParentNode("li", children=html_children)
        children_nodes.append(li_node)
    
    return ParentNode(tag="ul", children=children_nodes)



def md_to_html_orderedlist(ordered_list):
    children_nodes = []
    lines = ordered_list.split('\n')
    format_removed = [re.sub(r"^\d+\.\s*", "", line) for line in lines]
    non_empty_lines = [line for line in format_removed if line]  


    for line in non_empty_lines:
        html_children = text_to_children(line)
        li_node = ParentNode("li", children=html_children)
        children_nodes.append(li_node)
    
    return ParentNode(tag="ol", children=children_nodes)
    


def md_to_html_code(code):
    code_block = code[3:-3]
    dedented = textwrap.dedent(code_block)
    stripped = dedented.lstrip("\n")
    code_textnode = TextNode(stripped, TextType.CODE)
    child_node = text_node_to_html_node(code_textnode)
    return ParentNode(tag="pre", children=[child_node])



    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)  # returns list of TextNodes
    html_children = []
    for node in text_nodes:
        html_children.append(text_node_to_html_node(node))
    return html_children  # Now a list of LeafNodes (HTMLNodes)




def extract_title(markdown):
    if not markdown.startswith('# '):
        raise Exception("No Header Found")
    header = markdown.strip("# ")
    return header
    
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    

