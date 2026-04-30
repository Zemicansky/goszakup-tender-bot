import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

# ---------------- НАСТРОЙКИ (ЗАПОЛНИ СВОИ ДАННЫЕ) ----------------
BOT_TOKEN = "8754810003:AAGb1d92yvLpY92m3lRMDPYkY2OeyEwpW7M"
CHAT_ID = "1007470697"
CHECK_INTERVAL = 600  # Проверка новых тендеров каждые 10 минут (в секундах)
# -------------------------------------------------------------------

URL = "https://www.goszakup.gov.kz/ru/search/announce"
sent_tenders = set()

bot = Bot(token=BOT_TOKEN)

def parse_tenders():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        res = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("div", class_="announce-item")
        new_list = []

        for item in items:
            try:
                title = item.find("div", class_="announce-title").text.strip()
                price = item.find("div", class_="announce-price").text.strip()
                link_href = item.find("a")["href"]
                link = "https://www.goszakup.gov.kz" + link_href
                tender_id = link

                if tender_id not in sent_tenders:
                    new_list.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "id": tender_id
                    })
            except:
                continue
        return new_list
    except:
        return []

def send_message(tender):
    text = f"""🆕 Новый тендер

📋 Суть работы:
{tender['title']}

💰 Цена: {tender['price']}

🔗 Ссылка: {tender['link']}"""
    bot.send_message(chat_id=CHAT_ID, text=text)

def main():
    print("Бот запущен на твоём ПК, жду новые тендеры...")
    while True:
        tenders = parse_tenders()
        for t in tenders:
            send_message(t)
            sent_tenders.add(t["id"])
            time.sleep(1)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
