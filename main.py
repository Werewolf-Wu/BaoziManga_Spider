import grequests
from one_chap_jpg_lists import get_jpg_list, get_jpg_list_rewrite
from get_chap_list import get_chap_dict
import httpx
import pathlib

params = {
    "cmd": "sessions.create",
    "session": "1",
}

httpx.post("http://127.0.0.1:8191/v1", json=params)


class manga:
    # abab = httpx.Client(http2=True)
    def __init__(self, homepage_url):
        self.homepage_url = homepage_url
        self.chap_dict = {}
        self.chap_link_dict = {}
        self.client = httpx.Client()
        self.resu = {}
        # self.client = client

    def get_chapter_dict(self):
        self.chap_dict, self.solv = get_chap_dict(
            homep=self.homepage_url, client=self.client, session="1"
        )

    def get_pages_by_chapter(self):
        client = httpx.Client()
        for chapname, chaplink in self.chap_dict.items():
            # self.chap_link_dict[chapname] = get_jpg_list(chaplink,client=self.client, session = "1")
            self.chap_link_dict[chapname] = get_jpg_list_rewrite(
                chaplink, client=client, solv=self.solv
            )

    def get_page_files(self):
        cwd_path = pathlib.Path().cwd()
        manga_home_directory = cwd_path / self.homepage_url.split("/")[-1]
        for chapname, pagelinklist in self.chap_link_dict.items():
            rs = [grequests.get(link) for link in pagelinklist]
            resu = grequests.map(rs)
            for i in resu:
                pathtochapter = manga_home_directory / chapname
                pathtochapter.mkdir(parents=True, exist_ok=True)
                with open(
                    manga_home_directory / chapname / (i.url.split("/")[-1]), "wb"
                ) as f:
                    f.write(i.content)
