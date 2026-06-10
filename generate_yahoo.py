import xml.etree.ElementTree as ET
import requests

from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
update_time = datetime.now(JST).strftime("%Y/%m/%d %H:%M")

RSS_URL = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"

rss = requests.get(RSS_URL, timeout=30)

root = ET.fromstring(rss.content)

items = root.findall(".//item")

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body{{
    font-family:sans-serif;
    font-size:14px;
    margin:0;
    padding:10px;
}}
h3{{
    margin-top:0;
}}
.update{{
    color:#666;
    font-size:12px;
    margin-bottom:10px;
}}
.news{{
    margin-bottom:8px;
}}
a{{
    text-decoration:none;
}}
a:hover{{
    text-decoration:underline;
}}
</style>
</head>
<body>

<h3>📰 Yahoo!ニュース</h3>
<div class="update">最終更新: {update_time}</div>

"""

from email.utils import parsedate_to_datetime
from datetime import timedelta

for item in items[:15]:

    title = item.findtext("title", "")
    link = item.findtext("link", "")
    pub_date = item.findtext("pubDate", "")

    try:
        dt = parsedate_to_datetime(pub_date)

        # UTC → JST
        dt = dt + timedelta(hours=9)

        date_str = dt.strftime("%m/%d %H:%M")

    except Exception:
        date_str = ""

    html += f"""
    <div class="news">
      <span class="date">{date_str}</span>
      <a href="{link}" target="_blank">
        {title}
      </a>
    </div>
    """

html += """
</body>
</html>
"""

with open("yahoo.html", "w", encoding="utf-8") as f:
    f.write(html)
