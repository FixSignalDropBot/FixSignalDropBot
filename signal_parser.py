from bs4 import BeautifulSoup

def parse_signal(text):
    # Тук добави логиката за разпознаване на сигнал от входния текст
    if "Over 2.5 goals" in text:
        return "📊 Прогноза: Над 2.5 гола ✅"
    elif "Under 2.5 goals" in text:
        return "📊 Прогноза: Под 2.5 гола 🔻"
    elif "Draw" in text:
        return "🤝 Прогноза: Равенство ⚖️"
    elif "1" in text or "Home win" in text:
        return "🏠 Победа за домакина ✅"
    elif "2" in text or "Away win" in text:
        return "🚀 Победа за госта ✅"
    else:
        return "❗ Не мога да разбера сигнала. Моля, провери формата на съобщението."
