"""Util functions to handle html files from an epub"""
from typing import Union, List
from pathlib import Path
from zipfile import ZipFile
import shutil

from utils.bold_text import bold_text
from utils.epub_html_parser import EPUBHTMLParser


FIRST_TAGS = """<?xml version='1.0' encoding='utf-8'?>
    <!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n"""


def collect_html_from_folder(folder_path: Union[str, Path])->List[Path]:
    """Recursively collects the html files in a folder"""

    htmls = [file_path for file_path in Path(folder_path).rglob("*") if "htm" in file_path.suffix]

    return htmls

def unzip_epub_file(epub_path: Union[str, Path])->Union[str,Path]:
    """Unzips the content of an epub file to the parent folder of the file"""

    unzip_path = f"{Path(epub_path).parent}/{Path(epub_path).stem}_BR"

    with ZipFile(epub_path, 'r') as zip_obj:
        zip_obj.extractall(unzip_path)

    return unzip_path


def open_html(html_path: Union[str, Path]):
    """Open an html file"""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_data = f.read()

    return html_data

def save_html(html_content, output_html_path: Union[str, Path]):
    """Save an html file"""

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def zip_html_files_as_epub(folder_to_compress: Union[str, Path]):
    """Zips a folder with html files and then converts the zip into epub format"""
    file_path= f"{folder_to_compress}"
    shutil.make_archive(base_name=folder_to_compress, format='zip', root_dir=folder_to_compress)
    zip_file = Path(f"{file_path}.zip")
    zip_file.rename(zip_file.with_suffix(".epub"))
    shutil.rmtree(folder_to_compress)


def handle_start_tag_of_html(html_part: str)->str:
    """Convert start tag of html to a string"""

    tag = '<' + html_part[0][1]
    full_attr = []
    for attr in html_part[1][1]:
        full_attr.append(attr[0] + f'="{attr[1]}"')
    full_attr = ' '.join(full_attr)
    if not full_attr:
        tag += full_attr + '>'
    else:
        tag += ' ' + full_attr + '>'

    return tag


def handle_end_tag_of_html(html_part: str)->str:
    """Convert end tag of html to a string"""

    tag = f"</{html_part[1]}>"

    return tag

def handle_epub_html_files(epub_html_list: List[str]):
    """Read html files from an epub to convert them to bionic reading format"""

    for html_file in epub_html_list:

        html_content = open_html(html_path=html_file)

        data_html = []
        parser = EPUBHTMLParser(data_list=data_html)
        parser.feed(html_content)

        full_html = ''
        for html_part in data_html:
            if html_part[0] == 'Data:':
                full_html += bold_text(html_part[1])

            if len(html_part) == 2 and html_part[0][0] == 'Start tag:':
                full_html += handle_start_tag_of_html(html_part=html_part)

            if html_part[0] == 'End tag:':
                full_html += handle_end_tag_of_html(html_part=html_part)

        full_html = FIRST_TAGS + full_html

        save_html(html_content=full_html, output_html_path=html_file)
