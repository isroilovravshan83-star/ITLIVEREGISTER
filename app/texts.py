# Botdagi barcha matnlar shu yerda. Tugma yozuvlari handlerlarda ham shu konstantalar orqali tekshiriladi.

# --- Tugmalar ---
BTN_APPLY = "📝 Kursga yozilish"
BTN_CONTACT = "📍 Aloqa va manzil"
BTN_CANCEL = "❌ Bekor qilish"
BTN_SEND_PHONE = "📱 Raqamni yuborish"
BTN_CONFIRM = "✅ Tasdiqlash"
BTN_RESTART = "✏️ Qayta to'ldirish"
BTN_STATS = "📊 Statistika"
BTN_EXPORT = "📤 Eksport"
BTN_ACCEPT = "✅ Qabul qildim"

# Tanlov variantlari: bazadagi kod → tugma yozuvi
COURSES = {
    "ai": "🤖 Sun'iy intellekt",
    "frontend": "💻 Frontend",
    "backend": "⚙️ Backend",
    "cyber": "🛡 Kiberxavfsizlik",
    "computer_literacy": "🖥 Kompyuter savodxonligi",
}
FORMATS = {
    "online": "🌐 Online",
    "offline": "🏫 Offline",
}
PREF_TIMES = {
    "morning": "🌅 Ertalab (9:00–12:00)",
    "day": "☀️ Kunduzi (12:00–17:00)",
    "evening": "🌙 Kechqurun (17:00–20:00)",
}
STATUSES = {
    "new": "🆕 Yangi",
    "accepted": "🟡 Qabul qilindi",
    "talked": "🗣 Gaplashildi",
    "callback": "🔁 Qayta aloqa",
    "informed": "ℹ️ Ma'lumot berildi",
    "unreachable": "📵 Bog'lanib bo'lmadi",
}
# Menejer "Qabul qildim" dan keyin tanlaydigan natijalar
RESULT_STATUSES = ("talked", "callback", "informed", "unreachable")
PHONE_SOURCES = {"contact": "📱", "typed": "✍️"}

# --- Umumiy ---
START = (
    "Assalomu alaykum, {first_name}! 👋\n"
    "IT Live o'quv markazining botiga xush kelibsiz.\n"
    "Kursga yozilish uchun ariza qoldiring — menejerimiz siz bilan bog'lanadi."
)
HELP = (
    "ℹ️ <b>Yordam</b>\n\n"
    f"{BTN_APPLY} — kursga ariza qoldirish\n"
    f"{BTN_CONTACT} — telefon, manzil va lokatsiya\n\n"
    "/start — asosiy menyu\n"
    "/cancel — joriy amalni bekor qilish\n"
    "/help — shu yordam"
)
HELP_ADMIN = (
    "\n\n<b>Admin:</b>\n"
    "/stats — statistika\n"
    "/export — barcha arizalar (CSV)"
)
CANCELLED = "Ariza bekor qilindi."
NOTHING_TO_CANCEL = "Bekor qiladigan amal yo'q. Asosiy menyu 👇"
UNKNOWN = "🤔 Tushunmadim. Iltimos, pastdagi menyudan foydalaning."

# --- Ariza formasi ---
ALREADY_APPLIED = (
    "✅ Siz avval ariza qoldirgansiz (#{id}, {date}).\n"
    f"Menejerimiz siz bilan bog'lanadi. Savollar bo'lsa — {BTN_CONTACT}."
)
PHONE_TAKEN = f"⚠️ Bu telefon raqami bilan avval ro'yxatdan o'tilgan. Savollar bo'lsa — {BTN_CONTACT}."
ASK_NAME = "1/5. Ism va familiyangizni yozing:\nMasalan: <i>Aziz Karimov</i>"
ASK_PHONE = (
    "2/5. Telefon raqamingizni yuboring 👇\n"
    f"«{BTN_SEND_PHONE}» tugmasini bosing yoki yozing: <i>+998901234567</i>"
)
ASK_COURSE = "3/5. Qaysi kursga yozilmoqchisiz?"
ASK_FORMAT = "4/5. O'qish formatini tanlang:"
ASK_TIME = "5/5. Sizga qaysi vaqtda qo'ng'iroq qilish qulay?"
CONFIRM = (
    "Ma'lumotlaringizni tekshiring:\n\n"
    "👤 {name}\n"
    "📞 {phone}\n"
    "📚 {course}\n"
    "🏫 {study_format}\n"
    "🕐 {pref_time}\n\n"
    "Hammasi to'g'rimi?"
)
APPLIED = "🎉 Arizangiz qabul qilindi! (#{id})\nMenejerimiz siz tanlagan vaqtda ({pref_time}) bog'lanadi."

