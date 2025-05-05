from textnode import TextNode, TextType
from htmlnode import HTMLNode
from functions import markdown_to_html_node, extract_title
import os
import shutil


def main():

    copy_function("static", "public")

    

    generate_pages_recursive("content/", "template.html", "public/")
   

def copy_function(src, dst):
    #check if the destionation is valid
    if os.path.exists(dst):
        #clear the destination:
        shutil.rmtree(dst)

    # Recreate the destination directory
    os.mkdir(dst)
    
    #loop through the src
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        #check for file or dir
        if os.path.isfile(src_item):
    # Skip Zone.Identifier files if they exist
            if not src_item.endswith(":Zone.Identifier"):
                shutil.copy(src_item, dst_item)
                print(f"Copied file: {src_item} to {dst_item}")
        else:
            print(f"Processing directory: {src_item}")
            #its a directory, call the function again
            copy_function(src_item, dst_item)
          
    
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(f'{from_path}') as file_object_origin:
        md_origin = file_object_origin.read()


    with open(f"{template_path}") as file_object_template:
        template = file_object_template.read()

    htmlnode = markdown_to_html_node(md_origin)
    html_content = htmlnode.to_html()
    title = extract_title(md_origin)

    template_filled = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    if not os.path.dirname(dest_path):
        os.makedirs(dest_path)
    
    with open(f"{dest_path}", "w") as f:
        f.write(f"{template_filled}")





def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dst_item = os.path.join(dest_dir_path, item)

        #check for file or dir
        if os.path.isdir(src_item):
               #make a directory and call function again
            os.makedirs(dst_item)
        
            generate_pages_recursive(src_item, template_path, dst_item)
        else:
            if src_item.endswith(".md"):
                dst_item = dst_item.replace('.md', '.html')
                generate_page(src_item, template_path, dst_item)
    
    


main()