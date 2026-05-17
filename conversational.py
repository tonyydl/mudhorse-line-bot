from linebot.models import (
    TextSendMessage, QuickReply, QuickReplyButton, MessageAction,
)
from rent591 import get_place_arg, rent_591_object_list, build_flex_carousel
from session import get_session, set_session, clear_session

_LOCATION_BUTTONS = ['台北市', '新北市', '台中市', '高雄市', '自行輸入']
_KIND_LABELS = ['整層住家', '獨立套房', '分租套房', '雅房', '不限']

_CITY_DISTRICTS = {
    '台北市': ['大安區', '信義區', '中山區', '內湖區', '松山區', '士林區', '文山區', '中正區', '北投區', '萬華區'],
    '新北市': ['板橋區', '三重區', '蘆洲區', '新莊區', '中和區', '永和區', '新店區', '土城區', '淡水區', '汐止區'],
    '台中市': ['西屯區', '北屯區', '南屯區', '豐原區', '大里區', '太平區', '北區', '東區', '南區', '西區'],
    '高雄市': ['三民區', '苓雅區', '前鎮區', '左營區', '楠梓區', '鳳山區', '小港區', '鼓山區', '新興區', '前金區'],
}
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
        elif text in _CITY_DISTRICTS:
            districts = _CITY_DISTRICTS[text] + ['不限（全市）', '自行輸入']
            set_session(uid, {**session, 'step': 'district', 'city': text})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請選擇{}的地區'.format(text), quick_reply=_qr(districts)),
            )
        else:
            _handle_location_text(line_bot_api, event, session, text)

    elif step == 'location_freetext':
        _handle_location_text(line_bot_api, event, session, text)

    elif step == 'district':
        city = session.get('city', '')
        if text == '不限（全市）':
            set_session(uid, {**session, 'step': 'kind', 'location': city})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請選擇類型', quick_reply=_qr(_KIND_LABELS)),
            )
        elif text == '自行輸入':
            set_session(uid, {**session, 'step': 'district_freetext'})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請輸入地區名稱（例如：蘆洲區）'),
            )
        else:
            _handle_location_text(line_bot_api, event, session, text)

    elif step == 'district_freetext':
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
