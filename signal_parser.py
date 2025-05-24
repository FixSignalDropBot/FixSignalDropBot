
import requests
from bs4 import BeautifulSoup
import telebot
import os
import time

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ТУК_СЛОЖИ_ТОКЕНА_АКО_НЯМАШ_ENV")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "ТУК_СЛОЖИ_ЧАТ_ID")

bot = telebot.TeleBot(TOKEN)
BASE_URL = "https://m.goaloo.com"
DROP_URL = f"{BASE_URL}/1x2OddsDrop/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

sent_links = set()

def fetch_main_page():
    response = requests.get(DROP_URL, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser")

def extract_match_links(soup):
    links = []
    for a in soup.select("a[href*='/football/']"):
        href = a.get("href")
        if "/oddscomp-" in href:
            full_url = BASE_URL + href
            if full_url not in sent_links:
                links.append(full_url)
    return links

def parse_drop_page(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "odds-table"})
    title = soup.find("title").text.strip()
    match_name = title.split("oddscomp")[0].strip().replace("–", "-")

    signal_lines = []
    if table:
        rows = table.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                time = cols[0].text.strip()
                score = cols[1].text.strip()
                handy = cols[2].text.strip()
                home = cols[3].text.strip()
                away = cols[4].text.strip()
                signal_lines.append(f"{time} | {score} | {handy} | {home} | {away}")

    if len(signal_lines) >= 3:
        message = f"⚽ Мач: {match_name}\n"
        message += f"📊 Последни движения:\n"
        message += "\n".join(signal_lines[:6]) + "\n"
        message += f"🔗 {url}"
        return message

    return None

def run():
    soup = fetch_main_page()
    links = extract_match_links(soup)

    for link in links:
        if link not in sent_links:
            signal = parse_drop_page(link)
            if signal:
                bot.send_message(CHAT_ID, signal)
                sent_links.add(link)
            time.sleep(2)  # За да не се претоварва сървърът

if __name__ == "__main__":
    run()
