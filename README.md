# IT Live Register Bot

Kurslarga yozilmoqchi bo'lganlardan ariza yig'adigan Telegram bot. Ariza navbat bilan sotuv menejeriga
(shaxsiy chatiga) va nusxasi admin chatiga boradi; menejer tugmalar bilan statusni belgilaydi.

To'liq reja: [SPEC.md](SPEC.md).

## Imkoniyatlar
- **Foydalanuvchi:** `📝 Kursga yozilish` (ism → telefon → kurs → format → qulay vaqt → tasdiqlash),
  `📍 Aloqa va manzil`. Har qadamda tekshiruv va `❌ Bekor qilish`. Bitta akkaunt va bitta raqam — bitta ariza.
- **Menejer:** arizani shaxsiy chatida oladi → `✅ Qabul qildim` → `🗣 Gaplashildi` / `🔁 Qayta aloqa` /
  `ℹ️ Ma'lumot berildi` / `📵 Bog'lanib bo'lmadi`. Status o'zgarsa, foydalanuvchiga xabar boradi.
- **Admin:** har arizaning nusxasi, istalgan arizaning statusini o'zgartirish, `/stats`, `/export` (CSV).

## Sozlamalar (`.env`)
| O'zgaruvchi | Izoh |
|---|---|
| `BOT_TOKEN` | @BotFather bergan token |
| `ADMIN_IDS` | Adminlar Telegram ID lari, vergul bilan: `11111,22222` |
| `ADMIN_CHAT_ID` | Ariza nusxasi boradigan chat: admin ID si yoki guruh ID si (`-100...`) |
| `MANAGER_IDS` | Sotuv menejerlari ID lari, vergul bilan (navbat bilan taqsimlanadi) |
| `DB_PATH` | SQLite fayl yo'li, standart `data/bot.db` |

- O'z ID ingizni bilish: Telegram'da @userinfobot ga yozing.
- **Har bir menejer botga kamida bir marta `/start` bosishi shart** — aks holda Telegram bot unga yoza olmaydi.
  Bot ishga tushganda buni tekshiradi va yetib bo'lmaydigan menejerlar haqida admin chatiga yozadi.
- `ADMIN_CHAT_ID` guruh bo'lsa: botni guruhga qo'shing, guruh ID sini (`-100...`) yozing.
- Aloqa ma'lumotlari (telefon, manzil, mo'ljal, ish vaqti, koordinatalar) — `app/config.py` dagi `CONTACT_*`.
- Barcha matnlar — `app/texts.py`.

## Lokal ishga tushirish (Windows, PowerShell)
Kompyuterda **alohida test bot** tokenini ishlating. Bitta token bilan ikki joyda (lokal + Railway)
bir vaqtda ishga tushirilsa, Telegram `Conflict` xatosini beradi va arizalar ikki bazaga bo'linib ketadi.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` ni to'ldiring, keyin:

```powershell
.\.venv\Scripts\python.exe main.py
```

Log'da `Run polling for bot @...` chiqsa — bot ishlayapti. To'xtatish: `Ctrl+C`.
Baza (`data/bot.db`) birinchi ishga tushganda o'zi yaratiladi.

## Railway'ga deploy
1. **GitHub'ga yuklash.** `.env`, `.venv/`, `data/` `.gitignore` da — ular yuklanmaydi. Yuklashdan oldin
   `git status` da `.env` ko'rinmasligiga ishonch hosil qiling.
2. Railway → **New Project → Deploy from GitHub repo** → shu repozitoriyni tanlang.
   Python versiyasi `.python-version` dan (3.12), ishga tushirish buyrug'i `railway.toml` dan olinadi.
3. Servis → **Variables**: `BOT_TOKEN` (prod bot), `ADMIN_IDS`, `ADMIN_CHAT_ID`, `MANAGER_IDS`,
   `DB_PATH=/app/data/bot.db`.
4. **Volume (majburiy!)** — servis ustida o'ng tugma → **Attach Volume** → Mount path: `/app/data`.
   Volume bo'lmasa, har deploy'da baza o'chib ketadi.
5. Deploy tugagach **Deployments → Logs** da `Run polling for bot` qatorini tekshiring.
6. **Volume tekshiruvi:** bitta test ariza qoldiring → **Redeploy** → `/stats` da ariza saqlanib qolganini ko'ring.
7. Servis replikalari soni **1** bo'lsin (polling bitta nusxada ishlashi kerak).

Zaxira: haftada bir marta `/export` qilib, CSV faylni saqlab qo'ying.

## Tuzilma
```
main.py               ishga tushirish, middleware, routerlar
app/config.py         .env sozlamalari, vaqt zonasi, aloqa ma'lumotlari
app/db.py             SQLite (leads, status_history, settings)
app/texts.py          barcha matnlar va tugma yozuvlari
app/keyboards.py      reply va inline tugmalar
app/states.py         ariza formasi holatlari (FSM)
app/validators.py     ism va telefon tekshiruvi
app/notify.py         ariza kartasi, menejerga yuborish, status xabarlari
app/handlers/         common, apply, contact, manager, admin, fallback, errors
```
