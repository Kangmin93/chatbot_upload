import json

from collections import OrderedDict

# def json_default(value):
#     if isinstance(value, datetime.date):
#         return value.strftime('%Y-%m-%d')
#     raise TypeError('not JSON serializable')
#
# data = {'date': datetime.date.today()}
# json_data = json.dumps(data, default=json_default)
def jsonify(data):
    return json.loads(data.replace("'", '"'))

def jsonCreater(itemlist):
    jsonList = []
    seletion_list = []

    file_data = OrderedDict()
    file_data["type"] = "section"
    file_data["text"] = {
        "type": "mrkdwn",
        "text": "요청하신 " + str(len(itemlist)) + "개의 핫딜입니다.\n\n *아이템 목록:*"
    }
    jsonList.append(file_data)

    file_data = OrderedDict()
    file_data["type"] = "divider"
    jsonList.append(file_data)

    for i in range(len(itemlist)):
        # for selection panel
        seletion_item = OrderedDict()

        seletion_item["text"] = {
            "type": "plain_text",
            "text": itemlist[i][0] if len(itemlist[i][0]) < 20 else itemlist[i][0][:20],
        }
        seletion_item["value"] = itemlist[i][0]
        seletion_list.append(seletion_item)

        file_data = OrderedDict()
        #file_data["title"] = itemlist[i][0] if len(itemlist[i][0]) < 20 else itemlist[i][0][:20]
        file_data["type"] = "section"
        file_data["text"] = {
            "type": "mrkdwn",
            "text": "*<" + itemlist[i][6] + "|" + itemlist[i][0]+">*\n"

        }
        #file_data["url"] = itemlist[i][5]
        if(itemlist[3] != "None"):
            file_data["accessory"] = {
                "type" : "image",
                "image_url" : itemlist[i][3],
                "alt_text" : "이미지 파일\n X",
            }
        else:
            file_data["accessory"] = {
                "type": "image",
                "image_url": "https://static.thenounproject.com/png/340719-200.png",
                "alt_text": "이미지 파일\n X"
            }
        jsonList.append(file_data)

    file_data = OrderedDict()
    file_data["type"] = "divider"
    jsonList.append(file_data)

    file_data = OrderedDict()
    file_data["type"] = "section"
    file_data["text"] = {
        "type": "mrkdwn",
        "text": "최저가 변동 추이를 보고 싶은 핫딜을 선택하세요."
    }

    file_data["accessory"] = {
        "type": "static_select",
        "placeholder": {
            "type": "plain_text",
            "text": "Select an item",
            "emoji": True
        },
        "options": seletion_list
    }
    jsonList.append(file_data)

    result = json.dumps(jsonList, ensure_ascii=False, indent="\t")
    #result = str(jsonify(result))
    return json.loads(result)#.replace("'", '"')

def formatting_msg():
    testList = [
        ("lg 그램", "123456", "2019-07-11",
         "https://s3.ap-northeast-2.amazonaws.com/algumon/%EB%BD%90%EB%BF%8C-%EC"
         "%9D%BC%EB%B0%98/1_470D6178427F4FD2B5B02CD9A9724DA6.jpg",
         "11번가", "뽐뿌", "https://www.ppomppu.co.kr/", "10", "3", "4"),
        ("lg 그램", "123456", "2019-07-11",
         "https://s3.ap-northeast-2.amazonaws.com/algumon/%EB%BD%90%EB%BF%8C-%EC"
         "%9D%BC%EB%B0%98/1_470D6178427F4FD2B5B02CD9A9724DA6.jpg",
         "11번가", "뽐뿌", "https://www.ppomppu.co.kr/", "10", "3", "4"),
        ("lg 그램", "123456", "2019-07-11",
         "https://s3.ap-northeast-2.amazonaws.com/algumon/%EB%BD%90%EB%BF%8C-%EC"
         "%9D%BC%EB%B0%98/1_470D6178427F4FD2B5B02CD9A9724DA6.jpg",
         "11번가", "뽐뿌", "https://www.ppomppu.co.kr/", "10", "3", "4"),
        ("lg 그램", "123456", "2019-07-11",
         "https://s3.ap-northeast-2.amazonaws.com/algumon/%EB%BD%90%EB%BF%8C-%EC"
         "%9D%BC%EB%B0%98/1_470D6178427F4FD2B5B02CD9A9724DA6.jpg",
         "11번가", "뽐뿌", "https://www.ppomppu.co.kr/", "10", "3", "4"),
        ("lg 그램", "123456", "2019-07-11",
         "https://s3.ap-northeast-2.amazonaws.com/algumon/%EB%BD%90%EB%BF%8C-%EC"
         "%9D%BC%EB%B0%98/1_470D6178427F4FD2B5B02CD9A9724DA6.jpg",
         "11번가", "뽐뿌", "https://www.ppomppu.co.kr/", "10", "3", "4"),
    ]

    result = jsonCreater(testList)
    #print(result)
    #print(type(result))
    return result

#formatting_msg()