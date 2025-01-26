from textnode import TextNode, TextType
import shutil, os
from block_markdown import markdown_to_html_node, extract_title

def remove_existing_public(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    entries = os.listdir(directory)
    for entry in entries:
        entry_full_path = os.path.join(directory, entry)
        if os.path.isdir(entry_full_path):
            remove_existing_public(entry_full_path)
            os.rmdir(entry_full_path)
            print(f"Deleting folder {entry_full_path}")
        else:
            os.remove(entry_full_path)
            print(f"Deleting file {entry_full_path}")

def copy_static(root, destination):
    entries = os.listdir(root)
    for entry in entries:
        entry_full_path = os.path.join(root, entry)
        if os.path.isfile(entry_full_path):
            shutil.copy(entry_full_path, destination)
            print(f"Copying file {entry_full_path}")
        else:
            newdir = os.path.join(destination, entry)
            os.makedirs(newdir, exist_ok = True)
            print(f"Copying directory {entry}")
            copy_static(entry_full_path, newdir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    os.path.dirname(from_path)
    with open(from_path,"r") as f:
        markdown_text = f.read()
    with open(template_path,"r") as f:
        temp_text = f.read()
    html_text = markdown_to_html_node(markdown_text)
    html_text = html_text.to_html()
    html_title = extract_title(markdown_text)
    new_temp = temp_text.replace("{{ Content }}",html_text).replace("{{ Title }}",html_title)

    with open(os.path.join(dest_path),"w") as f:
        f.write(new_temp)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        entry_full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_full_path) and entry.endswith(".md"):
            filename = os.path.join(dest_dir_path,"index.html")
            generate_page(entry_full_path,template_path, filename)
        elif os.path.isdir(entry_full_path):
            created_dir = os.path.join(dest_dir_path, entry)
            os.mkdir(created_dir)
            generate_pages_recursive(entry_full_path, template_path, created_dir)




def main():
    src_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(src_path,"..")
    public_path = os.path.join(root_path,"public/")
    static_path = os.path.join(root_path,"static/")

    remove_existing_public(public_path)
    copy_static(static_path,public_path)

    generate_pages_recursive(os.path.join(root_path,"content/"),
                  os.path.join(root_path,"template.html"),
                  public_path)
    print("copying and removing complete")

if __name__ =="__main__":
    main()