# 必要なライブラリをインポート
import time
from urllib import request
from bs4 import BeautifulSoup
import re

# 小説のURL
CodeList = [
    {'code': 'n6316bn', 'title': '転生したらスライムだった件', 'Page': ''},
    ]

def get_num_parts(code):
    """指定されたコードの小説の部数を取得する関数"""
    try:
        infotopurl = f"https://ncode.syosetu.com/novelview/infotop/ncode/{code}/"
        resinfo = request.urlopen(infotopurl)
        soupinfo = BeautifulSoup(resinfo, "html.parser")
        pattern = r'全(\d+(,\d+)*)部分'
        parts_str = re.search(pattern, soupinfo.find(id='pre_info').text).group(1)
        parts_str = parts_str.replace(',', '')  # カンマを削除
        return int(parts_str)
    except Exception as e:
        print(f"エラー発生: {e}")
        return 0


def download_novel_part(code, part):
    """小説の特定の部分をダウンロードする関数"""
    try:
        url = f"https://ncode.syosetu.com/{code}/{part}/"
        res = request.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")
        title = soup.find(class_='novel_subtitle').text
        honbun = soup.select_one("#novel_honbun").text
        return f"##{title}\n\n{honbun}\n"
    except Exception as e:
        print(f"エラー発生: {e}")
        return ""

def save_novel_text(filename, text):
    """ダウンロードしたテキストをファイルに保存する関数"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        print(f"ファイル保存中のエラー: {e}")

# 各小説の部数を取得してCodeListに格納
for Code in CodeList:
    Code['Page'] = get_num_parts(Code['code'])
    #進行状況を表示
    print(f"{Code['title']} : {Code['Page']}部")
    #待機
    time.sleep(2)
    

# 各小説の部数を表示
for Code in CodeList:
    print(f"{Code['title']} : {Code['Page']}")
# ダウンロードにかかる時間を表示
print(f"見積もり時間: 約{sum([Code['Page'] for Code in CodeList]) * 2}秒")

# 各小説のダウンロード処理
for Code in CodeList:
    downloaded_texts = []
    for part in range(1, Code['Page'] + 1):
        part_text = download_novel_part(Code['code'], part)
        downloaded_texts.append(part_text)
        # 進行状況を表示
        print(f"{Code['title']} : {part}部 / {Code['Page']}部")
        print(part_text[:50])  
        time.sleep(2)  # サーバーに負荷をかけないように待機

    combined_text = "\n".join(downloaded_texts)
    save_novel_text(f"{Code['title']}.txt", combined_text)
