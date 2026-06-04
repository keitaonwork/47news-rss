import requests
from bs4 import BeautifulSoup
from email.utils import formatdate
from datetime import datetime
import xml.etree.ElementTree as ET

URL = "https://www.47news.jp/bulletin"

html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

rss = ET.Element("rss")
rss.set("version", "2.0")

channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "47NEWS速報"
ET.SubElement(channel, "link").text = URL
ET.SubElement(channel, "description").text = "47NEWS速報RSS"

for item in soup.select("a.post_item")[:50]:

    title_tag = item.select_one(".item_ttl")
    time_tag = item.select_one(".item_time")

    if not title_tag:
        continue

    href = item.get("href", "")

    if href.startswith("/"):
        href = "https://www.47news.jp" + href

    news = ET.SubElement(channel, "item")

    ET.SubElement(news, "title").text = title_tag.get_text(strip=True)
    ET.SubElement(news, "link").text = href

    if time_tag:
        ET.SubElement(news, "description").text = time_tag.get_text(strip=True)

    ET.SubElement(news, "pubDate").text = formatdate()

tree = ET.ElementTree(rss)
tree.write(
    "feed.xml",
    encoding="utf-8",
    xml_declaration=True
)
