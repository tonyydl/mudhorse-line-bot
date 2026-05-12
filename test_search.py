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
