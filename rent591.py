import requests

theEnum = {'place': '位置', 'kind': '類型', 'rentprice': '租金', 'area': '坪數'}

region = {}
region[0] = [
    {'id': 0, 'txt': '北部'},
    {'id': 1, 'txt': '台北市'},
    {'id': 3, 'txt': '新北市'},
    {'id': 6, 'txt': '桃園市'},
    {'id': 4, 'txt': '新竹市'},
    {'id': 5, 'txt': '新竹縣'},
    {'id': 21, 'txt': '宜蘭縣'},
    {'id': 2, 'txt': '基隆市'}
];

region[1] = [
    {'id': 0, 'txt': '中部'},
    {'id': 8, 'txt': '台中市'},
    {'id': 10, 'txt': '彰化縣'},
    {'id': 14, 'txt': '雲林縣'},
    {'id': 7, 'txt': '苗栗縣'},
    {'id': 11, 'txt': '南投縣'}
];

region[2] = [
    {'id': 0, 'txt': '南部'},
    {'id': 17, 'txt': '高雄市'},
    {'id': 15, 'txt': '台南市'},
    {'id': 12, 'txt': '嘉義市'},
    {'id': 13, 'txt': '嘉義縣'},
    {'id': 19, 'txt': '屏東縣'}
]

region[3] = [
    {'id': 0, 'txt': '東部'},
    {'id': 22, 'txt': '台東縣'},
    {'id': 23, 'txt': '花蓮縣'},
    {'id': 24, 'txt': '澎湖縣'},
    {'id': 25, 'txt': '金門縣'},
    {'id': 26, 'txt': '連江縣'}
]

section = {}
section[1] = {1: "中正區", 2: "大同區", 3: "中山區", 4: "松山區", 5: "大安區", 6: "萬華區", 7: "信義區", 8: "士林區", 9: "北投區", 10: "內湖區",
              11: "南港區", 12: "文山區"};
section[2] = {13: "仁愛區", 14: "信義區", 15: "中正區", 16: "中山區", 17: "安樂區", 18: "暖暖區", 19: "七堵區"};
section[3] = {20: "萬里區", 21: "金山區", 26: "板橋區", 27: "汐止區", 28: "深坑區", 29: "石碇區", 30: "瑞芳區", 31: "平溪區", 32: "雙溪區",
              33: "貢寮區", 34: "新店區", 35: "坪林區", 36: "烏來區", 37: "永和區", 38: "中和區", 39: "土城區", 40: "三峽區", 41: "樹林區",
              42: "鶯歌區", 43: "三重區", 44: "新莊區", 45: "泰山區", 46: "林口區", 47: "蘆洲區", 48: "五股區", 49: "八里區", 50: "淡水區",
              51: "三芝區", 52: "石門區"};
section[4] = {370: "香山區", 371: "東區", 372: "北區"};
section[5] = {54: "竹北市", 55: "湖口鄉", 56: "新豐鄉", 57: "新埔鎮", 58: "關西鎮", 59: "芎林鄉", 60: "寶山鄉", 61: "竹東鎮", 62: "五峰鄉",
              63: "橫山鄉", 64: "尖石鄉", 65: "北埔鄉", 66: "峨嵋鄉"};
section[6] = {73: "桃園區", 67: "中壢區", 68: "平鎮區", 69: "龍潭區", 70: "楊梅區", 71: "新屋區", 72: "觀音區", 74: "龜山區", 75: "八德區",
              76: "大溪區", 77: "復興區", 78: "大園區", 79: "蘆竹區"};
section[7] = {88: "苗栗市", 80: "竹南鎮", 81: "頭份市", 82: "三灣鄉", 83: "南庄鄉", 84: "獅潭鄉", 85: "後龍鎮", 86: "通霄鎮", 87: "苑裡鎮",
              89: "造橋鄉", 90: "頭屋鄉", 91: "公館鄉", 92: "大湖鄉", 93: "泰安鄉", 94: "銅鑼鄉", 95: "三義鄉", 96: "西湖鄉", 97: "卓蘭鎮"};
