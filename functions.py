import re


def extractor(items):
    links = []
    for item in items:
        link = item.find('a').get('href')
        link = re.sub('&sa=U.*', '', re.sub('/url\\?q=', '', link))
        links.append(link)
    return links



