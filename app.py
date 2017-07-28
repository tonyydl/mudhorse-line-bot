import os
import sys
import requests
import re
import random

from bs4 import BeautifulSoup
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

# get channel_secret and channel_access_token from your environment variable
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
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def androidweekly():
    target_url = 'http://androidweekly.net'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''

    cnt = 0
    for item in soup.select('.latest-stuff .latest-issue .rahmen .sections .article-headline'):
        title = item.text
        link = item['href']
        data = '{}\n{}\n\n'.format(title, link)
        content += data
        cnt += 1
        if cnt >= 5:
            break
    return content

def rent591_datalist(argu):
    arguContent = getArgumentsContent(argu)
    print (arguContent)
    target_url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&' + arguContent
    header = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2',
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive',
            'Cookie' : "PHPSESSID=sdsini6kdld2gnblp9h9nuur20; userLoginHttpReferer=https%253A%252F%252Fwww.591.com.tw%252Fuser-login.html; 591equipment=08826710014998500681545450; ResolutionSort=1; index_keyword_search_analysis=%7B%22role%22%3A%221%22%2C%22type%22%3A2%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%E4%B8%89%E9%87%8D%E5%8D%80%22%2C%22menu%22%3A%22400-800%E8%90%AC%22%2C%22hasHistory%22%3A1%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; detail-guide=1; last_search_type=1; localTime=2; imgClick=5407932; c10f3143a018a0513ebe1e8d27b5391c=1; is_new_index=1; is_new_index_redirect=1; today_role=eyJpdiI6InJNdHpHazdVMVMrSktqejNyYzR6MkE9PSIsInZhbHVlIjoiYVdFMVAwNGtCYTRWZXpuOGJtMUpHZz09IiwibWFjIjoiOWU2MDM1YWQwMjk0NzBhNzRjZThlMzdkNjI5Y2FkNmJkZGU5NDlmMjE3YzExNmE1M2RkMjRkOWRkN2Y0N2E3OSJ9; user_sessionid=sdsini6kdld2gnblp9h9nuur20; DETAIL[1][5422330]=1; DETAIL[1][5415350]=1; DETAIL[1][5426465]=1; user_index_role=1; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225426465%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225415350%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225422330%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225408991%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225343842%22%3B%7D%7D; ba_cid=a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%225f91a10df47762976645e67b67ee4864%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-5415350.html%22%3Bs%3A4%3A%22page%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-5426465.html%22%3Bs%3A7%3A%22time_ex%22%3Bi%3A1500861727%3Bs%3A4%3A%22time%22%3Bi%3A1500861749%3B%7D; loginNoticeStatus=1; loginNoticeNumber=2; __asc=c2e9982815d72ac825af4f0143e; __auc=e1db4f0b15d3607a4d9066c79d8; __utma=82835026.1593737612.1499849967.1500696632.1500867495.2; __utmb=82835026.1.10.1500867495; __utmc=82835026; __utmz=82835026.1500696632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); urlJumpIp=3; urlJumpIpByTxt=%E6%96%B0%E5%8C%97%E5%B8%82; _gat_tw591=1; _dc_gtm_UA-97423186-1=1; new_rent_list_kind_test=0; _ga=GA1.3.1593737612.1499849967; _gid=GA1.3.1740626314.1500688929; _ga=GA1.4.1593737612.1499849967; _gid=GA1.4.1740626314.1500688929; 591_new_session=eyJpdiI6InNmK0RhZWMyUVNvWDFVUDBOMTFEXC9BPT0iLCJ2YWx1ZSI6IlwvN1hsNzRqbnY0aVpGYjdPNkY3clBSdys1RkgwVjJZa0pPamZDdzd1ZDZmYXdtcnRJV1hNNmNnTlMyR3g1SDJKMHorUmI5K282QktwTUNzMzVPTitydz09IiwibWFjIjoiZWRmMGNjNmU5NDk1OWY0NTFhYzk1ZmMwZWEwODgxYzgwNjY0N2ViMWQ1ZjBjNTg0NzM5NzEyOTZkMDlmNmY3NiJ9",
            'Host' : 'rent.591.com.tw',
    }
    res = requests.Session()
    req = res.get(target_url, headers=header)
    data = req.json()
    return data['data']['data']

def rent591_datalist_tostring(items):
    limit = 5
    cnt = 0
    content = ''
    for item in items:
        title = item['address_img']
        layout = item['layout']
        kind_name = item['kind_name']
        fulladdress = item['section_name'] + item['street_name'] + item['addr_number_name']
        price = item['price']
        link = "https://rent.591.com.tw/rent-detail-{}.html".format(item['id'])
        content += "{}\n{}\n{}\n{}\n{}\n{}\n\n".format(title, layout, kind_name, fulladdress, price, link)
        cnt += 1
        if cnt >= limit:
            break;
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event_message = event.message.text.strip().split(' ')
    main_action = event_message[0]
    if main_action == 'androidweekly':
        content = androidweekly()
        print (content)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if main_action == '591':
        argu = event_message[1:]
        items = rent591_datalist(argu)
        content = rent591_datalist_tostring(items)
        print (content)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