section[8] = {98: "中區", 99: "東區", 100: "南區", 101: "西區", 102: "北區", 103: "北屯區", 104: "西屯區", 105: "南屯區", 106: "太平區",
              107: "大里區", 108: "霧峰區", 109: "烏日區", 110: "豐原區", 111: "后里區", 112: "石岡區", 113: "東勢區", 114: "和平區",
              115: "新社區", 116: "潭子區", 117: "大雅區", 118: "神岡區", 119: "大肚區", 120: "沙鹿區", 121: "龍井區", 122: "梧棲區",
              123: "清水區", 124: "大甲區", 125: "外埔區", 126: "大安區"};
section[10] = {127: "彰化市", 128: "芬園鄉", 129: "花壇鄉", 130: "秀水鄉", 131: "鹿港鎮", 132: "福興鄉", 133: "線西鄉", 134: "和美鎮",
               135: "伸港鄉", 136: "員林市", 137: "社頭鄉", 138: "永靖鄉", 139: "埔心鄉", 140: "溪湖鎮", 141: "大村鄉", 142: "埔鹽鄉",
               143: "田中鎮", 144: "北斗鎮", 145: "田尾鄉", 146: "埤頭鄉", 147: "溪州鄉", 148: "竹塘鄉", 149: "二林鎮", 150: "大城鄉",
               151: "芳苑鄉", 152: "二水鄉"};
section[11] = {153: "南投市", 154: "中寮鄉", 155: "草屯鎮", 156: "國姓鄉", 157: "埔里鎮", 158: "仁愛鄉", 159: "名間鄉", 160: "集集鎮",
               161: "水里鄉", 162: "魚池鄉", 163: "信義鄉", 164: "竹山鎮", 165: "鹿谷鄉"};
section[12] = {373: "西區", 374: "東區"};
section[13] = {167: "番路鄉", 168: "梅山鄉", 169: "竹崎鄉", 170: "阿里山鄉", 171: "中埔鄉", 172: "大埔鄉", 173: "水上鄉", 174: "鹿草鄉",
               175: "太保市", 176: "朴子市", 177: "東石鄉", 178: "六腳鄉", 179: "新港鄉", 180: "民雄鄉", 181: "大林鎮", 182: "溪口鄉",
               183: "義竹鄉", 184: "布袋鎮"};
section[14] = {185: "斗南鎮", 186: "大埤鄉", 187: "虎尾鎮", 188: "土庫鎮", 189: "褒忠鄉", 190: "東勢鄉", 191: "臺西鄉", 192: "崙背鄉",
               193: "麥寮鄉", 194: "斗六市", 195: "林內鄉", 196: "古坑鄉", 197: "莿桐鄉", 198: "西螺鎮", 199: "二崙鄉", 200: "北港鎮",
               201: "水林鄉", 202: "口湖鄉", 203: "四湖鄉", 204: "元長鄉"};
section[15] = {206: "東區", 207: "南區", 208: "中西區", 209: "北區", 210: "安平區", 211: "安南區", 212: "永康區", 213: "歸仁區", 214: "新化區",
               215: "左鎮區", 216: "玉井區", 217: "楠西區", 218: "南化區", 219: "仁德區", 220: "關廟區", 221: "龍崎區", 222: "官田區",
               223: "麻豆區", 224: "佳里區", 225: "西港區", 226: "七股區", 227: "將軍區", 228: "學甲區", 229: "北門區", 230: "新營區",
               231: "後壁區", 232: "白河區", 233: "東山區", 234: "六甲區", 235: "下營區", 236: "柳營區", 237: "鹽水區", 238: "善化區",
               239: "大內區", 240: "山上區", 241: "新市區", 242: "安定區"};
