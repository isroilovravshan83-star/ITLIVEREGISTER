# Telegram bot loyihasi — AI agent uchun qoidalar

## Texnologiyalar (o'zgartirma)
- Python 3.12, aiogram 3 (eng so'nggi 3.x), aiosqlite, python-dotenv
- Ma'lumotlar bazasi: SQLite, yo'li DB_PATH muhit o'zgaruvchisidan (standart: data/bot.db)
- Deploy: Railway (GitHub orqali), polling rejimi

## Tuzilma
- main.py — ishga tushirish nuqtasi
- app/config.py — sozlamalar (.env dan)
- app/db.py — baza bilan ishlash
- app/texts.py — barcha matnlar
- app/keyboards.py — tugmalar
- app/states.py — FSM holatlari
- app/handlers/ — har funksiya alohida Router faylida

## Qat'iy qoidalar
1. BOT_TOKEN va boshqa sirlarni hech qachon kodga, chatga yoki log'ga chiqarma. Faqat .env.
2. .env, .venv, data/, *.db — .gitignore'da bo'lishi shart.
3. Fayl o'chirish yoki katta o'zgarishdan oldin nima qilishingni ayt va ruxsat so'ra.
4. Har bosqichdan keyin botni ishga tushir va menga Telegram'da nimani sinashni ayt.
5. Xato chiqsa — avval sababini tushuntir, keyin minimal tuzatish qil.
6. Javob va izohlar o'zbek tilida.
