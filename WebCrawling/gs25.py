import requests
import json
import bs4
import pandas as pd

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"


def get_gs25_prd_list() -> list:
    """
    GS25 행사 상품 목록을 반환합니다.
    """
    result = []
    url = "https://gs25.gsretail.com/gscvs/ko/products/event-goods-search"
    params = {
        "pageNum": "1",
        "pageSize": "1500",
        "searchType": "",
        "searchWord": "",
        "parameterList": "TOTAL",
    }
    response = requests.get(url, params=params, headers={"User-Agent": USER_AGENT})
    json_data = json.loads(json.loads(response.text))
    for i in json_data["results"]:
        if i["goodsStatNm"] == "정상":
            prd_dict = {}
            prd_dict["name"] = i["goodsNm"]
            prd_dict["img"] = i["attFileNm"].replace("http", "https")
            prd_dict["price"] = int(i["price"])
            prd_dict["event_type"] = i["eventTypeNm"]
            if i["eventTypeNm"] == "1+1":
                prd_dict["event_price"] = int(int(i["price"]) / 2)
            elif i["eventTypeNm"] == "2+1":
                prd_dict["event_price"] = int(int(i["price"]) * 2 / 3)
            elif i["eventTypeNm"] == "덤증정":
                prd_dict["event_price"] = "덤증정"
                prd_dict["event_gift_name"] = (
                    i["giftGoodsNm"] if "giftGoodsNm" in i else ""
                )
                prd_dict["event_gift_price"] = (
                    int(i["giftPrice"]) if "giftPrice" in i else ""
                )
                prd_dict["event_gift_count"] = (
                    int(i["giftCount"]) if "giftCount" in i else ""
                )
            else:
                prd_dict["event_price"] = "해당없음"
            result.append(prd_dict)
    return result


def get_auth_info() -> dict:
    """
    CSRF 토큰과 JSP 세션 ID를 반환합니다.

    근데 행사 상품 목록 그냥 get 방식으로 호출하니까 그냥 되네요.
    post로 호출하면 토큰이랑 세션 ID 없이는 안 되던데.
    무슨 이런 사이트가 다 있나...
    """
    url = "http://gs25.gsretail.com/products/event-goods"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "CSRFToken"})["value"]
    jsessionid = response.cookies["JSESSIONID"]
    return {"csrf_token": csrf_token, "jsession_id": jsessionid}


if __name__ == "__main__":
    prd_list = get_gs25_prd_list()
    print("GS25 행사상품 총 {}개 수신".format(len(prd_list)))
    df = pd.DataFrame(prd_list)
    df.to_csv("gs25_prd_list.csv", index=False)
    print("CSV 파일 저장 완료 :)")
