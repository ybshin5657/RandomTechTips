import csv
import json
import requests


def get_stocks() -> dict:
    result = []
    for i in range(1, 40):
        url = "https://m.stock.naver.com/api/stocks/marketValue/KOSPI?page=" + str(i) + "&pageSize=50"
        res = requests.get(url)
        json_data = json.loads(res.text)
        for stock in json_data["stocks"]:
            stock_dict = {}
            code = stock["itemCode"]
            name = stock["stockName"]
            price = int(stock["closePrice"].replace(",", ""))

            stock_dict['itemCode'] = code
            stock_dict['stockName'] = name
            stock_dict['closePrice'] = price
            result.append(stock_dict)
    return result


if __name__ == '__main__':
    stockList = get_stocks()
    for stock in stockList:
        print(stock)
    print(len(stockList))

    with open('old/stockList.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, ["itemCode", "stockName", "closePrice"])
        dict_writer.writeheader()
        dict_writer.writerows(stockList)
