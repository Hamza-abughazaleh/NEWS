import html2text
import re


def parse_descreption_to_text(description):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    html = description
    text = text_maker.handle(html)
    text = re.sub('[!@#$%*]', '', text).strip()
    return text


def image_res(website, image):
    if website[:3] == "TRT":
        return image.replace("/w32", "/w960")
