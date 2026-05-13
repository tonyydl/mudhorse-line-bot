# Flex Message Carousel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace plain-text rental listing replies with a LINE Flex Message carousel — each of the 5 results becomes a swipeable card with photo, details, and a tap-to-open button.

**Architecture:** Add `build_flex_carousel(items)` and `_build_bubble(item)` to `rent591.py`; update `handle_message` in `app.py` to call it. No scraping logic changes. No SDK upgrade needed.

**Tech Stack:** Python 3, line-bot-sdk==1.9.0 (`FlexSendMessage`, `BubbleContainer`, `CarouselContainer`, `ImageComponent`, `BoxComponent`, `TextComponent`, `ButtonComponent`, `URIAction`)

---

## File Map

| File | Change |
|------|--------|
| `rent591.py` | Add `_build_bubble(item)` and `build_flex_carousel(items)` at the bottom |
| `app.py` | Import `build_flex_carousel`; swap `TextSendMessage` for `FlexSendMessage` on success path |

---

### Task 1: Add `_build_bubble` and `build_flex_carousel` to `rent591.py`

**Files:**
- Modify: `rent591.py` (append to end of file)

- [ ] **Step 1: Add the new imports at the top of `rent591.py`**

Open `rent591.py`. The first line is `import requests`. Add the linebot imports after it:

```python
import requests

from linebot.models import (
    FlexSendMessage, BubbleContainer, CarouselContainer,
    ImageComponent, BoxComponent, TextComponent,
    ButtonComponent, URIAction,
)
```

- [ ] **Step 2: Append `_build_bubble` to the end of `rent591.py`**

```python
def _build_bubble(item):
    photo_list = item.get('photoList', [])
    hero = None
    if photo_list:
        hero = ImageComponent(
            url=photo_list[0],
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=URIAction(label='查看詳情', uri=item.get('url', '')),
        )

    body = BoxComponent(
        layout='vertical',
        contents=[
            TextComponent(
                text=item.get('title', ''),
                weight='bold',
                size='md',
                wrap=True,
                max_lines=2,
            ),
            BoxComponent(
                layout='vertical',
                margin='md',
                spacing='sm',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='sm',
                        contents=[
                            TextComponent(text='📍', size='sm', flex=0),
                            TextComponent(
                                text=item.get('address', ''),
                                wrap=True,
                                size='sm',
                                flex=5,
                                color='#666666',
                            ),
                        ],
                    ),
                    BoxComponent(
                        layout='baseline',
                        spacing='sm',
                        contents=[
                            TextComponent(text='🏠', size='sm', flex=0),
                            TextComponent(
                                text='{} · {}'.format(
                                    item.get('kind_name', ''),
                                    item.get('area_name', ''),
                                ),
                                size='sm',
                                flex=5,
                                color='#666666',
                            ),
                        ],
                    ),
                    BoxComponent(
                        layout='baseline',
                        spacing='sm',
                        contents=[
                            TextComponent(text='🏢', size='sm', flex=0),
                            TextComponent(
                                text=item.get('floor_name', ''),
                                size='sm',
                                flex=5,
                                color='#666666',
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    footer = BoxComponent(
        layout='vertical',
        spacing='sm',
        contents=[
            TextComponent(
                text=item.get('price', '') + ' ' + item.get('price_unit', '元/月'),
                weight='bold',
                size='xl',
                color='#1DB446',
            ),
            ButtonComponent(
                style='primary',
                height='sm',
                action=URIAction(label='查看詳情', uri=item.get('url', '')),
            ),
        ],
    )

    return BubbleContainer(hero=hero, body=body, footer=footer)
```

- [ ] **Step 3: Append `build_flex_carousel` right after `_build_bubble`**

```python
def build_flex_carousel(items):
    bubbles = [_build_bubble(item) for item in items[:5]]
    return FlexSendMessage(
        alt_text='591租屋搜尋結果',
        contents=CarouselContainer(contents=bubbles),
    )
```

- [ ] **Step 4: Verify the new functions can be imported and run without error**

```bash
python3 -c "
from rent591 import rent_591_object_list, build_flex_carousel
items = rent_591_object_list(['位置=蘆洲區', '類型=獨立套房', '租金=5000,15000'])
msg = build_flex_carousel(items)
print('type:', type(msg).__name__)
print('alt_text:', msg.alt_text)
print('bubble count:', len(msg.contents.contents))
first = msg.contents.contents[0]
print('first hero url:', first.hero.url if first.hero else 'no photo')
print('first body title:', first.body.contents[0].text[:30])
print('first footer price:', first.footer.contents[0].text)
"
```

Expected output (values will vary):
```
type: FlexSendMessage
alt_text: 591租屋搜尋結果
bubble count: 5
first hero url: https://img2.591.com.tw/...
first body title: 🌈飯店式套房🔥食衣住行皆...
first footer price: 13,000 元/月
```

- [ ] **Step 5: Commit**

```bash
git add rent591.py
git commit -m "feat: add build_flex_carousel for LINE Flex Message cards"
```

---

### Task 2: Update `app.py` to send Flex Message

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Add `build_flex_carousel` to the import line**

Current import line in `app.py`:
```python
from rent591 import *
```

This already imports everything via `*`, so no change needed — `build_flex_carousel` is already available. Skip to Step 2.

- [ ] **Step 2: Replace the success reply in `handle_message`**

Find and replace this entire block in `app.py` (inside the `if main_action == '591':` branch):

```python
        try:
            items = rent_591_object_list(argu)
            content = rent_591_object_list_tostring(items)
        except JSONDecodeError:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='591爬蟲失敗'))
            return 0
        if content == '':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='找不到物件。'))
            return 0
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

        return 0
```

Replace with:

```python
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
```

- [ ] **Step 3: Verify `app.py` starts cleanly (env vars just need to be set, values don't matter)**

```bash
LINE_CHANNEL_SECRET=test LINE_CHANNEL_ACCESS_TOKEN=test python3 -c "import app; print('app imported OK')"
```

Expected:
```
app imported OK
```

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat: send Flex Message carousel in LINE bot reply"
```

---

### Task 3: Update `test_search.py` to also print Flex Message structure

**Files:**
- Modify: `test_search.py`

- [ ] **Step 1: Add a Flex Message verification block to `test_search.py`**

Append to the end of `test_search.py`:

```python
print("\n=== Flex Message structure check ===")
from rent591 import build_flex_carousel
sample = rent_591_object_list(['位置=蘆洲區', '類型=獨立套房', '租金=5000,15000'])
msg = build_flex_carousel(sample)
print(f"FlexSendMessage alt_text: {msg.alt_text}")
print(f"Bubble count: {len(msg.contents.contents)}")
for i, bubble in enumerate(msg.contents.contents):
    title = bubble.body.contents[0].text[:25] if bubble.body else '?'
    price = bubble.footer.contents[0].text if bubble.footer else '?'
    has_photo = '✓' if bubble.hero else '✗'
    print(f"  [{i+1}] photo={has_photo}  {title!r}  {price}")
```

- [ ] **Step 2: Run the full test script and confirm output**

```bash
python3 test_search.py
```

Expected (last section):
```
=== Flex Message structure check ===
FlexSendMessage alt_text: 591租屋搜尋結果
Bubble count: 5
  [1] photo=✓  '🌈飯店式套房...'  13,000 元/月
  [2] photo=✓  '徐匯捷運套房...'  11,800 元/月
  ...
```

- [ ] **Step 3: Commit**

```bash
git add test_search.py
git commit -m "test: add Flex Message structure check to test_search.py"
```