# --- Xatolar ---
ERR_NAME = "❗ Ism faqat harflardan iborat bo'lsin (2–40 belgi).\nMasalan: <i>Aziz Karimov</i>"
ERR_PHONE = "❗ Raqam noto'g'ri. O'zbekiston mobil raqamini yuboring.\nNamuna: <i>+998901234567</i>"
ERR_FOREIGN_CONTACT = "❗ Faqat o'zingizning raqamingizni yuboring."
ERR_BUTTON = "❗ Iltimos, pastdagi tugmalardan birini tanlang."
ERR_MEDIA = "❗ Iltimos, matn yozing yoki tugmani bosing."
NO_ACCESS = "⛔ Sizda ruxsat yo'q."

# --- Menejer/admin kartasi ---
CARD = (
    "📋 <b>Ariza #{id}</b>\n"
    "👤 {name}\n"
    "📞 {phone} {phone_source}\n"
    "📚 {course}\n"
    "🏫 {study_format}\n"
    "🕐 {pref_time}\n"
    "💬 {telegram}\n"
    "📅 {created}\n\n"
    "Status: <b>{status}</b>"
)
CARD_MANAGER = "\n👨‍💼 Menejer: {manager} · qabul: {accepted}"
CARD_NOT_DELIVERED = "\n⚠️ Menejerga yetkazilmadi — admin qabul qilishi kerak."
PROFILE_LINK = '<a href="tg://user?id={id}">profil</a>'

CB_ACCEPTED = "✅ Qabul qilindi"
CB_STATUS_SET = "✅ Status: {status}"
CB_ALREADY = "Status allaqachon yangilangan"
CB_NOT_FOUND = "Ariza topilmadi"

# --- Foydalanuvchiga status xabari ---
USER_STATUS = {
    "accepted": "👋 Arizangiz (#{id}) menejer tomonidan qabul qilindi. Tez orada bog'lanamiz.",
    "talked": f"✅ Suhbat uchun rahmat! Savollar bo'lsa — {BTN_CONTACT}.",
    "callback": "🔁 Menejerimiz siz bilan qayta bog'lanadi.",
    "informed": f"ℹ️ Kurs haqida ma'lumot berildi. Savollar bo'lsa — {BTN_CONTACT}.",
    "unreachable": f"📵 Sizga qo'ng'iroq qildik, lekin bog'lana olmadik. Iltimos, biz bilan bog'laning — {BTN_CONTACT}.",
}

# --- Admin ---
STATS = (
    "📊 <b>Statistika</b>\n"
    "Bugun: {today} · 7 kun: {week} · Jami: {total}\n\n"
    "<b>Status bo'yicha:</b>\n{by_status}\n\n"
    "<b>Kurs bo'yicha:</b>\n{by_course}\n\n"
    "<b>Format:</b>\n{by_format}\n\n"
    "⏱ O'rtacha qabul qilish vaqti: {avg_accept}"
)
STATS_NO_DATA = "—"
NO_LEADS = "Hali arizalar yo'q."
EXPORT_DONE = "📤 Jami {count} ta ariza."
EXPORT_HEADER = (
    "ID", "Sana", "Ism", "Telefon", "Kurs", "Format", "Qulay vaqt",
    "Status", "Menejer ID", "Qabul vaqti", "Username",
)
RECIPIENT_UNREACHABLE = (
    "⚠️ Bot quyidagi menejerlarga xabar yubora olmayapti: {ids}\n"
    "Ular botga /start bosishi kerak, aks holda arizalar ularga yetib bormaydi."
)

# --- Aloqa ---
CONTACT = (
    "📍 <b>IT Live</b>\n"
    "📞 Telefon: {phone}\n"
    "🏢 Manzil: {address}\n"
    "🧭 Mo'ljal: {landmark}\n"
    "🕐 Ish vaqti: {hours}"
)
VENUE_TITLE = "IT Live"

# --- Bot buyruqlari menyusi ---
CMD_START = "Asosiy menyu"
CMD_HELP = "Yordam"
CMD_CANCEL = "Bekor qilish"
