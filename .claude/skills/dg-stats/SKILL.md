---
name: dg-stats
description: Аналитика канала @dunningkrugereffect — подписчики (новые/ушедшие), статистика постов, тренды. Снимки для сравнения между вызовами.
---

# dg-stats

Снимок и аналитика Telegram-канала @dunningkrugereffect.

## Когда вызывать

- `/dg-stats` — полный снимок + отчёт
- «статистика канала», «аналитика dg», «сколько подписчиков»

## Константы

- **Chat ID**: 1101882372
- **Stats dir**: `projects/daning-kruger/.life/stats/`
- **Diff script**: `projects/daning-kruger/.claude/skills/dg-stats/scripts/diff_subscribers.py`

## Алгоритм

### 1. Сбор данных (параллельно)

Вызвать одновременно:
- `mcp__telegram-mcp__get_chat(chat_id="dunningkrugereffect")` → total подписчиков
- `mcp__telegram-mcp__get_participants(chat_id="dunningkrugereffect")` → список подписчиков
- `mcp__telegram-mcp__get_history(chat_id="dunningkrugereffect", limit=50)` → последние 50 постов

### 2. Сохранить снимки

Дата = сегодня (YYYY-MM-DD).

**subscribers-YYYY-MM-DD.json:**
```json
{
  "date": "YYYY-MM-DD",
  "total": <число из get_chat>,
  "participants": [
    {"id": <int>, "first_name": "...", "last_name": "...", "username": "..."}
  ]
}
```

**posts-YYYY-MM-DD.json:**
```json
{
  "date": "YYYY-MM-DD",
  "posts": [
    {"id": <int>, "date": "YYYY-MM-DD HH:MM", "views": <int>, "forwards": <int>, "reactions": <int>, "text_preview": "первые 80 символов..."}
  ]
}
```

Записать оба файла в `projects/daning-kruger/.life/stats/`.

### 3. Diff подписчиков

Найти предыдущий снимок подписчиков (Glob `subscribers-*.json`, взять предпоследний по дате).

- **Предыдущий есть** → запустить:
  ```
  python3 projects/daning-kruger/.claude/skills/dg-stats/scripts/diff_subscribers.py <prev.json> <curr.json>
  ```
- **Первый снимок** → пропустить diff, отметить в отчёте.

### 4. Отчёт

Вывести в формате:

```
## @dunningkrugereffect — DD месяц YYYY

### Подписчики: N (+X / -Y с DD.MM)
Новые: @username1, Имя Фамилия
Ушли: @username2

### Топ-5 постов по просмотрам
| # | Дата | Views | Reactions | Forwards | Текст |
|---|------|-------|-----------|----------|-------|
| 1 | ... | ... | ... | ... | первые 60 символов... |

### Тренды
- Среднее просмотров на пост: N
- Среднее реакций на пост: N
- Последний пост: дата
- Всего постов в выборке: N
```

Если первый снимок — вместо diff написать: «Первый снимок, сравнение будет доступно при следующем вызове.»

## Важные правила

- Не публиковать статистику в канал
- Снимки хранятся в `.life/stats/`, не в скилле
- При ошибке MCP — сообщить пользователю, не падать молча
- **Chat ID**: использовать username `dunningkrugereffect` (не числовой ID — Telethon интерпретирует его как PeerUser)
- **Views/forwards/reactions**: `get_history` не возвращает эти метрики в текстовом выводе. Пока сохраняем как null. TODO: доработать telegram-mcp или парсить из frontmatter в `content/posts/`
