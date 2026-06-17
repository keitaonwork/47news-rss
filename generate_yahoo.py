import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

JST = timezone(timedelta(hours=9))
update_time = datetime.now(JST).strftime("%m/%d %H:%M")

RSS_URL = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"

rss = requests.get(RSS_URL, timeout=30)
root = ET.fromstring(rss.content)
items = root.findall(".//item")

# 47NEWSのデザインと100%一致させたHTML・CSSを構築
html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  /* 外枠をなくし、埋め込みパーツとして最適化 */
  body {{
    font-family: 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
    border-radius: 14px;
    padding: 14px 18px;
    margin: 0;
    color: #374151;
  }}

  /* ヘッダーデザイン */
  .news-header {{
    font-size: 15px;
    font-weight: bold;
    color: #0284c7;
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(37, 99, 235, 0.15);
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .header-icon {{ font-size: 16px; }}

  /* 最終更新日時 */
  .update-time {{
    font-size: 11px;
    color: #9ca3af;
    margin-bottom: 6px;
    text-align: right;
  }}

  /* リスト全体の余白リセット */
  ul {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}
  
  /* 行間・上下余白・文字サイズを完全統一 */
  li {{
    padding: 5px 4px;
    border-bottom: 1px dashed rgba(0, 0, 0, 0.05);
    font-size: 13.5px;
    line-height: 1.3;
    display: flex; 
    align-items: flex-start;
    gap: 10px;
  }}
  li:last-child {{
    border-bottom: none;
  }}

  /* 更新日時のデザイン（グレーのバッジ風） */
  .news-date {{
    font-size: 11px;
    color: #6b7280;
    background: rgba(0, 0, 0, 0.04);
    padding: 1px 6px;
    border-radius: 4px;
    white-space: nowrap; 
    margin-top: 1px;
  }}

  /* 記事リンク */
  a {{
    color: #374151;
    text-decoration: none;
    flex: 1; 
    transition: color 0.15s ease;
  }}
  a:hover {{
    color: #0284c7;
    text-decoration: underline;
  }}
</style>
</head>
<body>

<div class="news-header">
  <span class="header-icon"> Yahoo!ニュース トピックス (GitHub連携)
</div>

<div class="update-time">
  最終更新: {update_time}
</div>

<ul>
"""

# 最大20件を取得
for item in items[:20]:
    title = item.findtext("title", "")
    link = item.findtext("link", "")
    pub_date = item.findtext("pubDate", "")

    try:
        # Yahoo!の「最初から日本時間」のデータをそのまま正しく解析
        dt = parsedate_to_datetime(pub_date)
        date_str = dt.strftime("%m/%d %H:%M")
    except Exception:
        date_str = ""

    html += f"""  <li>
    {f'<span class="news-date">{date_str}</span>' if date_str else ''}
    <a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a>
  </li>
"""

html += """</ul>
</body>
</html>
"""

with open("yahoo.html", "w", encoding="utf-8") as f:
    f.write(html)
print("yahoo.html を正しい時間で更新しました。")
