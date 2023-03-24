from MyLogger.MyLogger import MyLogger
import urllib
import bs4
from SoupMaker import SoupMaker


def main():
    logger = MyLogger("URL_Getter")
    domain = "https://sv.bagoum.com"
    soupMaker = SoupMaker()
    soup = soupMaker.makeSoup("https://sv.bagoum.com/cardSort")
    a_tags = soup.select("a")
    url_list = []
    for a_tag in a_tags:
        href = a_tag.get("href")
        if "/cards/" in href:
            url_list.append(domain + href + "\n")

    with open("url_links.txt", "w", encoding="utf-8") as f:
        f.writelines(url_list, )


if __name__ == "__main__":
    main()
