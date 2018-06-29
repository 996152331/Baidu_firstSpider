# coding=utf-8

import codecs


class DataOutput(object):

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        with open('baike.html', 'w', encoding='utf-8') as file:
            file.write("<html>")
            file.write("<body>")
            file.write("<p>爬取百度百科</p>")
            file.write("<table border='1'>")
            for data in self.datas:
                file.write("<tr>")
                file.write("<td>%s</td>" % data['url'])
                file.write("<td>%s</td>" % data['title'])
                file.write("<td>%s</td>" % data['summary'])
                file.write("</tr>")
            file.write("</table>")
            file.write("</body>")
            file.write("</html>")

