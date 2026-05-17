# Conversational Search Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a guided 3-step Quick Reply flow (地區 → 類型 → 租金) so users can search by tapping buttons instead of memorising the command format, while keeping the existing `591 位置=... 類型=...` format working.

**Architecture:** Two new modules — `session.py` (in-memory state with 10-min TTL) and `conversational.py` (Quick Reply message builders + step dispatch). `app.py` gets a single new routing branch that checks for an active session before the existing `591` command handler.

**Tech Stack:** Python 3, line-bot-sdk==1.9.0 (`QuickReply`, `QuickReplyButton`, `MessageAction`, `TextSendMessage`)

---

## File Map

| File | Change |
|------|--------|
| `session.py` | **Create** — in-memory session store with TTL |
| `conversational.py` | **Create** — Quick Reply builders + step logic |
| `app.py` | **Modify** — new routing branch + imports |

---

### Task 1: Create `session.py`

**Files:**
- Create: `session.py`

- [ ] **Step 1: Create `session.py` with the full implementation**

```python
import time

_sessions = {}  # user_id -> {step, location, kind, expires}


def get_session(user_id):
    """Return active session dict or None if missing/expired."""
    entry = _sessions.get(user_id)
    if entry is None:
        return None
    if time.time() > entry['expires']:
        del _sessions[user_id]
        return None
    return entry


def set_session(user_id, data):
    """Create or overwrite session, resetting the 10-minute TTL."""
    _sessions[user_id] = {**data, 'expires': time.time() + 600}


def clear_session(user_id):
    """Remove session (no-op if absent)."""
    _sessions.pop(user_id, None)
```

- [ ] **Step 2: Verify session logic with a quick manual test**

```bash
python3 -c "
import time
from session import get_session, set_session, clear_session

# no session yet
assert get_session('u1') is None

# set and get
set_session('u1', {'step': 'location'})
s = get_session('u1')
assert s['step'] == 'location'
assert 'expires' in s

# clear
clear_session('u1')
assert get_session('u1') is None

print('session.py OK')
"
```

Expected: `session.py OK`

- [ ] **Step 3: Commit**

```bash
git add session.py
git commit -m "feat: add in-memory session store with 10-min TTL"
```

---

### Task 2: Create `conversational.py`

**Files:**
- Create: `conversational.py`

- [ ] **Step 1: Create `conversational.py` with the full implementation**

```python
from linebot.models import (
    TextSendMessage, QuickReply, QuickReplyButton, MessageAction,
)
from rent591 import get_place_arg, rent_591_object_list, build_flex_carousel
from session import get_session, set_session, clear_session

_LOCATION_BUTTONS = ['台北市', '新北市', '台中市', '高雄市', '自行輸入']
_KIND_LABELS = ['整層住家', '獨立套房', '分租套房', '雅房', '不限']
_PRICE_LABELS = ['不限', '5000以下', '5000~15000', '15000~30000', '30000以上']

_PRICE_MAP = {
    '不限':        None,
    '5000以下':    '0,5000',
    '5000~15000':  '5000,15000',
    '15000~30000': '15000,30000',
    '30000以上':   '30000,999999',
}


def _qr(labels):
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label=t, text=t)) for t in labels
    ])


def start_flow(line_bot_api, event):
    """Clear any existing session and start at step=location."""
    clear_session(event.source.user_id)
    set_session(event.source.user_id, {'step': 'location'})
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='請選擇地區', quick_reply=_qr(_LOCATION_BUTTONS)),
    )


def handle_step(line_bot_api, event, session, text):
    """Dispatch to the correct step handler based on session['step']."""
    step = session['step']
    uid = event.source.user_id

    if step == 'location':
        if text == '自行輸入':
            set_session(uid, {**session, 'step': 'location_freetext'})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請輸入地區名稱（例如：蘆洲區）'),
            )
        else:
            _handle_location_text(line_bot_api, event, session, text)

    elif step == 'location_freetext':
        _handle_location_text(line_bot_api, event, session, text)

    elif step == 'kind':
        if text not in _KIND_LABELS:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請從按鈕中選擇類型', quick_reply=_qr(_KIND_LABELS)),
            )
            return
        set_session(uid, {**session, 'step': 'price', 'kind': text})
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請選擇租金範圍', quick_reply=_qr(_PRICE_LABELS)),
        )

    elif step == 'price':
        if text not in _PRICE_MAP:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請從按鈕中選擇租金範圍', quick_reply=_qr(_PRICE_LABELS)),
            )
            return
        _run_search(line_bot_api, event, session, text)


def _handle_location_text(line_bot_api, event, session, text):
    uid = event.source.user_id
    if not get_place_arg(text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='找不到「{}」，請重新輸入地區名稱'.format(text)),
        )
        return
    set_session(uid, {**session, 'step': 'kind', 'location': text})
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='請選擇類型', quick_reply=_qr(_KIND_LABELS)),
    )


def _run_search(line_bot_api, event, session, price_label):
    uid = event.source.user_id
    clear_session(uid)

    argu = ['位置=' + session['location']]
    kind = session.get('kind', '不限')
    if kind != '不限':
        argu.append('類型=' + kind)
    price = _PRICE_MAP[price_label]
    if price:
        argu.append('租金=' + price)

    items = rent_591_object_list(argu)
    if not items:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='找不到物件。'),
        )
        return

    line_bot_api.reply_message(
        event.reply_token,
        build_flex_carousel(items),
    )
```

