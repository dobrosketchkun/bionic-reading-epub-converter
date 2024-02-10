"""Util functions to bold text in asimilar way to the bionic reading format"""
from math import ceil, log
import string
import re

AMPERSAND = "&"
SEMICOLON = ";"
AMPERSAND_ENTITY = f"{AMPERSAND}amp{SEMICOLON}"

def bold_token_part_by_position(token_part:str, position:int)->str:
    """Bold a string until a given position of the characters in the string"""
    bold_part = token_part[:position]
    normal_part = token_part[position:]

    new_token_part = f"<b>{bold_part}</b>{normal_part}"

    return new_token_part


def _is_formatted_text(text:str)->bool:
    """Check for special characteres of a page that do not need text bolding"""

    is_formatted = False
    formatted_text_to_check = ["@page", "margin:"]
    if not text.strip() or any(formatting in text for formatting in formatted_text_to_check):
        is_formatted = True

    return is_formatted


def process_token_part(token_part:str)->str:
    """Process token part and assign a bold format given for a given position"""
    if token_part in string.punctuation or token_part in string.digits:
        new_token_part = token_part

    else:
        if token_part == AMPERSAND_ENTITY:
            new_token_part = f"<b>{token_part}</b>"
        elif len(token_part) <= 3:
            new_token_part = bold_token_part_by_position(token_part=token_part, position=2)
        else:
            bold_stop = ceil(log(len(token_part), 1.8))
            new_token_part = bold_token_part_by_position(token_part=token_part, position=bold_stop)

    return new_token_part

def bold_text(text):
    """Bold the parts of a text in the bionic reading format"""

    text_tokens = text.split(" ")
    new_text = ''

    for i, token in enumerate(text_tokens):
        new_token = ''
        if _is_formatted_text(token):
            new_token = token
        else:
            token_parts = re.findall( r'\w+|[^\s\w]+', token)
            recomposed_token_parts = recompose_token_if_ampersand(token_parts)
            for token_part in recomposed_token_parts:
                new_token_part = process_token_part(token_part)
                new_token += new_token_part

        if i == 0:
            new_text += new_token
        else:
            new_text += f" {new_token}"

    return new_text

def recompose_token_if_ampersand(token_list):
    """Recomposes text tokens containing '&' and ';' into '&amp;'"""

    if AMPERSAND in token_list and SEMICOLON in token_list:
        amp_idx = token_list.index(AMPERSAND)
        semicolon_idx = token_list.index(SEMICOLON)
        special_char = "".join(token_list[amp_idx:semicolon_idx + 1])
        return token_list[:amp_idx] + [special_char] + token_list[semicolon_idx + 1:]
    else:
        return token_list