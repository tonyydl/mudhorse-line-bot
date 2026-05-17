# Conversational Search Flow Design

**Date:** 2026-05-17  
**Scope:** Add a guided 3-step Quick Reply flow so users can search without memorising the command format. Existing `591 位置=... 類型=... 租金=...` format is preserved unchanged.

---

## User Flow

```
User: "591"  (no arguments)
Bot:  "請選擇地區" + Quick Reply buttons
      [台北市] [新北市] [台中市] [高雄市] [自行輸入]

User taps "新北市"  (or types any valid location)
Bot:  "請選擇類型" + Quick Reply buttons
      [整層住家] [獨立套房] [分租套房] [雅房] [不限]

User taps "獨立套房"
Bot:  "請選擇租金範圍" + Quick Reply buttons
      [不限] [5000以下] [5000-15000] [15000-30000] [30000以上]

User taps "5000-15000"
Bot:  → run search → return Flex Message carousel (existing behaviour)
```

The existing format `591 位置=蘆洲區 類型=獨立套房 租金=5000,15000` continues to work with no changes.

---

## Architecture

### New file: `session.py`

Owns all session state. Uses an in-memory dict keyed by LINE `user_id`.

```
sessions: dict[str, SessionEntry]

SessionEntry:
  step:      'location' | 'location_freetext' | 'kind' | 'price'
  location:  str | None
  kind:      str | None
  expires:   float  (time.time() + 600)
```

Public API:
- `get_session(user_id) -> SessionEntry | None` — returns None if not found or expired
- `set_session(user_id, data: dict)` — creates/updates entry, resets 10-minute TTL
- `clear_session(user_id)` — removes entry
- `is_conversational_reply(user_id, text) -> bool` — True if user_id has an active session

Expiry is checked lazily on `get_session` (no background thread needed).

### Changes to `app.py`

`handle_message` gains a new branch **before** the existing `591` command check:

```
if active session for this user:
    route to conversational_step_handler(event, session, text)
elif text == '591' (no args):
    start new session, send location Quick Reply
elif text starts with '591 ':
    existing command parser (unchanged)
else:
    existing unknown-command reply (unchanged)
```

### New helper: `conversational.py`

Contains the step logic and Quick Reply message builders:

- `start_flow(event)` — clears any existing session, saves step='location', sends location Quick Reply
- `handle_step(event, session, text)` — dispatches to the right step handler:
  - `_handle_location(event, session, text)` — validates location, saves it, sends kind Quick Reply
  - `_handle_kind(event, session, text)` — validates kind, saves it, sends price Quick Reply
  - `_handle_price(event, session, text)` — maps label→rentprice param, clears session, runs search, sends Flex carousel

---

## Quick Reply Options

### Location (step 1)
Buttons: `台北市`, `新北市`, `台中市`, `高雄市`, `自行輸入`

`自行輸入` sends the text "自行輸入". The bot replies "請輸入地區名稱（例如：蘆洲區）" and sets session step to `location_freetext`. The next plain-text message from that user is treated as the location input and validated against the region/section lookup.

### Kind (step 2)
Buttons: `整層住家`, `獨立套房`, `分租套房`, `雅房`, `不限`

`不限` = no `kind` parameter in the search.

### Price range (step 3)
Buttons: `不限`, `5000以下`, `5000~15000`, `15000~30000`, `30000以上`

Mapping to `rentprice` API param:
| Button | rentprice value |
|--------|----------------|
| 不限 | *(omitted)* |
| 5000以下 | `0,5000` |
| 5000~15000 | `5000,15000` |
| 15000~30000 | `15000,30000` |
| 30000以上 | `30000,999999` |

---

## Error Handling

- **Invalid free-text location** (not found in region/section lookup): reply "找不到「X」，請重新輸入地區名稱" and keep session at step=location.
- **Session expired mid-flow**: treat as no session; if text is ambiguous, prompt user to start again with "591".
- **Search returns 0 results**: existing `TextSendMessage('找不到物件。')` reply, session cleared.

---

## Out of Scope

- Persistent session storage (Redis)
- 坪數 (area) step
- Cancelling mid-flow (user can just ignore; session expires in 10 min)
- LINE Rich Menu
