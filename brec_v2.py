import os
import regex
import zipfile
import argparse
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def bionic_word(word):
    if len(word) <= 1:
        return word
    elif len(word) <= 3:
        return f"<b>{word[:1]}</b>{word[1:]}"
    else:
        midpoint = len(word) // 2
        return f"<b>{word[:midpoint]}</b>{word[midpoint:]}"

def process_text(text):
    word_pattern = regex.compile(r'\b[\p{L}\p{M}]+\b', regex.UNICODE)
    
    def replace_word(match):
        word = match.group(0)
        return bionic_word(word)
    
    return word_pattern.sub(replace_word, text)

def process_html_content(content):
    soup = BeautifulSoup(content, 'lxml')
    
    skip_tags = {'script', 'style', 'pre', 'code'}
    
    for element in soup.find_all(text=True):
        if element.parent.name not in skip_tags:
            new_text = process_text(element.string)
            new_element = BeautifulSoup(new_text, 'html.parser')
            element.replace_with(new_element)
    
    return str(soup)

def process_epub(input_path, output_path):
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        file_list = zip_ref.infolist()
        total_files = len(file_list)
        
        with zipfile.ZipFile(output_path, 'w') as zip_out:
            with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
                for file_info in file_list:
                    with zip_ref.open(file_info) as file:
                        content = file.read()
                        
                        if file_info.filename.endswith(('.html', '.xhtml', '.htm')):
                            content = process_html_content(content)
                        elif file_info.filename.endswith('content.opf'):
                            # Do not modify content.opf
                            pass
                        
                        zip_out.writestr(file_info, content)
                    
                    pbar.update(1)
                    pbar.set_postfix(current_file=file_info.filename)

def main():
    parser = argparse.ArgumentParser(description='Convert EPUB to Bionic Reading format')
    parser.add_argument('input', help='Input EPUB file path')
    parser.add_argument('output', help='Output EPUB file path')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    if os.path.exists(args.output):
        print(f"Warning: Output file '{args.output}' already exists. It will be overwritten.")

    try:
        process_epub(args.input, args.output)
        print(f"Conversion complete. Output saved to '{args.output}'")
    except Exception as e:
        print(f"Error occurred during processing: {str(e)}")

if __name__ == "__main__":
    main()
