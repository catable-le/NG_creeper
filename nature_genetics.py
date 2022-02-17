# -*- coding: UTF-8 -*-
import urllib2
import re
import pandas as pd


def download():
    table = pd.DataFrame(columns=['标题', '类型', '时间'])
    k = 1
    while k < 293:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        url = 'https://www.nature.com/ng/research-articles?searchType=journalSearch&sort=PubDate&page='+str(k)
        urls = urllib2.Request(url, headers=send_headers)
        html = urllib2.urlopen(urls)
        html_Doc = html.read()
        html.close()

        title = re.findall(r"(<a href=\"/articles/.*?</a>)", html_Doc, re.S)
        type = re.findall(r"(<span class=\"c-meta__type\">.*?</span>)", html_Doc, re.S)
        time = re.findall(r"(<time class=\"c-meta__item c-meta__item--block-at-lg\" .*?</time>)", html_Doc)

        for i in range(0, len(title)):
            if title[i]:
                r = re.findall(r"(data-track-label=\"link\">.*?</a>)", title[i], re.S)
                title1 = r[0].replace('data-track-label=\"link\">','').replace('<i>','').replace('</i>','').replace('</a>','')
                if type:
                    type1 = type[i].replace('<span class=\"c-meta__type\">','').replace('</span>','')
                else:
                    type1 = ''
                if time:
                    t = re.findall(r"(itemprop=\"datePublished\">.*?</time>)", time[i])
                    time1 = t[0].replace('itemprop=\"datePublished\">','').replace('</time>','')
                table = table.append({'标题': title1, '类型': type1, '时间': time1}, ignore_index=True)
        if k == 292:
            print table
            table.to_csv("D:/nature.csv", sep="\t", index=False)
            return table
            break
        else:
            k = k + 1



if __name__ == '__main__':
    table1 = download()