section[17] = {243: "新興區", 244: "前金區", 245: "苓雅區", 246: "鹽埕區", 247: "鼓山區", 248: "旗津區", 249: "前鎮區", 250: "三民區",
               251: "楠梓區", 252: "小港區", 253: "左營區", 254: "仁武區", 255: "大社區", 258: "岡山區", 259: "路竹區", 260: "阿蓮區",
               261: "田寮區", 262: "燕巢區", 263: "橋頭區", 264: "梓官區", 265: "彌陀區", 266: "永安區", 267: "湖內區", 268: "鳳山區",
               269: "大寮區", 270: "林園區", 271: "鳥松區", 272: "大樹區", 273: "旗山區", 274: "美濃區", 275: "六龜區", 276: "內門區",
               277: "杉林區", 278: "甲仙區", 279: "桃源區", 280: "那瑪夏區", 281: "茂林區", 282: "茄萣區"};
section[19] = {295: "屏東市", 296: "三地門鄉", 297: "霧臺鄉", 298: "瑪家鄉", 299: "九如鄉", 300: "里港鄉", 301: "高樹鄉", 302: "鹽埔鄉",
               303: "長治鄉", 304: "麟洛鄉", 305: "竹田鄉", 306: "內埔鄉", 307: "萬丹鄉", 308: "潮州鎮", 309: "泰武鄉", 310: "來義鄉",
               311: "萬巒鄉", 312: "崁頂鄉", 313: "新埤鄉", 314: "南州鄉", 315: "林邊鄉", 316: "東港鎮", 317: "琉球鄉", 318: "佳冬鄉",
               319: "新園鄉", 320: "枋寮鄉", 321: "枋山鄉", 322: "春日鄉", 323: "獅子鄉", 324: "車城鄉", 325: "牡丹鄉", 326: "恆春鎮",
               327: "滿州鄉"};
section[21] = {328: "宜蘭市", 329: "頭城鎮", 330: "礁溪鄉", 331: "壯圍鄉", 332: "員山鄉", 333: "羅東鎮", 334: "三星鄉", 335: "大同鄉",
               336: "五結鄉", 337: "冬山鄉", 338: "蘇澳鎮", 339: "南澳鄉"};
section[22] = {341: "台東市", 342: "綠島鄉", 343: "蘭嶼鄉", 344: "延平鄉", 345: "卑南鄉", 346: "鹿野鄉", 347: "關山鎮", 348: "海端鄉",
               349: "池上鄉", 350: "東河鄉", 351: "成功鎮", 352: "長濱鄉", 353: "太麻里鄉", 354: "金峰鄉", 355: "大武鄉", 356: "達仁鄉"};
section[23] = {357: "花蓮市", 358: "新城鄉", 359: "秀林鄉", 360: "吉安鄉", 361: "壽豐鄉", 362: "鳳林鎮", 363: "光復鄉", 364: "豐濱鄉",
               365: "瑞穗鄉", 366: "萬榮鄉", 367: "玉里鎮", 368: "卓溪鄉", 369: "富里鄉"};
section[24] = {283: "馬公市", 284: "西嶼鄉", 285: "望安鄉", 286: "七美鄉", 287: "白沙鄉", 288: "湖西鄉"};
section[25] = {289: "金沙鎮", 290: "金湖鎮", 291: "金寧鄉", 292: "金城鎮", 293: "烈嶼鄉", 294: "烏坵鄉"};
section[26] = {22: "南竿鄉", 23: "北竿鄉", 24: "莒光鄉", 25: "東引鄉", 256: "東沙", 257: "南沙"};

kind = {1: '整層住家', 2: '獨立套房', 3: '分租套房', 4: '雅房', 8: '車位', 24: '其他'}


def get_region_name(input_region_name):
    for i in region:
        for re in region[i]:
            if re['txt'] == input_region_name:
                return re['id']
    return -1


def get_section_name(input_section_name):
    for i in section:
        for number, sec in section[i].items():
            if sec == input_section_name:
                return i, number
    return -1, -1


def get_place_arg(input_place_name):
    region_number = get_region_name(input_place_name)
    if region_number != -1:
        return 'region=' + str(region_number)
    else:
        the_region_number, section_number = get_section_name(input_place_name)
        if the_region_number != -1 and section_number != -1:
            return 'region=' + str(the_region_number) + '&section=' + str(section_number)
    return ''