- [ ] **Step 2: Verify `conversational.py` imports cleanly and key internals are correct**

```bash
python3 -c "
from conversational import _PRICE_MAP, _qr, _KIND_LABELS, _PRICE_LABELS, _LOCATION_BUTTONS

# price map completeness
assert len(_PRICE_MAP) == 5
assert _PRICE_MAP['不限'] is None
assert _PRICE_MAP['5000~15000'] == '5000,15000'
assert _PRICE_MAP['30000以上'] == '30000,999999'

# qr builder
qr = _qr(['A', 'B'])
assert len(qr.items) == 2
assert qr.items[0].action.label == 'A'
assert qr.items[0].action.text == 'A'

print('conversational.py OK')
"
```

Expected: `conversational.py OK`

- [ ] **Step 3: Commit**

```bash
git add conversational.py
git commit -m "feat: add conversational flow with Quick Reply step handlers"
```

---

### Task 3: Update `app.py` to route conversational sessions

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Add imports and update `handle_message`**

Replace the entire content of `app.py` with:

```python
#!/usr/bin/env python3
from json.decoder import JSONDecodeError
import os
import sys

from flask import Flask, request, abort
from rent591 import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from session import get_session
from conversational import start_flow, handle_step

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    uid = event.source.user_id

    # Active conversational session takes priority
    session = get_session(uid)
    if session:
        handle_step(line_bot_api, event, session, text)
        return 0

    parts = text.split(' ')
    main_action = parts[0]

    if main_action == '591':
        argu = parts[1:]
        if not argu:
            start_flow(line_bot_api, event)
            return 0
        try:
            items = rent_591_object_list(argu)
        except JSONDecodeError:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='591爬蟲失敗'))
            return 0

        if not items:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='找不到物件。'))
            return 0

        line_bot_api.reply_message(
            event.reply_token,
            build_flex_carousel(items))
        return 0

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='無法辨識 「{0}」，範例：「591 位置=蘆洲區 類型=獨立套房 租金=5000,15000」，更多指令請參考 https://github.com/tonyyang924/mudhorse-line-bot'.format(text)))


if __name__ == "__main__":
    app.run()
```

- [ ] **Step 2: Verify `app.py` imports cleanly**

```bash
LINE_CHANNEL_SECRET=test LINE_CHANNEL_ACCESS_TOKEN=test python3 -c "import app; print('app.py OK')"
```

Expected: `app.py OK`

- [ ] **Step 3: Run a full integration check**

```bash
python3 -c "
from session import get_session, set_session, clear_session
from conversational import _PRICE_MAP, _KIND_LABELS, _LOCATION_BUTTONS, _PRICE_LABELS

# simulate a full flow
uid = 'test_user'

# step 1 — location selected
set_session(uid, {'step': 'kind', 'location': '蘆洲區'})
s = get_session(uid)
assert s['step'] == 'kind'
assert s['location'] == '蘆洲區'

# step 2 — kind selected
set_session(uid, {**s, 'step': 'price', 'kind': '獨立套房'})
s = get_session(uid)
assert s['step'] == 'price'
assert s['kind'] == '獨立套房'

# step 3 — build argu list (same logic as _run_search)
argu = ['位置=' + s['location']]
argu.append('類型=' + s['kind'])
argu.append('租金=' + _PRICE_MAP['5000~15000'])
assert argu == ['位置=蘆洲區', '類型=獨立套房', '租金=5000,15000']

# clear session
clear_session(uid)
assert get_session(uid) is None

print('integration check OK')
"
```

Expected: `integration check OK`

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat: route conversational sessions in handle_message"
```
