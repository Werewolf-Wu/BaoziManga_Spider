from lxml import etree
from cookies_and_headers import cookies, headers


# def get_jpg_list(url,client) -> list:
#     r = client.get(url,cookies=cookies,headers=headers)
#     html = etree.HTML(r.content)
#     resu_list_raw = list(html.xpath('//amp-img/@src'))
#     resu_list = list(filter(lambda x:x.find("scomic") != -1,resu_list_raw))
#     return resu_list


def get_jpg_list(url, client, session) -> list:
    post_body = {"cmd": "request.get", "url": url, "maxTimeout": 60000}

    if session == None:
        r = client.post(
            "http://127.0.0.1:8191/v1",
            cookies=cookies,
            headers=headers,
            json=post_body,
            timeout=None,
        )
    else:
        post_body = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000,
            "session": session,
        }
        r = client.post(
            "http://127.0.0.1:8191/v1",
            cookies=cookies,
            headers=headers,
            json=post_body,
            timeout=None,
        )
    response = (r.json())["solution"]["response"]
    html = etree.HTML(response)
    resu_list_raw = list(html.xpath("//amp-img/@src"))
    resu_list = list(filter(lambda x: x.find("scomic") != -1, resu_list_raw))
    return resu_list


# 重写，因为接入flaresolverr

# 再次重写，尝试利用flaresolverr的solution


def get_jpg_list_rewrite(url, client, solv):
    cookies = solv["cookies"]
    clean_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}
    headers = {"User-Agent": solv["userAgent"]}
    r = client.get(
        url=url, cookies=clean_cookies, headers=headers, follow_redirects=True
    )
    html = etree.HTML(r.text)
    resu_list_raw = list(html.xpath("//amp-img/@src"))
    resu_list = list(filter(lambda x: x.find("scomic") != -1, resu_list_raw))
    return resu_list
