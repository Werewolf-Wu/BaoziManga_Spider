from lxml import etree
from cookies_and_headers import cookies, headers

# def get_chap_dict(homep,client):
#     response = client.get(homep, cookies=cookies, headers=headers)
#     url_prefix = r"https://cn.baozimh.com"
#     html = etree.HTML(response.text)
#     result_pages = html.xpath("//a[@class='comics-chapters__item']/@href")
#     result_names = html.xpath("//a[@class='comics-chapters__item']//span/text()")
#     result_pages = [url_prefix + i for i in result_pages]
#     resp = dict(zip(result_names,result_pages))
#     return resp
# 重写，因为接入flaresolverr

post_body = {
    "cmd": "request.get",
    "url": "https://www.petsathome.com/",
    "maxTimeout": 60000,
}


def get_chap_dict(homep, client, session):
    post_body = {"cmd": "request.get", "url": homep, "maxTimeout": 60000}
    if session == None:
        response_raw = client.post(
            "http://127.0.0.1:8191/v1",
            cookies=cookies,
            headers=headers,
            json=post_body,
            timeout=None,
        )
    else:
        post_body = {
            "cmd": "request.get",
            "url": homep,
            "maxTimeout": 60000,
            "session": session,
        }
        response_raw = client.post(
            "http://127.0.0.1:8191/v1",
            cookies=cookies,
            headers=headers,
            json=post_body,
            timeout=None,
        )
    response = (response_raw.json())["solution"]["response"]
    url_prefix = r"https://cn.baozimh.com"
    html = etree.HTML(response)
    result_pages = html.xpath("//a[@class='comics-chapters__item']/@href")
    result_names = html.xpath("//a[@class='comics-chapters__item']//span/text()")
    result_pages = [url_prefix + i for i in result_pages]
    resp = dict(zip(result_names, result_pages))
    challengesolve = (response_raw.json())["solution"]

    return resp, challengesolve
