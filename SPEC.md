# IT Live Register Bot — Spetsifikatsiya (v1)

> Holat: qoralama. ❓ belgisi bor joylar tasdiqlanishi kerak (oxiridagi "Ochiq savollar" bo'limiga qarang).

---

## 1. Muammo va maqsad
Kurslarga qiziqqanlarning arizalari tarqoq keladi, yo'qoladi va menejer ular bilan qanday ishlaganini kuzatib bo'lmaydi. Bot arizani to'g'ri formatda yig'adi, uni **1 daqiqa ichida** menejerga yetkazadi. Maqsad: **arizalarning 95% i 24 soat ichida "Yangi" statusidan chiqishi**. Bu `/stats` dagi "o'rtacha qabul qilish vaqti" va "Yangi" soni orqali o'lchanadi.

## 2. Rollar
| Rol | Kim | Nima qila oladi |
|---|---|---|
| Foydalanuvchi | Istalgan Telegram foydalanuvchisi | Ariza qoldiradi (1 marta), aloqa ma'lumotlari va lokatsiyani ko'radi |
| Menejer | `MANAGER_IDS` dagi foydalanuvchilar | Arizalarni shaxsiy chatida oladi (navbat bilan), "Qabul qildim" va natija statuslarini bosadi (faqat o'ziga biriktirilgan arizalarda) |
| Admin | `ADMIN_IDS` dagi foydalanuvchilar | Har arizaning nusxasini `ADMIN_CHAT_ID` ga oladi, istalgan arizaning statusini o'zgartiradi, `/stats` va `/export` buyruqlaridan foydalanadi |

Bir odam ham admin, ham menejer bo'lishi mumkin.

## 3. Foydalanuvchi hikoyalari
1. **Qiziquvchi** sifatida tugmalar orqali bir daqiqada ariza qoldirmoqchiman, chunki uzun forma to'ldirishni xohlamayman.
2. **Qiziquvchi** sifatida raqamimni bitta tugma bilan yubormoqchiman, chunki uni qo'lda yozganda xato qilishim mumkin.
3. **Qiziquvchi** sifatida o'zimga qulay vaqtni tanlamoqchiman, chunki menga noqulay paytda qo'ng'iroq qilishlarini xohlamayman.
4. **Qiziquvchi** sifatida o'quv markazining telefoni va manzilini xaritada ko'rmoqchiman, chunki borib ko'rishni xohlayman.
5. **Qiziquvchi** sifatida xato kiritsam darhol bilmoqchiman, chunki keyin "raqamingiz noto'g'ri ekan" degan holat bo'lmasin.
6. **Menejer** sifatida yangi arizani darhol shaxsiy chatimda olmoqchiman, chunki mijoz sovib qolmasdan qo'ng'iroq qilishim kerak.
7. **Menejer** sifatida arizani bitta tugma bilan "qabul qildim" deb belgilamoqchiman, chunki admin kim ishlayotganini ko'rsin.
8. **Menejer** sifatida gaplashgandan keyin natijani (Gaplashildi / Qayta aloqa / Ma'lumot berildi / Bog'lanib bo'lmadi) belgilamoqchiman, chunki keyin kimga qayta qo'ng'iroq qilishni bilishim kerak.
9. **Admin** sifatida `/stats` orqali kurslar va statuslar kesimidagi raqamlarni ko'rmoqchiman, chunki reklama va menejer samaradorligini baholashim kerak.
10. **Admin** sifatida barcha arizalarni Excel'da ochiladigan faylga yuklab olmoqchiman, chunki hisobot va zaxira kerak.

## 4. Funksiyalar

### MVP (1-kun)
1. `/start` va bosh menyu: **📝 Kursga yozilish**, **📍 Aloqa va manzil** (manzil, telefon va xaritadagi lokatsiya).
2. Ariza formasi: 5 qadam + tasdiqlash. Har qadamda darhol tekshiruv va "Bekor qilish".
3. Takrorni bloklash: bitta Telegram akkaunt va bitta telefon raqam faqat 1 marta ariza qoldira oladi.
4. Arizani menejerga navbat bilan (round-robin) shaxsiy chatga yuborish va nusxasini `ADMIN_CHAT_ID` ga yuborish.
5. Status tugmalari: **Qabul qildim** → 4 ta natija statusi. Status bosilganda menejer va admindagi ikkala xabar ham yangilanadi, foydalanuvchiga esa qisqa status xabari boradi ("Zo'r ishlash" standarti, 13-band).
6. `/stats` va `/export` (CSV) — faqat admin uchun.

### KEYINGI (keyin qo'shiladi)
- Menejer izohi ("ertaga 15:00 da qo'ng'iroq")
- "Qayta aloqa" uchun sana/vaqt va eslatma
- Boshqa kursga qo'shimcha ariza qoldirish imkoni
- Kurslar ro'yxatini admin bot ichidan boshqarishi
- "📚 Kurslar haqida" bo'limi (narx, davomiylik)
- "Biz haqimizda qayerdan eshitdingiz" (reklama manbasi)
- Rus tili
- Menejerga kunlik hisobot, Google Sheets bilan sinxronlash
- Telefon raqam bo'yicha qidiruv (`/find`)

## 5. Ekranlar

**E1 — Bosh menyu** (`/start`, "Bekor qilish", ariza tugagandan keyin)
- Matn: T1 (11-bo'lim)
- Reply tugmalar: `📝 Kursga yozilish` → E3 yoki E2 | `📍 Aloqa va manzil` → E4
- Adminlarga qo'shimcha tugmalar: `📊 Statistika` → `/stats` | `📤 Eksport` → `/export`

**E2 — Avval ariza qoldirgan** (akkaunt bo'yicha takror)
- Matn: T3. Tugmalar: bosh menyu tugmalari.

**E3 — Ariza formasi** (6-bo'limdagi FSM; har ekranda `❌ Bekor qilish` → T10 → E1)
| Qadam | Matn | Tugmalar |
|---|---|---|
| 1/5 Ism | T4 | `❌ Bekor qilish` |
| 2/5 Telefon | T5 | `📱 Raqamni yuborish` (request_contact), `❌ Bekor qilish` |
| 3/5 Kurs | T6 | `🤖 Sun'iy intellekt`, `💻 Frontend`, `⚙️ Backend`, `🛡 Kiberxavfsizlik`, `🖥 Kompyuter savodxonligi`, `❌ Bekor qilish` |
| 4/5 Format | T7 | `🌐 Online`, `🏫 Offline`, `❌ Bekor qilish` |
| 5/5 Vaqt | T8 | `🌅 Ertalab (9:00–12:00)`, `☀️ Kunduzi (12:00–17:00)`, `🌙 Kechqurun (17:00–20:00)`, `❌ Bekor qilish` ❓ |
| Tasdiqlash | T9 (ma'lumotlar xulosasi) | `✅ Tasdiqlash` → saqlash → T11 → E1 · `✏️ Qayta to'ldirish` → 1/5 · `❌ Bekor qilish` → E1 |

**E4 — Aloqa**: T2 matni (telefon, manzil, mo'ljal, ish vaqti) va undan keyin Telegram lokatsiyasi (`send_venue`: koordinata, nom, manzil). Tugmalar: bosh menyu.

**E5 — Menejer/admin kartasi** (shaxsiy chatda va `ADMIN_CHAT_ID` da)
- Matn: T12.
- Inline tugmalar:
  - Status "Yangi" bo'lsa: `✅ Qabul qildim` → status "Qabul qilindi", menejer va vaqt yoziladi, natija tugmalari chiqadi.
  - Qabul qilingandan keyin: `🗣 Gaplashildi`, `🔁 Qayta aloqa`, `ℹ️ Ma'lumot berildi`, `📵 Bog'lanib bo'lmadi`. Bosilganda status almashadi va joriy statusning oldiga `•` qo'yiladi. Tugmalar o'chmaydi, ya'ni natijani keyin ham o'zgartirsa bo'ladi ❓. "Yangi" statusiga qaytarib bo'lmaydi.
- Tugma bosilganda bot qisqa bildirishnoma ko'rsatadi: "Status: Gaplashildi ✅".

**E6 — `/stats`** — T13. **E7 — `/export`** — CSV fayl + T14.

## 6. Dialog oqimlari (FSM)
`ApplyForm` holatlari. Har qadamda `❌ Bekor qilish` yoki `/start` bosilsa → holat tozalanadi → E1.

| Holat | Kutilgan kiritish | Tekshiruv (8-bo'lim) | Xato bo'lsa | Keyingi holat |
|---|---|---|---|---|
| (kirish) | `📝 Kursga yozilish` | Bu `tg_id` bilan ariza yo'qmi? | E2 ko'rsatiladi, FSM boshlanmaydi | `name` |
| `name` | Matn | V1 | Xato matni, holat o'zgarmaydi | `phone` |
| `phone` | Kontakt yoki matn | V2 + V3 + takror telefon | Xato matni yoki T15 (takror) | `course` |
| `course` | Tugma matni | V4 | "Tugmalardan birini tanlang" | `format` |
| `format` | Tugma matni | V5 | Shu | `time` |
| `time` | Tugma matni | V6 | Shu | `confirm` |
| `confirm` | 3 tugmadan biri | V7 | Shu | Saqlash → E1 / `name` / E1 |

Saqlash bosqichi: `tg_id` va `phone` yana bir bor tekshiriladi (bazadagi UNIQUE cheklov). Keyin: INSERT → menejer tanlanadi → menejerga yuboriladi → adminga nusxa yuboriladi → `msg_id` lar saqlanadi.

Foydalanuvchi har qanday holatda matn o'rniga stiker, rasm yoki ovozli xabar yuborsa: "Iltimos, matn yozing yoki tugmani bosing" deb javob beriladi, holat o'zgarmaydi.

## 7. Ma'lumotlar modeli (SQLite)

**`leads`**
| Maydon | Turi | Majburiy | Cheklov |
|---|---|---|---|
| id | INTEGER | ha | PRIMARY KEY AUTOINCREMENT |
| tg_id | INTEGER | ha | UNIQUE |
| tg_username | TEXT | yo'q | — |
| name | TEXT | ha | 2–40 belgi |
| phone | TEXT | ha | UNIQUE, `+998XXXXXXXXX` |
| phone_source | TEXT | ha | CHECK IN ('contact','typed') |
| course | TEXT | ha | CHECK IN ('ai','frontend','backend','cyber','computer_literacy') |
| study_format | TEXT | ha | CHECK IN ('online','offline') |
| pref_time | TEXT | ha | CHECK IN ('morning','day','evening') |
| status | TEXT | ha | DEFAULT 'new'; CHECK IN ('new','accepted','talked','callback','informed','unreachable') |
| manager_id | INTEGER | yo'q | NULL = menejerga yetkazilmadi |
| manager_msg_id | INTEGER | yo'q | — |
| admin_msg_id | INTEGER | yo'q | — |
| created_at | TEXT | ha | UTC, ISO-8601 |
| accepted_at | TEXT | yo'q | UTC, ISO-8601 |
| updated_at | TEXT | ha | UTC, ISO-8601 |

**`status_history`** — id INTEGER PK · lead_id INTEGER NOT NULL (FK → leads.id) · old_status TEXT · new_status TEXT NOT NULL · changed_by INTEGER NOT NULL · changed_at TEXT NOT NULL

**`settings`** — key TEXT PK · value TEXT NOT NULL (`rr_index`, ya'ni round-robin ko'rsatkichi)

Indeks: `leads(status)`, `leads(created_at)`. Vaqt bazada UTC'da saqlanadi va Toshkent vaqtida (UTC+5, qat'iy offset) ko'rsatiladi.

## 8. Tekshiruv qoidalari
- **V1 Ism:** bo'shliqlar qisqartiriladi; uzunligi 2–40 belgi. Faqat harflar (lotin/kirill, oʻ gʻ), bo'sh joy, `-`, `'`, `ʻ`, `ʼ` ruxsat etiladi. Kamida 2 ta harf bo'lishi shart. Raqam, emoji, `@` va havola rad etiladi. Menyu tugmasining matni (masalan, "📝 Kursga yozilish") ism sifatida qabul qilinmaydi.
- **V2 Telefon (matn):** bo'sh joy, `-`, `(`, `)` olib tashlanadi. `998…` bo'lsa boshiga `+` qo'shiladi, 9 xonali bo'lsa `+998` qo'shiladi. Natija `^\+998(20|33|50|55|77|88|90|91|93|94|95|97|98|99)\d{7}$` ga mos kelishi kerak. Operator kodlari ro'yxati config'da turadi.
- **V3 Telefon (kontakt):** `contact.user_id == from_user.id` bo'lishi shart, ya'ni faqat o'z raqamini yuborish mumkin. Undan keyin V2 normalizatsiyasi qo'llanadi. O'zbekiston raqami bo'lmasa rad etiladi.
- **Takror:** normallashtirilgan telefon `leads.phone` da bo'lsa T15 chiqariladi va ariza to'xtatiladi.
- **V4/V5/V6:** matn tugma yozuvlaridan biriga aniq teng bo'lishi kerak.
- **V7:** faqat `✅ Tasdiqlash` / `✏️ Qayta to'ldirish` / `❌ Bekor qilish` qabul qilinadi.
- **Callback:** bosgan odam ADMIN_IDS ichida yoki shu arizaning `manager_id` si bo'lishi kerak. Aks holda "Sizda ruxsat yo'q" bildirishnomasi chiqadi.

## 9. Admin funksiyalari
- **Bildirishnoma:** yangi ariza menejerga (E5) va `ADMIN_CHAT_ID` ga nusxa sifatida yuboriladi. Menejerga yuborib bo'lmasa, navbatdagi menejerga yuboriladi. Hech kimga yetkazilmasa, admin nusxasiga "⚠️ Menejerga yetkazilmadi" yozuvi qo'shiladi va admin arizani o'zi qabul qila oladi.
- **Status tugmalari:** E5. "Qabul qildim" so'rovi `UPDATE … WHERE status='new'` ko'rinishida bajariladi. Shuning uchun ikki kishi bir vaqtda bossa ham faqat biriniki o'tadi, ikkinchisi "Allaqachon qabul qilingan" xabarini oladi. Har o'zgarish `status_history` ga yoziladi va ikkala karta ham tahrirlanadi.
- **`/stats`:** bugun / 7 kun / jami arizalar soni; status, kurs va format bo'yicha taqsimot; o'rtacha qabul qilish vaqti (`accepted_at - created_at`).
- **`/export`:** barcha arizalar CSV faylda (UTF-8 BOM, `;` ajratgich, Excel to'g'ri ochadi). Fayl nomi `itlive_arizalar_YYYY-MM-DD.csv`. Ustunlar: ID, Sana, Ism, Telefon, Kurs, Format, Qulay vaqt, Status, Menejer ID, Qabul vaqti, Username.

## 10. Chegaraviy holatlar
1. **Tugma o'rniga matn yozilsa** (kurs/format/vaqt qadamida) → "Tugmalardan birini tanlang" deb, klaviatura qayta ko'rsatiladi.
2. **Begona kontakt yuborilsa** → "Faqat o'zingizning raqamingizni yuboring".
3. **Chet el yoki noto'g'ri raqam kiritilsa** → T16 namunasi bilan qayta so'raladi.
4. **Bir akkaunt qayta ariza qoldirmoqchi bo'lsa** → forma boshlanmaydi, E2 chiqadi.
5. **Boshqa akkauntdan, lekin avvalgi telefon bilan** → telefon qadamida T15 chiqadi, holat tozalanadi.
6. **"Tasdiqlash" ikki marta tez bosilsa** → UNIQUE(tg_id) tufayli bitta yozuv qoladi, ikkinchi bosish E2 ni ko'rsatadi.
7. **Forma o'rtasida bot qayta ishga tushsa** (FSM xotirada edi) → foydalanuvchi keyingi xabarini holatsiz yuboradi → "Iltimos, qaytadan boshlang" va E1.
8. **Menejer botni bloklagan yoki hech `/start` bosmagan bo'lsa** → `TelegramForbiddenError` ushlanadi, ariza keyingi menejerga yoki adminga o'tadi (9-bo'lim). Bot ishga tushganda menejerlarga yetib borish mumkinligi tekshiriladi va natija adminga yoziladi.
9. **Baza bo'sh bo'lsa** → `/stats` va `/export` "Hali arizalar yo'q" deb javob beradi, fayl yuborilmaydi.
10. **Admin bo'lmagan odam `/stats` yoki `/export` yozsa** → "⛔ Sizda ruxsat yo'q." ("Zo'r ishlash" standarti, 12-band).
11. **Begona odam callback bossa** (masalan, forward qilingan karta orqali) → "Sizda ruxsat yo'q".
12. **Eski kartadagi tugma bosilsa** (status allaqachon o'zgargan) → bazadagi joriy holat bo'yicha karta qayta chiziladi va "Status allaqachon yangilangan" bildirishnomasi chiqadi.
13. **Bot guruhga qo'shilsa** → `ADMIN_CHAT_ID` dan boshqa guruhlardagi xabarlar e'tiborsiz qoldiriladi.
14. **Stiker, rasm yoki ovozli xabar** → 6-bo'limdagi umumiy javob.
15. **Ismning o'rniga menyu tugmasi bosilsa** → V1 orqali rad etiladi.

## 11. Bot matnlari
- **T1:** "Assalomu alaykum, {first_name}! 👋\nIT Live o'quv markazining botiga xush kelibsiz.\nKursga yozilish uchun ariza qoldiring — menejerimiz siz bilan bog'lanadi."
- **T2:** "📍 IT Live\n📞 Telefon: {PHONE}\n🏢 Manzil: {ADDRESS}\n🧭 Mo'ljal: {LANDMARK}\n🕐 Ish vaqti: {HOURS}" ❓
- **T3:** "✅ Siz avval ariza qoldirgansiz (#{id}, {sana}).\nMenejerimiz siz bilan bog'lanadi. Savollar bo'lsa — 📍 Aloqa."
- **T4:** "1/5. Ism va familiyangizni yozing:\nMasalan: Aziz Karimov"
- **T5:** "2/5. Telefon raqamingizni yuboring 👇\nTugmani bosing yoki yozing: +998901234567"
- **T6:** "3/5. Qaysi kursga yozilmoqchisiz?"
- **T7:** "4/5. O'qish formatini tanlang:"
- **T8:** "5/5. Sizga qaysi vaqtda qo'ng'iroq qilish qulay?"
- **T9:** "Ma'lumotlaringizni tekshiring:\n👤 {name}\n📞 {phone}\n📚 {course}\n🏫 {format}\n🕐 {time}\n\nHammasi to'g'rimi?"
- **T10:** "Ariza bekor qilindi."
- **T11:** "🎉 Arizangiz qabul qilindi! (#{id})\nMenejerimiz siz tanlagan vaqtda ({time}) bog'lanadi."
- **T12 (karta):** "🆕 Ariza #{id}\n👤 {name}\n📞 {phone} {📱|✍️}\n📚 {course}\n🏫 {format}\n🕐 {time}\n💬 {@username yoki profil havolasi}\n📅 {sana}\n\nStatus: {status_emoji} {status} {— menejer, vaqt}"
- **T13:** "📊 Statistika\nBugun: {a} · 7 kun: {b} · Jami: {c}\n\nStatus bo'yicha:\n…\nKurs bo'yicha:\n…\nOnline: {x} · Offline: {y}\n⏱ O'rtacha qabul qilish vaqti: {m} daq"
- **T14:** "📤 Jami {n} ta ariza."
- **T15:** "⚠️ Bu telefon raqami bilan avval ro'yxatdan o'tilgan. Savollar bo'lsa — 📍 Aloqa."
- **Xatolar:**
  - Ism: "❗ Ism faqat harflardan iborat bo'lsin (2–40 belgi). Masalan: Aziz Karimov"
  - **T16** (telefon): "❗ Raqam noto'g'ri. Namuna: +998901234567"
  - Kontakt: "❗ Faqat o'zingizning raqamingizni yuboring."
  - Tugma: "❗ Iltimos, pastdagi tugmalardan birini tanlang."
  - Media: "❗ Iltimos, matn yozing yoki tugmani bosing."
  - Ruxsat: "⛔ Sizda ruxsat yo'q."
  - Bo'sh baza: "Hali arizalar yo'q."

## 12. Muhit o'zgaruvchilari
| Nom | Misol | Izoh |
|---|---|---|
| BOT_TOKEN | — | Faqat `.env` va Railway Variables'da |
| ADMIN_IDS | `11111,22222` | Vergul bilan ajratiladi |
| ADMIN_CHAT_ID | `11111` yoki `-100…` | Adminlarga nusxa boradigan chat (shaxsiy chat yoki guruh) |
| MANAGER_IDS | `33333` | Navbat bilan taqsimlanadi. Hozircha 1 kishi |
| DB_PATH | `data/bot.db` | Railway'da: `/app/data/bot.db` (Volume) |

Aloqa ma'lumotlari (telefon, manzil, koordinatalar) sir emas, shuning uchun `app/texts.py` va `app/config.py` da turadi.

## 13. Qabul testlari (Telegram'da qo'lda)
1. `/start` → T1 va 2 ta tugma chiqadi (admin uchun 4 ta).
2. `📍 Aloqa va manzil` → matn va xaritadagi lokatsiya keladi.
3. `📝 Kursga yozilish` → ism uchun `A1` yozing → xato chiqadi, holat o'sha qadamda qoladi.
4. To'g'ri ism → telefon qadamiga `12345` yozing → T16 chiqadi.
5. `📱 Raqamni yuborish` tugmasini bosing → kurs tugmalari chiqadi.
6. Kurs qadamida "python" deb yozing → "tugmalardan birini tanlang" chiqadi.
7. Kurs, format va vaqtni tanlang → T9 xulosasi to'g'ri chiqadi.
8. `✏️ Qayta to'ldirish` → 1/5 qadamga qaytadi.
9. Oxirigacha to'ldirib `✅ Tasdiqlash` bosing → T11 chiqadi, menejer va admin chatiga karta keladi.
10. Menejer `✅ Qabul qildim` bosadi → ikkala kartada status "Qabul qilindi" bo'ladi va 4 ta natija tugmasi chiqadi.
11. Menejer `🔁 Qayta aloqa`ni, keyin `🗣 Gaplashildi`ni bosadi → ikkala kartada ham status yangilanadi.
12. O'sha akkauntdan yana `📝 Kursga yozilish` bosing → T3 chiqadi.
13. Boshqa akkauntdan o'sha raqamni yozib ko'ring → T15 chiqadi.
14. Admin bo'lmagan akkauntdan `/stats` yozing → "⛔ Sizda ruxsat yo'q." chiqadi.
15. Admin `/stats` va `/export` yuboradi → raqamlar to'g'ri, CSV Excel'da o'zbekcha harflar bilan to'g'ri ochiladi.

---

## Ochiq savollar ❓
1. **Aloqa ma'lumotlari:** telefon, manzil, mo'ljal, ish vaqti va lokatsiya (koordinata yoki Google/Yandex havola).
2. **Qulay vaqt oraliqlari:** Ertalab 9–12 / Kunduzi 12–17 / Kechqurun 17–20 to'g'rimi?
3. **Natija statusini keyin o'zgartirish** (masalan, Qayta aloqa → Gaplashildi) mumkin bo'lsinmi? Reja hozir "ha" deb yozilgan.
4. **ADMIN_CHAT_ID** — adminning shaxsiy chatimi yoki alohida guruhmi?

## 3 ta eng katta xavf
1. **Railway'da redeploy paytida SQLite fayli o'chib ketadi.** Railway konteyner diski vaqtinchalik.
   → Railway **Volume** ulanadi va `/app/data` ga mount qilinadi, `DB_PATH=/app/data/bot.db`. Birinchi deploy'dan keyin test ariza qoldirib, redeploy qilib, ariza saqlanib qolganini tekshirish kerak. Zaxira sifatida admin haftasiga bir marta `/export` qiladi.
2. **Arizalar bitta menejerga bog'liq.** Menejer botni `/start` qilmagan, bloklagan yoki ta'tilda bo'lsa, arizalar yo'qoladi.
   → Har ariza adminga ham nusxa sifatida boradi. Yetkazib bo'lmasa adminga ogohlantirish chiqadi. Bot ishga tushganda menejerlarga yetib borish tekshiriladi. "Yangi" statusidagi arizalar `/stats` da ko'rinib turadi.
3. **Ikkita bot nusxasi bir vaqtda polling qiladi** (lokal kompyuter va Railway). Natijada `TelegramConflictError` chiqadi, xabarlar ikki nusxa orasida bo'linib ketadi va arizalar ikki xil bazaga yoziladi.
   → Lokal sinov uchun **alohida test bot tokeni** ishlatiladi (BotFather'da yangi bot). Prod tokeni faqat Railway'da turadi.
