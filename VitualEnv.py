from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import urllib.request


def get_6m_price_change_from_naver(item_name):
    selected_item_name = ""

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")



    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://shopping.naver.com/")
    assert "네이버쇼핑" in driver.title
    elem = driver.find_element_by_name("query")
    elem.send_keys(item_name)
    elem.send_keys(Keys.RETURN)
    driver.implicitly_wait(3)
    try:
        grouped_item = driver.find_element_by_xpath("//li[@class='_model_list _itemSection']")
    except Exception as e:
        # print(e)
        error_msg = u"요청하신 [" + item_name + u"]에 대한 가격 변동 정보가 존재하지 않아요.ㅠㅠ"
        print(error_msg)
        return (False, error_msg)
    else:
        if grouped_item is not None:
            selected_item_name = driver.find_element_by_xpath("//li[@class='_model_list _itemSection']/div/a[@class='tit']").text

            elem = driver.find_element_by_xpath("//li[@class='_model_list _itemSection']/div/a[@class='tit']")
            elem.click()

            url = elem.get_attribute('href')

            source_code = urllib.request.urlopen(url).read().decode('utf-8')

            pos1 = source_code.find("priceChartHandler=shop.detail.HistoryChartHandler")
            pos2 = source_code.find("var countChartHandler=shop.detail.HistoryChartHandler")
            mod_source_code = source_code[pos1:pos2]

            price_list = mod_source_code.split(',')[2].split('|')
            price_list = list(map(lambda x: int(x.replace('"', "").replace(';', "").replace(')', "")), price_list))

            date_list = mod_source_code.split(',')[1].split('|')
            date_list = list(map(lambda x: float(x.replace('"', "").replace(';', "").replace(')', "")), date_list))

            six_month_row_price = []
            for i in range(13):
                six_month_row_price.append((date_list[35 + i * 12], price_list[35 + i * 12]))

            graph_plot(six_month_row_price, selected_item_name)
        return (True, selected_item_name, 'plot.png')

def graph_plot(raw_data, item_name):
    pos = range(len(raw_data))

    font = fm.FontProperties(fname='./NanumBarunGothic.ttf')
    plt.title("[" + str(item_name) + "]의 최근 6개월 간 최저가", fontproperties=font)
    plt.plot(pos, [data[1] for data in raw_data], 'rs--')
    plt.xticks(pos, [str(data[0]) for data in raw_data], fontproperties=font)
    plt.xlabel("날짜", fontproperties=font)
    plt.ylabel("가격", fontproperties=font)
    plt.tight_layout()
    plot_filename = 'plot.png'
    plt.savefig(plot_filename)

    plt.show()
