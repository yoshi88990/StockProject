import urllib.request
import xml.etree.ElementTree as ET
import datetime

def fetch_latest_news():
    print("【WORLD NEWS NODE】世界の最先端ニュース（テクノロジー・AI・世界情勢）を網羅的に取得中...")
    
    # 取得するRSSフィードのURL（Google Newsのテクノロジーとワールド）
    urls = {
        "最先端テクノロジー（AI・IT）": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ja&gl=JP&ceid=JP:ja",
        "世界情勢（World News）": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ja&gl=JP&ceid=JP:ja"
    }

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    markdown_content = f"# 世界の最先端ニュース (自動収集時刻: {now_str})\n\n"

    for category, url in urls.items():
        markdown_content += f"## 【{category}】\n"
        try:
            # ニュースの取得（スクレイピング対策で仮想ブラウザ偽装）
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # 上位15件を抽出（最先端の情報を漏らさず取得）
                count = 0
                for item in root.findall('.//item'):
                    if count >= 15:
                        break
                    title = item.find('title').text
                    link = item.find('link').text
                    pubDate = item.find('pubDate').text
                    markdown_content += f"- **{pubDate}**: [{title}]({link})\n"
                    count += 1
            print(f"> {category} の最新データを15件確保しました。")
            markdown_content += "\n"
        except Exception as e:
            markdown_content += f"取得エラー: {e}\n\n"

    # ファイルに書き込み
    filename = "最新_世界ニュース.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n✅ 取得完了！！！『{filename}』に全ての最先端ニュースを叩き込みました。")

if __name__ == "__main__":
    fetch_latest_news()
