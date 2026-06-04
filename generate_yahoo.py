import xml.etree.ElementTree as ET
import requests

RSS_URL = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"

rss = requests.get(RSS_URL, timeout=30)

root = ET.fromstring(rss.content)

items = root.findall(".//item")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body{
    font-family:sans-serif;
    font-size:14px;
    margin:0;
    padding:10px;
}
h3{
    margin-top:0;
}
.news{
    margin-bottom:8px;
}
a{
    text-decoration:none;
}
a:hover{
    text-decoration:underline;
}
</style>
</head>
<body>

<h3>📰 Yahoo!ニュース</h3>

"""

from email.utils import parsedate_to_datetime

for item in items[:15]:

    title = item.findtext("title", "")
    link = item.findtext("link", "")
    pub_date = item.findtext("pubDate", "")

    try:
        dt = parsedate_to_datetime(pub_date)
        date_str = dt.strftime("%m/%d %H:%M")
    except:
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
