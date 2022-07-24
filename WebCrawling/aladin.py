import requests
from bs4 import BeautifulSoup


def get_bestsellers() -> list:
    result = []
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&start=we"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    index = 0
    for book in soup.select(".ss_book_box"):
        index += 1
        book_dict = {}
        book_dict["rank"] = index
        book_dict["title"] = book.select_one("b").text
        rawdata = book.select_one(".ss_book_list > ul > li:nth-child(3)").text
        if "할인" in rawdata:
            rawdata = book.select_one(".ss_book_list > ul > li:nth-child(2)").text
        book_dict["writer"] = rawdata.split("|")[0].strip()
        book_dict["publisher"] = rawdata.split("|")[1].strip()
        book_dict["release_date"] = rawdata.split("|")[2].strip()
        result.append(book_dict)
    return result


if __name__ == "__main__":
    book_data = get_bestsellers()
    for book in book_data:
        print(book)
