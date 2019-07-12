import re
import json
import datetime

import requests
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from flask import Flask, request

from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.web.classes.interactions import MessageInteractiveEvent

import Json_parser
import VitualEnv

SLACK_TOKEN = "xoxb-686562110308-677176448707-etp0wb6U99S0T0OqSUwRiNZV"
SLACK_SIGNING_SECRET = "89e9bdfb86fb67d4c3d1c02ca368bae4"

app = Flask(__name__)
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

check_pre_time = None
check_pre_msg = ""

def formatting_msg():
    print(_crawl_listitem(5))
    result = Json_parser.jsonCreater(_crawl_listitem(5))

    return result


# 알구몬 listitem 크롤링 함수
def _crawl_listitem(cnt, rank=False):
    url = "https://algumon.com"
    if rank:
        url = "https://algumon.com/deal/rank"
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    list_items = []

    # 입력 숫자만큼 리스트에 추가
    index_cnt = int(cnt)

    if index_cnt < 1:
        index_cnt = 5
    elif index_cnt > 20:
        index_cnt = 20

    for list_item in soup.find_all("div", class_="post-group"):
        if index_cnt == 0:
            break
        index_cnt -= 1

        #product name
        product_name = list_item.find("a", class_="product-link").getText().strip()

        #price
        price_tag = list_item.find("small", class_="product-price")
        if price_tag !=None:
            price = price_tag.getText().strip()
        else:
            price = "가격정보없음"

        #time
        time = list_item.find("small", class_="label-time pull-right text-muted").getText().strip()

        #img_url
        img_url_tag = list_item.find("div", class_="product-img-box")
        is_img = img_url_tag.find("span",class_= "no-image")
        if is_img == None:
            str_img = img_url_tag.find("img").get("src")
            img_url = "https://" + urllib.parse.quote(str_img[8:], safe="/")
        else:
            img_url = "https://static.thenounproject.com/png/340719-200.png"

        #market_str
        market_str = list_item.find("span", class_="label shop").getText().strip()

        #source_str
        source_str = list_item.find("span", class_="label site").getText().strip()

        #source_url
        source_url = url + list_item.find("a", class_="product-link").get("href")

        #comment_cnt, up_cnt, down_cnt
        cnt_trigger = [0,0,0]
        comment_tag = list_item.find_all("small", class_="text-muted")
        is_comment = comment_tag[1].find("i", class_="fa fa-commenting-o fa-fw")
        is_up = comment_tag[1].find("i",class_="fa fa-thumbs-o-up fa-fw")
        is_down = comment_tag[1].find("i",class_="fa fa-thumbs-o-down fa-fw")

        cnt_list = comment_tag[1].getText().split()
        #result [comment , up, down]
        result_cnt = []
        if is_comment == None:
            cnt_trigger[0] = 0
            result_cnt.append("comment 없음")
        else:
            cnt_trigger[0] = 1
            result_cnt.append(cnt_list[0])
            cnt_list.pop(0)
        if is_up == None:
            cnt_trigger[1] = 0
            result_cnt.append("up 없음")
        else:
            cnt_trigger[1] = 1
            result_cnt.append(cnt_list[0])
            cnt_list.pop(0)
        if is_down==None:
            cnt_trigger[2] = 0
            result_cnt.append("down 없음")
        else:
            cnt_trigger[2] = 1
            result_cnt.append(cnt_list[0])
            cnt_list.pop(0)


        comment_cnt = result_cnt[0]
        up_cnt = result_cnt[1]
        down_cnt = result_cnt[2]


        #list_tuple(이름, 가격, 시간, 이미지url, market str, source str, source url, comment-cnt, up-cnt,down-cnt)
        list_tuple = (product_name,price,time,img_url,market_str,source_str,source_url, comment_cnt, up_cnt, down_cnt)
        list_items.append(list_tuple)

    return list_items


def _detect_input(text):
    compile_txt = re.compile(r'\d+개')
    digit_txt_list = compile_txt.findall(text)

    result = ""

    if re.search('핫딜', text) and re.search('인기',text):
        return "핫딜 중에서 인기 많은거 보여줌"
    elif re.search('추천', text) or re.search('살만한', text):
        return "살만한 물건 추천"
    elif re.search('최저가', text) or re.search('변동추이', text) or re.search('변동',text):
        return "최저가(그래프보여주기)"
    elif re.search('도움', text) or re.search('help', text) or re.search('옵션', text) or re.search('option', text):
        return "도움말"
    else:
        if len(digit_txt_list) > 1:
            result = Json_parser.jsonCreater(_crawl_listitem(int(5)))
            return result
        elif len(digit_txt_list) == 1:
            digit_filter = re.compile(r'\d+')
            digit = digit_filter.findall(digit_txt_list[0])
            result = Json_parser.jsonCreater(_crawl_listitem(int(digit[0])))
            return result



# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    global check_pre_msg, check_pre_time
    _channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]


    if check_pre_time==None and check_pre_msg=="":
        print("First call")
        check_pre_time = datetime.datetime.now()
        check_pre_msg = str(text).split()[1:]

        slack_web_client.chat_postMessage(
            channel=_channel,
            text="First call",
            blocks=_detect_input(text)
        )

        return None

    called_time = datetime.datetime.now()

    #print(check_pre_time, called_time, (called_time - check_pre_time).total_seconds())

    if check_pre_msg != str(text).split()[1:]:
        print("After call", check_pre_msg, str(text).split()[1:], (called_time - check_pre_time).total_seconds())
        slack_web_client.chat_postMessage(
            channel=_channel,
            text="After call" + str(text),
            blocks=_detect_input(text)
        )
        check_pre_msg = str(text).split()[1:]

        return None

    if check_pre_msg == str(text).split()[1:] and (called_time - check_pre_time).total_seconds() > 60:
        print("Over 60sec call", check_pre_msg, str(text).split()[1:],
              (called_time - check_pre_time).total_seconds())

        check_pre_time = called_time
        slack_web_client.chat_postMessage(
            channel=_channel,
            text="Over 60sec" + str(text),
            blocks=_detect_input(text)
        )

        return None

    if check_pre_msg == str(text).split()[1:] and (called_time - check_pre_time).total_seconds() < 60:
        print("Same msg", check_pre_msg, str(text).split()[1:], (called_time - check_pre_time).total_seconds())
        slack_web_client.chat_postMessage(
            channel=_channel,
            text="*중복된 메시지를 보내시면 안되요.*"
        )
        return None


@app.route("/click", methods=["GET", "POST"])
def on_button_click():
    # 버튼 클릭은 SlackEventsApi에서 처리해주지 않으므로 직접 처리합니다
    payload = request.values["payload"]
    click_event = MessageInteractiveEvent(json.loads(payload))

    keyword = click_event.block_id
    item_name = click_event.value
    result = VitualEnv.get_6m_price_change_from_naver(item_name)


    if (result[0]):
        slack_web_client.chat_postMessage(
            channel=click_event.channel.id,
            text="저희가 선택하신 제품과 가장 유사한 제품의 가격변동 추이에요.\n 선택제품: {0} | 검색된 제품: {1}\n".format(item_name, result[1])
        )
        slack_web_client.files_upload(channels=click_event.channel.id, file=result[2])
    else:
        slack_web_client.chat_postMessage(
            channel=click_event.channel.id,
            text=result[1]
        )

    return "OK", 200



# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=4040)

