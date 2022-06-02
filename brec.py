from html.entities import name2codepoint
from html.parser import HTMLParser
from zipfile import ZipFile
from math import ceil, log
import argparse
import shutil
import string
import re
import os



class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global data_html
        # print("Start tag:", tag)
        attributes = []
        for attr in attrs:
            # print("     attr:", attr)
            attributes.append(attr)
        data_html.append((("Start tag:", tag), ("attr:", attributes)))

    def handle_endtag(self, tag):
        global data_html
        # print("End tag  :", tag)
        data_html.append(("End tag:", tag))

    def handle_data(self, data):
        global data_html
        data_html.append(("Data:", data))
        # print("Data     :", data)

    def handle_comment(self, data):
        pass
        # print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        # print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        # print("Num ent  :", c)

    def handle_decl(self, data):
        pass
        # print("Decl     :", data)

def bolding(text):
    parts = re.findall( r'\w+|[^\s\w]+', text)
    new_text = ''
    for part in parts:
        if part in string.punctuation or part in string.digits:
            new_text += part
        else:
            if len(part) <= 3:
                new_part = ''
                new_part = f"<b>{part[0]}</b>"
                new_part += ''.join(part[1:])
                new_text += ' ' + new_part
            else:
                point = ceil(log(len(part), 2))
                new_part = ''
                new_part = f"<b>{part[0:point]}</b>"
                new_part += ''.join(part[point:])
                new_text += ' ' + new_part 
    return new_text      



####################################


parser = argparse.ArgumentParser()
parser.add_argument("epubfile", help="put a path to your epub file in here")
args = parser.parse_args()
file_path = args.epubfile
file_name = os.path.basename(file_path)
epub_path = os.getcwd() +'/bionic_' + file_name
unzip_path_folder = file_name + '_zip/' 
unzip_path = os.getcwd() + '/' + unzip_path_folder


try:
    with ZipFile(file_path, 'r') as zipObj:
        zipObj.extractall(unzip_path)
except:
    with ZipFile(os.getcwd() + '/' + file_path, 'r') as zipObj:
        zipObj.extractall(unzip_path)


####################################

first_tags = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n"""


htmls = []
# r=root, d=directories, f = files
for r, d, f in os.walk(unzip_path):
    for hfile in f:
        if hfile[-4:] == 'html':
            htmls.append(os.path.join(r, hfile))


for html in htmls:
  
    with open(html, 'r', encoding='utf-8') as f:
        html_data = f.read()

    data_html = []
    parser = MyHTMLParser()
    parser.feed(html_data)

    full_html = ''
    for html_part in data_html:
        # print(html_part, '\n')
        if html_part[0] == 'Data:':
            # full_html += html_part[1]
            # full_html += f"<b>{html_part[1]}</b>"
            full_html += bolding(html_part[1])
            

        if len(html_part) == 2 and html_part[0][0] == 'Start tag:':
            tag = '<' + html_part[0][1] 
            full_attr = []
            for attr in html_part[1][1]:
                full_attr.append(attr[0] + f'="{attr[1]}"')
            full_attr = ', '.join(full_attr)
            if not full_attr:
                tag += full_attr + '>'
            else:
                tag += ' ' + full_attr + '>'
            full_html += tag
        if html_part[0] == 'End tag:':
            tag = f"</{html_part[1]}>"
            full_html += tag
    full_html = first_tags + full_html

    with open(html, 'w', encoding='utf-8') as f:
        f.write(full_html)


####################################

os.chdir(unzip_path)
shutil.make_archive(epub_path, 'zip', './')
os.rename((epub_path + '.zip'), (epub_path + '.zip')[:-4])

