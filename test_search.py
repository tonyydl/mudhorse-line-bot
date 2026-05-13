#!/usr/bin/env python3
"""Quick manual test for the 591 scraper. Usage: python3 test_search.py"""
from rent591 import rent_591_object_list, rent_591_object_list_tostring

queries = [
    ['位置=蘆洲區', '類型=獨立套房', '租金=5000,15000'],
    ['位置=台中市', '類型=整層住家'],
    ['位置=三重區', '租金=10000,23000', '類型=整層住家'],
]

for args in queries:
    print(f">>> 591 {' '.join(args)}")
    items = rent_591_object_list(args)
    result = rent_591_object_list_tostring(items)
    print(result if result else '找不到物件。')
    print('-' * 40)

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
