# Flex Message Carousel Design

**Date:** 2026-05-13  
**Scope:** Replace plain-text rental listing replies with LINE Flex Message carousel cards.

---

## Goal

When a user queries `591 位置=... 類型=...`, the bot replies with a visually rich carousel instead of a plain text block. Each card shows the photo, key details, and a tap-to-open button for the listing URL.

---

## Card Layout

Each Bubble card (up to 5 per carousel):

```
┌─────────────────────┐
│   封面圖（16:9）     │  photoList[0]
├─────────────────────┤
│ 標題                │  title (max 2 lines, truncated)
│ 📍 蘆洲區-復興路    │  address
│ 獨立套房 · 7.5坪    │  kind_name + area_name
│ 7F/11F              │  floor_name
├─────────────────────┤
│ 💰 13,000 元/月     │  price + price_unit (bold)
│ [  查看詳情  ]      │  URI action → item url
└─────────────────────┘
```

5 bubbles wrapped in a single Carousel container; user swipes horizontally.

---

## Code Changes

### `rent591.py`

Add one new function:

```python
def build_flex_carousel(items) -> FlexSendMessage
```

- Accepts the list returned by `rent_591_object_list()`
- Iterates over `items[:5]`, builds one `BubbleContainer` per item
- Returns a `FlexSendMessage(alt_text='591租屋搜尋結果', contents=CarouselContainer(...))`
- `rent_591_object_list_tostring()` is kept unchanged (used by `test_search.py`)

### `app.py`

In `handle_message`, replace the reply logic for the `591` command:

| Condition | Reply |
|---|---|
| Items found | `FlexSendMessage` via `build_flex_carousel(items)` |
| No items | `TextSendMessage(text='找不到物件。')` |
| JSONDecodeError | `TextSendMessage(text='591爬蟲失敗')` |

---

## SDK

No upgrade required. `FlexSendMessage`, `BubbleContainer`, `CarouselContainer` are available in `line-bot-sdk==1.9.0` (added in 1.8.0).

---

## Out of Scope

- Pagination / "下一頁"
- If `photoList` is empty, the hero image section is omitted entirely (no placeholder)
- Changes to scraping logic
