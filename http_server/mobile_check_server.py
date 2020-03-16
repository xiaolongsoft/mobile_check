import re

import bs4
import tornado.ioloop as loop
import tornado.web as server
from selenium import webdriver  # 用来驱动浏览器的


class MainHandler(server.RequestHandler):

    def get(self):
        """get请求"""
        url = self.get_argument('url')
        chrome = self.inint_browser()
        result = self.do_check(url, chrome)
        image = self.get_html_image(chrome)
        self.write(str(url) + '::===>>' + result+"image64::===>data:image/jpg;base64,"+image)

    def inint_browser(self):
        # 2.选择让谷歌模拟的设备
        mobileEmulation = {"deviceName": "iPhone X"}
        # 3.将设备加入到浏览器
        # 实例化谷歌浏览器加载项
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", mobileEmulation)
        options.add_argument('headless')
        chrome = webdriver.Chrome(options=options)
        return chrome

    # 访问给定的网址，抓取页面数据
    def do_check(self, url, chrome):

        try:
            chrome.get(url)
            html = chrome.execute_script('return document.documentElement.outerHTML')

            return self.mobile_check(html)
        except:
            print("访问不到页面啊。")
            return False

    ##检查页面是否支持移动化
    def mobile_check(self, html):
        searchSoup = bs4.BeautifulSoup(html, features="html.parser")
        # 1.网站自适应标志
        imgs =  searchSoup.select("img ")
        for m in imgs:
            print(m.get('src'))

        elements = searchSoup.select('meta[name="viewport"]')
        if len(elements) > 0:
            return "true"

        # 2 .富门户移动化过的标志
        fmhmark = searchSoup.find_all(src=re.compile("http://gmwz-1251053291.file.myqcloud.com/"))

        if len(fmhmark) > 0:
            return "true"

        return "false"
    def get_html_image(self,chrome):
        return chrome.get_screenshot_as_base64()


#启动服务  监听mobile_check路径
application = server.Application([(r"/mobile_check", MainHandler), ])

if __name__ == "__main__":
    application.listen(18114)
    loop.IOLoop.instance().start()
