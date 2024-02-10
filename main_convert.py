"""Main script to perform conversion of an epub file to bionic reading format"""
from typing import Union
from pathlib import Path
import logging
import fire

from utils import html_file_utils



def convert_epub(epub_path: Union[str, Path]):
    """Converts an epub file to a format where the first parts of a word are higlgihted with bold letters.

    Parameters
    ----------
    epub_path : Union[str, Path]
        path of the epub file
    """

    logger = logging.getLogger(__name__)
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    logger.info(f"File to convert: {epub_path}")
    logger.info("Processing file...")
    unzip_path = html_file_utils.unzip_epub_file(epub_path=epub_path)
    html_files = html_file_utils.collect_html_from_folder(unzip_path)

    logger.info("Handling html files to bold text")
    html_file_utils.handle_epub_html_files(epub_html_list=html_files)

    logger.info("Finishing conversion")
    html_file_utils.zip_html_files_as_epub(folder_to_compress=unzip_path)


if __name__ == "__main__":
    fire.Fire(convert_epub)
