import requests
import bs4
from urllib.parse import urljoin

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"


def get_categories() -> list:
    result = []
    url = "http://soonnam.com/board/index.php?language=&board=menu_01&sca=2"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    categories = soup.select("#snbWrap > ul > li")
    for category in categories:
        menu_url = category.select_one("a").get("href")
        result.append(urljoin(url, menu_url))
    return result


def get_menus(url=None) -> list:
    result = []
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    sessionid = response.cookies["PHPSESSID"]
    category_name = soup.select_one(".gnb > li.on > a").text
    pages = len(soup.select(".paging > span"))
    for page in range(1, pages + 1):
        response = requests.get(
            url + "&page=" + str(page), headers={"User-Agent": USER_AGENT}
        )
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        menus = soup.select(".menu_list > li")
        for menu in menus:
            menu_dict = {}
            menu_dict["category"] = category_name
            menu_dict["name"] = menu.select_one("h3").text
            img_url = urljoin(url, menu.select_one("img").get("src"))
            img_response = requests.get(
                img_url,
                headers={"User-Agent": USER_AGENT},
                cookies={"PHPSESSID": sessionid},
            )
            img_data = img_response.content
            with open("menu_img/" + "a" + ".jpg", "wb") as f:
                f.write(img_data)

            menu_dict["desc"] = (
                menu.select_one(".menu_desc").text.strip().replace("\n", " - ")
            )
            result.append(menu_dict)
    return result


if __name__ == "__main__":
    menu_list = []
    category_list = get_categories()
    for category in category_list:
        for menu in get_menus(category):
            menu_list.append(menu)
    for menu in menu_list:
        print(menu)
