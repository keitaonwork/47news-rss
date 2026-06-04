import requests
from bs4 import BeautifulSoup
from email.utils import format_datetime
from datetime import datetime
import xml.etree.ElementTree as ET

URL = "https://www.47news.jp/bulletin"

response = requests.get(URL, timeout=30)

response.encoding = response.apparent_encoding

html = response.text
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
    time_str = time_tag.get_text(strip=True)

    ET.SubElement(news, "description").text = time_str

    now = datetime.now()

    try:
        # 11時35分
        if "時" in time_str:

            hhmm = (
                time_str
                .replace("時", ":")
                .replace("分", "")
            )

            article_dt = datetime.strptime(
                f"{now.strftime('%Y-%m-%d')} {hhmm}",
                "%Y-%m-%d %H:%M"
            )

        # 06月03日
        elif "月" in time_str:

            md = (
                time_str
                .replace("月", "/")
                .replace("日", "")
            )

            article_dt = datetime.strptime(
                f"{now.year}/{md}",
                "%Y/%m/%d"
            )

        else:
            article_dt = now

        ET.SubElement(
            news,
            "pubDate"
        ).text = format_datetime(article_dt)

    except Exception:
        ET.SubElement(
            news,
            "pubDate"
        ).text = format_datetime(now)

tree = ET.ElementTree(rss)
xml_bytes = ET.tostring(
    rss,
    encoding="utf-8",
    xml_declaration=True
)

with open("feed.xml", "wb") as f:
    f.write(xml_bytes)
