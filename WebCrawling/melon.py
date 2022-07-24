import requests
import bs4
import json
import pandas as pd


def get_melon_chart(is_global=False) -> list:
    """
    멜론 차트를 반환합니다.
    :param is_global: 해외 종합 차트를 요청 (기본값 False, 국내 종합 차트)
    """
    result = []
    url = "https://www.melon.com/chart/day/index.htm?classCd=" + (
        "AB0000" if is_global else "DM0000"
    )  # 국내 차트는 DM0000, 해외 차트는 AB0000
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    songs = soup.select("#frm table tbody tr")
    for song in songs:
        song_dict = {}
        song_dict["rank"] = int(song.select_one("span.rank").text.strip())
        song_dict["title"] = song.select_one(".rank01 > span > a").text
        song_dict["artist"] = song.select_one(".rank02 > a").text
        song_dict["album"] = song.select_one(".rank03 > a").text
        song_dict["albumart"] = (
            song.select_one(".image_typeAll > img")
            .get("src")
            .replace("resize/120", "resize/300")
        )  # 이미지 사이즈를 300px로 변경
        result.append(song_dict)
    likes_data = get_likes([song.attrs["data-song-no"] for song in songs])
    for i in range(len(result)):
        result[i]["likes"] = likes_data[i]
    return result


def get_likes(song_numbers) -> int:
    """
    음원 번호 목록으로 좋아요 수 목록을 반환합니다.
    """
    result = []
    url = "https://www.melon.com/commonlike/getSongLike.json"
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        params={"contsIds": ",".join(song_numbers)},
    )
    json_data = json.loads(response.text)
    for i in json_data["contsLike"]:
        result.append(i["SUMMCNT"])
    return result


if __name__ == "__main__":
    print("국내 TOP 100 (5개판 표시)")
    kr_chart = get_melon_chart()
    for song in kr_chart[:5]:
        print(song)
    df = pd.DataFrame(kr_chart)
    df.to_csv("melon_chart_kr.csv", index=False)
    print("CSV 파일 저장 완료")
    print("=" * 20)

    print("해외 TOP 100 (5개판 표시)")
    global_chart = get_melon_chart(is_global=True)
    for song in global_chart[:5]:
        print(song)
    df = pd.DataFrame(global_chart)
    df.to_csv("melon_chart_global.csv", index=False)
    print("CSV 파일 저장 완료")
    print("=" * 20)
