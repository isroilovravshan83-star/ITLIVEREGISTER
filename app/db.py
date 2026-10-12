import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import aiosqlite

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id           INTEGER NOT NULL UNIQUE,
    tg_username     TEXT,
    name            TEXT    NOT NULL CHECK (length(name) BETWEEN 2 AND 40),
    phone           TEXT    NOT NULL UNIQUE,
    phone_source    TEXT    NOT NULL CHECK (phone_source IN ('contact', 'typed')),
    course          TEXT    NOT NULL CHECK (course IN ('ai', 'frontend', 'backend', 'cyber', 'computer_literacy')),
    study_format    TEXT    NOT NULL CHECK (study_format IN ('online', 'offline')),
    pref_time       TEXT    NOT NULL CHECK (pref_time IN ('morning', 'day', 'evening')),
    status          TEXT    NOT NULL DEFAULT 'new'
                    CHECK (status IN ('new', 'accepted', 'talked', 'callback', 'informed', 'unreachable')),
    manager_id      INTEGER,
    manager_msg_id  INTEGER,
    admin_msg_id    INTEGER,
    created_at      TEXT    NOT NULL,
    accepted_at     TEXT,
    updated_at      TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

CREATE TABLE IF NOT EXISTS status_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id     INTEGER NOT NULL REFERENCES leads(id),
    old_status  TEXT,
    new_status  TEXT    NOT NULL,
    changed_by  INTEGER NOT NULL,
    changed_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key    TEXT PRIMARY KEY,
    value  TEXT NOT NULL
);
"""


class DuplicateLeadError(Exception):
    """Bu Telegram akkaunt yoki telefon bilan ariza allaqachon bor."""


@dataclass(frozen=True)
class Lead:
    id: int
    tg_id: int
    tg_username: str | None
    name: str
    phone: str
    phone_source: str
    course: str
    study_format: str
    pref_time: str
    status: str
    manager_id: int | None
    manager_msg_id: int | None
    admin_msg_id: int | None
    created_at: datetime
    accepted_at: datetime | None
    updated_at: datetime


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _row_to_lead(row: aiosqlite.Row) -> Lead:
    data = dict(row)
    for key in ("created_at", "accepted_at", "updated_at"):
        if data[key] is not None:
            data[key] = datetime.fromisoformat(data[key])
    return Lead(**data)


class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    def _connect(self) -> aiosqlite.Connection:
        return aiosqlite.connect(self.path)

    async def init(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        async with self._connect() as conn:
            await conn.executescript(SCHEMA)
            await conn.commit()

    async def get_lead_by_tg(self, tg_id: int) -> Lead | None:
        async with self._connect() as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute("SELECT * FROM leads WHERE tg_id = ?", (tg_id,)) as cur:
                row = await cur.fetchone()
        return _row_to_lead(row) if row else None

    async def phone_exists(self, phone: str) -> bool:
        async with self._connect() as conn:
            async with conn.execute("SELECT 1 FROM leads WHERE phone = ?", (phone,)) as cur:
                return await cur.fetchone() is not None

    async def create_lead(
        self,
        *,
        tg_id: int,
        tg_username: str | None,
        name: str,
        phone: str,
        phone_source: str,
        course: str,
        study_format: str,
        pref_time: str,
    ) -> int:
        now = utc_now()
        try:
            async with self._connect() as conn:
                cur = await conn.execute(
                    """
                    INSERT INTO leads (tg_id, tg_username, name, phone, phone_source, course,
                                       study_format, pref_time, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (tg_id, tg_username, name, phone, phone_source, course,
                     study_format, pref_time, now, now),
                )
                await conn.commit()
                return cur.lastrowid
        except sqlite3.IntegrityError as exc:
            if "UNIQUE" in str(exc):
                raise DuplicateLeadError from exc
            raise

    async def get_lead(self, lead_id: int) -> Lead | None:
        async with self._connect() as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)) as cur:
                row = await cur.fetchone()
        return _row_to_lead(row) if row else None

    async def all_leads(self) -> list[Lead]:
        async with self._connect() as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute("SELECT * FROM leads ORDER BY id") as cur:
                rows = await cur.fetchall()
        return [_row_to_lead(row) for row in rows]

    async def get_rr_index(self) -> int:
        async with self._connect() as conn:
            async with conn.execute("SELECT value FROM settings WHERE key = 'rr_index'") as cur:
                row = await cur.fetchone()
        return int(row[0]) if row else 0

    async def set_delivery(
        self,
        lead_id: int,
        *,
        manager_id: int | None,
        manager_msg_id: int | None,
        admin_msg_id: int | None,
        rr_index: int | None,
    ) -> None:
        async with self._connect() as conn:
            await conn.execute(
                "UPDATE leads SET manager_id = ?, manager_msg_id = ?, admin_msg_id = ? WHERE id = ?",
                (manager_id, manager_msg_id, admin_msg_id, lead_id),
            )
            if rr_index is not None:
                await conn.execute(
                    "INSERT INTO settings (key, value) VALUES ('rr_index', ?) "
                    "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                    (str(rr_index),),
                )
            await conn.commit()

    async def change_status(self, lead_id: int, old: str, new: str, changed_by: int) -> bool:
        """Statusni faqat u hali `old` bo'lsa o'zgartiradi (ikki kishi bir vaqtda bossa — biriniki o'tadi)."""
        now = utc_now()
        async with self._connect() as conn:
            if old == "new":
                # Qabul qilish: vaqt yoziladi; menejerga yetkazilmagan bo'lsa, qabul qilgan admin biriktiriladi.
                cur = await conn.execute(
                    "UPDATE leads SET status = ?, updated_at = ?, accepted_at = ?, "
                    "manager_id = COALESCE(manager_id, ?) WHERE id = ? AND status = ?",
                    (new, now, now, changed_by, lead_id, old),
                )
            else:
                cur = await conn.execute(
                    "UPDATE leads SET status = ?, updated_at = ? WHERE id = ? AND status = ?",
                    (new, now, lead_id, old),
                )
            if cur.rowcount == 0:
                return False
            await conn.execute(
                "INSERT INTO status_history (lead_id, old_status, new_status, changed_by, changed_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (lead_id, old, new, changed_by, now),
            )
            await conn.commit()
        return True

    async def stats(self, today_start: str, week_start: str) -> dict:
        async with self._connect() as conn:
            async def scalar(sql: str, params: tuple = ()):
                async with conn.execute(sql, params) as cur:
                    return (await cur.fetchone())[0]

            async def grouped(column: str) -> dict[str, int]:
                async with conn.execute(f"SELECT {column}, COUNT(*) FROM leads GROUP BY {column}") as cur:
                    return {key: count for key, count in await cur.fetchall()}

            return {
                "total": await scalar("SELECT COUNT(*) FROM leads"),
                "today": await scalar("SELECT COUNT(*) FROM leads WHERE created_at >= ?", (today_start,)),
                "week": await scalar("SELECT COUNT(*) FROM leads WHERE created_at >= ?", (week_start,)),
                "avg_accept_min": await scalar(
                    "SELECT AVG((julianday(accepted_at) - julianday(created_at)) * 1440) "
                    "FROM leads WHERE accepted_at IS NOT NULL"
                ),
                "status": await grouped("status"),
                "course": await grouped("course"),
                "study_format": await grouped("study_format"),
            }
