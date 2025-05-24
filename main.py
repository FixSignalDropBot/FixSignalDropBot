import os
import time
import datetime
import requests
import schedule
from bs4 import BeautifulSoup
import telebot

# Получаваме токена и ID на чата от променливи на средата или директно
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ТУК_СЛОЖИ_ТОКЕНА")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "ТУК_СЛОЖИ_ЧАТА")

# Проверка за валидни данни
if not TOKEN or not CHAT_ID:
    print("❌ Липсва TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID!")
    exit()

bot = telebot.TeleBot(TOKEN)

URL = "https://www.goaloo.mobi/1x2OddsDrop/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

last_sent = set()  # За да не се дублират мачове

def fetch_html():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        return response.text
    except Exception as e:
        print(f"[ГРЕШКА] Проблем с достъп до сайта: {e}")
        return ""

def parse_odds_drops(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'oddsTable'})
    matches = []

    if table:
        rows = table.find_all('tr')[1:]  # Пропускаме заглавния ред
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 7:
                time_ = cols[0].text.strip()
                league = cols[1].text.strip()
                teams = cols[2].text.strip()
                drop_type = cols[3].text.strip()
                odds_before = cols[4].text.strip()
                odds_after = cols[5].text.strip()
                drop_pct = cols[6].text.strip()

                try:
                    pct = float(drop_pct.replace('%', ''))
                except:
                    pct = 0

                if pct >= 11:
                    match_id = f"{time_}|{teams}|{odds_before}->{odds_after}"
                    if match_id not in last_sent:
                        matches.append({
                            'time': time_,
                            'league': league,
                            'teams': teams,
                            'drop_type': drop_type,
                            'odds_before': odds_before,
                            'odds_after': odds_after,
                            'drop_pct': pct,
                            'id': match_id
                        })

    return matches

def send_signals(signals):
    for match in signals:
        msg = f"\u2728 *Ново движение на коефициент!* \u2728\n"
        msg += f"\U0001F310 Лига: {match['league']}\n"
        msg += f"\U0001F3C0 Мач: {match['teams']}\n"
        msg += f"\u23F0 Час: {match['time']}\n"
        msg += f"\u2193 Тип: {match['drop_type']}\n"
        msg += f"\U0001F522 Спад: {match['odds_before']} ➜ {match['odds_after']} ({match['drop_pct']}%)"

        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
        last_sent.add(match['id'])

def job():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Сканирам за нови сигнали...")
    html = fetch_html()
    if not html:
        print("Не успях да заредя страницата.")
        return
    signals = parse_odds_drops(html)
    if signals:
        send_signals(signals)
    else:
        print("Няма нови сигнали.")

# Задача на всеки 5 минути
schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    print("✅ Ботът е стартиран и работи...")
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)
