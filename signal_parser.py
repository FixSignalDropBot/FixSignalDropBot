import requests
from bs4 import BeautifulSoup
import datetime
import telebot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ТУК_СЛОЖИ_ТОКЕНА_АКО_НЯМАШ_ENV")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "ТУК_СЛОЖИ_ЧАТ_ID")

bot = telebot.TeleBot(TOKEN)

URL = "https://www.goaloo.mobi/1x2OddsDrop/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def fetch_html():
    response = requests.get(URL, headers=HEADERS)
    return response.text

def parse_odds_drops(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'oddsTable'})
    matches = []
    
    if table:
        rows = table.find_all('tr')[1:]  # Пропускаме заглавния ред
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 7:
                time = cols[0].text.strip()
                league = cols[1].text.strip()
                teams = cols[2].text.strip()
                drop_type = cols[3].text.strip()
                odds_before = cols[4].text.strip()
                odds_after = cols[5].text.strip()
                drop_pct = cols[6].text.strip()
                
                try:
                    pct = float(drop_pct.replace('%',''))
                except:
                    pct = 0
                
                if pct >= 11:
                    matches.append({
                        'time': time,
                        'league': league,
                        'teams': teams,
                        'drop_type': drop_type,
                        'odds_before': odds_before,
                        'odds_after': odds_after,
                        'drop_pct': pct
                    })
    return matches

def send_signals(signals):
    for match in signals:
        msg = f"\u2728 *Ново движение на коефициент!* \u2728\n"
        msg += f"\ud83c\udf10 Лига: {match['league']}\n"
        msg += f"\ud83c\udfc0 Мач: {match['teams']}\n"
        msg += f"\u23f0 Време: {match['time']}\n"
        msg += f"\u2193 Тип: {match['drop_type']}\n"
        msg += f"\ud83d\udd22 Спад: {match['odds_before']} -> {match['odds_after']} ({match['drop_pct']}%)"

        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')

def main():
    html = fetch_html()
    signals = parse_odds_drops(html)
    if signals:
        send_signals(signals)
    else:
        print("\n[INFO] Няма нови сигнали към " + datetime.datetime.now().strftime('%H:%M:%S'))

if __name__ == "__main__":
    main()
