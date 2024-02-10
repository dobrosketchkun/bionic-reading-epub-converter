"""HTML Parser Class"""
from html.parser import HTMLParser
from html.entities import name2codepoint

class EPUBHTMLParser(HTMLParser):
    """HTML Parser Class for EPUB files"""
    def __init__(self, data_list):
        HTMLParser.__init__(self)
        self.data_html = data_list

    def handle_data(self, data):
        """Append retrieved data to a list"""        
        self.data_html.append(("Data:", data.replace("&", "&amp;")))

    def handle_starttag(self, tag, attrs):
        attributes = []
        for attr in attrs:
            if "&" in attr[1]:
                attr = (attr[0], attr[1].replace("&", "&amp;"))
            attributes.append(attr)
        self.data_html.append((("Start tag:", tag), ("attr:", attributes)))

    def handle_endtag(self, tag):
        self.data_html.append(("End tag:", tag))

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