def get_kind_arg(input_kind_name):
    for k, v in kind.items():
        if v == input_kind_name:
            return 'kind=' + str(k)
    return ''


def get_arguments_content(lists):
    content = ''
    for n in lists:
        m = n.split('=')
        if len(m) <= 1:
            continue
        input_key = m[0]
        input_value = m[1]
        for k, v in theEnum.items():
            if v == input_key:
                if k == 'place':
                    place_arg = get_place_arg(input_value)
                    if place_arg != '':
                        content += place_arg + '&'
                    break
                if k == 'kind':
                    kind_arg = get_kind_arg(input_value)
                    if kind_arg != '':
                        content += kind_arg + '&'
                    break
                content += k + '=' + input_value + '&'
                break
    return content[:-1] if len(content) > 0 and content[-1] == '&' else content


def rent_591_object_list(argu):
    print(argu)
    argu_content = get_arguments_content(argu)
    if argu_content == '':
        return []
    print(argu_content)
    target_url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&' + argu_content
    print(target_url)
    header = {
        'Host': 'rent.591.com.tw',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2',
        'Cookie': 'PHPSESSID=sdsini6kdld2gnblp9h9nuur20; userLoginHttpReferer=https%253A%252F%252Fwww.591.com.tw%252Fuser-login.html; 591equipment=08826710014998500681545450; ResolutionSort=1; index_keyword_search_analysis=%7B%22role%22%3A%221%22%2C%22type%22%3A2%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%E4%B8%89%E9%87%8D%E5%8D%80%22%2C%22menu%22%3A%22400-800%E8%90%AC%22%2C%22hasHistory%22%3A1%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; detail-guide=1; last_search_type=1; localTime=2; imgClick=5407932; __utma=82835026.1593737612.1499849967.1500696632.1500867495.2; __utmc=82835026; __utmz=82835026.1500696632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); user_index_role=1; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225424210%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225372536%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225429867%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225413919%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225422226%22%3B%7D%7D; ba_cid=a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%225f91a10df47762976645e67b67ee4864%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-5372536.html%22%3Bs%3A4%3A%22page%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-5424210.html%22%3Bs%3A7%3A%22time_ex%22%3Bi%3A1501484991%3Bs%3A4%3A%22time%22%3Bi%3A1501485062%3B%7D; __auc=e1db4f0b15d3607a4d9066c79d8; c10f3143a018a0513ebe1e8d27b5391c=1; client:unique:pc=eyJpdiI6Ink3RHRFU01hYnVEZVwvSkVPWThuVjBRPT0iLCJ2YWx1ZSI6ImVtRW5ZWkNZeEtlOWxQYTMrZlFuS0E9PSIsIm1hYyI6ImZkZTlmMjBmMTFjZThkYjgwY2VlMWZiNjhlNjdjOWQ2NjUyMWE0ZmEzMzRlNjEyYWMwYjQxNzIzMDM2MmEyZDUifQ%3D%3D; is_new_index=1; is_new_index_redirect=1; loginNoticeStatus=1; loginNoticeNumber=3; new_rent_list_kind_test=0; _ga=GA1.3.1593737612.1499849967; _gid=GA1.3.1595742426.1501650062; _ga=GA1.4.1593737612.1499849967; _gid=GA1.4.1595742426.1501650062; urlJumpIp=3; urlJumpIpByTxt=%E6%96%B0%E5%8C%97%E5%B8%82;'
    }
    res = requests.Session()
    req = res.get(target_url, headers=header)
    data = req.json()
    return data['data']['data']


def rent_591_object_list_tostring(items):
    limit = 5
    cnt = 0
    content = ''
    for item in items:
        title = item['address_img']
        layout = item['layout']
        kind_name = item['kind_name']
        full_address = item['section_name'] + item['street_name'] + item['addr_number_name']
        price = item['price']
        link = "https://rent.591.com.tw/rent-detail-{}.html".format(item['id'])
        content += "{}\n{}\n{}\n{}\n{}\n{}\n\n".format(title, layout, kind_name, full_address, price, link)
        cnt += 1
        if cnt >= limit:
            break
    return content
