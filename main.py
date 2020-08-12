# -*- coding: utf-8 -*
import asyncio

from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import os


def cover_list(up: str) -> list:
    key = "AIzaSyCOs6EnXVhUCYc_loPpJXjGx7xmoUFTEQM"
    api_url = f"https://www.googleapis.com/youtube/v3/search?" \
              f"key={key}&" \
              f"channelId={up}&" \
              f"part=snippet,id&" \
              f"order=date&" \
              f"maxResults=1000"
    json = eval(urlopen(api_url).read().decode("utf-8"))
    try:
        while True:
            api_url_next = api_url + "&pageToken=" + json["nextPageToken"]
            for i in json["items"]:
                videoId = i["id"]["videoId"]
                yield f"https://www.youtube.com/watch?v={videoId} "
            json = eval(urlopen(api_url_next).read().decode("utf-8"))
    except KeyError:
        exit(0)


async def cover_download(video_name: str, streamTime: str):
    cover_link = f"https://img.youtube.com/vi/{video_name}/maxresdefault.jpg"
    time = 0
    data = None
    ifRequest = False

    while not ifRequest and time < 5:
        try:
            data = requests.get(cover_link).content
            ifRequest = True
        except (TypeError, AttributeError):
            print("封面链接失败，尝试重新连接")
            time += 1

    if not ifRequest:
        with open("error_message.txt", "a+") as file:
            file.write(video_name + " cover error\n")
            file.close()
        return None

    with open(f"buffer/{video_name}.jpg", "wb") as code:
        code.write(data)
        code.close()

    with open(f"covers/{streamTime}.jpg", "wb") as code:
        code.write(data)
        code.close()


async def video_info(video_link: str, up: str):
    time = 0
    date = None
    soup = None
    if_requested = False
    find_uploader = None

    while not if_requested and time < 5:
        try:
            website = urlopen(video_link).read().decode("utf-8")
            soup = BeautifulSoup(website, "lxml")
            date = soup.find('meta', {'itemprop': 'startDate'})
            find_uploader = soup.find('meta', {'itemprop': 'channelId'})['content']
            print(find_uploader)
            if_requested = True
        except AttributeError:
            print("视频信息链接失败，尝试重新连接")
            time += 1

    if not if_requested:
        with open("error_message.txt", "a+") as file:
            file.write(video_link + " message error\n")
            file.close()
        return None

    if find_uploader != up:
        return None

    if date:
        date = date['content'].replace('T', ' ').replace('+00:00', '')
        print(date)
    else:
        date = soup.find('meta', {'itemprop': 'datePublished'})
        date = date['content'] + " 00:00:00"
        print(date)
    return date


async def main():
    uploader = "UCdn5BQ06XqgXoAxIhbqw5Rg"
    if not os.path.exists("buffer"):
        os.mkdir("buffer")
    if not os.path.exists("covers"):
        os.mkdir("covers")

    for link in cover_list(uploader):
        try:
            name = link.replace("https://www.youtube.com/watch?v=", "")
        except AttributeError:
            print("列表为空，程序结束")
            break

        if os.path.exists(f"buffer/{name}.jpg"):
            print("该图片已经存在")
            continue

        date = await video_info(link, uploader)
        if date:
            await cover_download(name, date)
        else:
            continue


if __name__ == "__main__":
    asyncio.run(main())
    # cover_list("UCdn5BQ06XqgXoAxIhbqw5Rg")
