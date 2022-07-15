import requests, bs4, json

def getReviews(movieNo) -> list:
    """
    영화의 리뷰 10개를 반환하는 함수
    """
    result = []
    url = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?onlyActualPointYn=Y&code=" + str(movieNo)
    soup = bs4.BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')
    reviews = soup.select("div > div > div.score_result > ul > li")

    for review in reviews:
        reviewDict = {}
        score = review.select_one("div.star_score > em").text
        content = review.select_one("div.score_reple > p > span:not(.ico_viewer)").text.strip()
        writer = review.select_one("div.score_reple > dl > dt > em:nth-child(1) > a > span").text.strip()
        date = review.select_one("div.score_reple > dl > dt > em:nth-child(2)").text.strip()
        reviewDict['score'] = score
        reviewDict['content'] = content
        reviewDict['writer'] = writer
        reviewDict['date'] = date
        result.append(reviewDict)
    return result

def getMovies() -> list:
    """
    네이버 박스오피스 영화 리스트를 반환하는 함수
    """
    url = "https://movie.naver.com/movieChartJson.naver?type=BOXOFFICE"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://movie.naver.com/'
    }
    response = requests.get(url, headers=headers)
    jsonData = json.loads(response.text)
    result = []
    rank = 1
    for movie in jsonData["movieChartList"]["BOXOFFICE"]:
        movieDict = {}
        code = movie["movieCode"]
        title = movie["movieTitle"]
        img = "https://movie-phinf.pstatic.net/" + movie["posterImageUrl"]
        
        movieDict['rank'] = rank
        movieDict['title'] = title
        movieDict['code'] = code
        movieDict['url'] = "https://movie.naver.com/movie/bi/mi/basic.naver?code=" + str(code)
        movieDict['img'] = img
        movieDict['reviews'] = getReviews(code)
        rank += 1
        result.append(movieDict)
    return result

#print(json.dumps(getMovies(), ensure_ascii=False))

