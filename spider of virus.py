# provinceShortName
import json
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class VirusSpider(object):

    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def get_content_form_url(self, url):
        '''
        1.发送请求,返回字符串
        :param url: __init__中的url
        :return:字符串
        '''
        response = requests.get(url)
        return response.content.decode()

    def pars_home_page(self, home_page, tag_id):
        # 获取内容，解析数据
        # 2.根据标签什么的提取数据
        soup = BeautifulSoup(home_page, 'lxml')
        script = soup.find(id=tag_id)
        # script.text不能用
        text_string = script.string
        # 3.使用正则表达式 提取字符串
        json_str = re.findall(r'\[.+\]', text_string)[0]
        # 4.json->python
        data = json.loads(json_str)
        return data

    def save(self, data, path):
        # 5.python->json.text
        with open(path, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False)

    def golbal_last_day_virus(self):
        home_page = self.get_content_form_url(self.home_url)
        self.save(self.pars_home_page(home_page, 'getListByCountryTypeService2true'), 'golbal_last_day_virus.json')

    def days_virus_golbal(self):
        with open('golbal_last_day_virus.json', encoding='utf-8') as fp:
            last_day_virus = json.load(fp)
        corona_virus = []
        # tqdm其实还可以复用
        for city in tqdm(last_day_virus, '采集1月23日以来的各国疫情信息'):
            city_url = city['statisticsData']
            city_url_data_json = self.get_content_form_url(city_url)
            data = json.loads(city_url_data_json)['data']
            for one_day in data:
                one_day['provinceName'] = city['provinceName']
            corona_virus.extend(data)
        self.save(corona_virus, 'days_virus_golbal.json')

    def run(self):
        self.golbal_last_day_virus()
        # self.days_virus_golbal()


if __name__ == '__main__':
    spider = VirusSpider()
    spider.run()
