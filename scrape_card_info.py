from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from pathlib import Path
from time import sleep
from SoupMaker import SoupMaker  # type: ignore
import urllib.request
import requests  # type: ignore
from typing import Dict, Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import card_data

BASE_PATH = Path(__file__).parent
KEY_TYPE = "Type"
KEY_RARITY = "Rarity"
KEY_SET = "Set"
KEY_CV = "CV"
KEY_COST = "Cost"
KEY_BASE_STATS = "BaseStats"
KEY_BASE_EFFECT = "BaseEffect"
KEY_EVOLVED_STATS = "EvolvedStats"
KEY_EVOLVED_EFFECT = "EvolvedEffect"


def main():
    service = fs.Service(str(Path(BASE_PATH, "chromedriver")))
    driver = webdriver.Chrome(service=service)
    soup_maker = SoupMaker()
    print("-----------")
    driver.get("https://sv.bagoum.com/cards/111741030")
    driver.execute_script("changeLocale('ja');")
    sleep(10)
    scrape_card("https://sv.bagoum.com/cards/111741030", driver, soup_maker)


def scrape_card(url: str, driver: WebDriver, soup_maker: SoupMaker):
    driver.get(url)
    sleep(1)
    driver.execute_script("changeLocale('ja');")
    soup = soup_maker.makeSoupFromHtml(driver.page_source)
    description_text = soup.select_one("#cardbody > div.cardPage-cardTextHolder > div:nth-child(1) > p").text
    description_dict = format_description(description_text)
    card_info = card_data.ShadowVerseCard(
        card_data.strToRarity(description_dict[KEY_RARITY]),
        description_dict[KEY_SET],
        description_dict[KEY_CV],
        int(description_dict[KEY_COST])
    )
    print(card_info)
    print(card_info.toDict())
    flavor_text = soup.select_one("#cardbody > div.cardPage-cardTextHolder > div:nth-child(2) > p").text
    print(flavor_text)
    print(format_flavor(flavor_text))
    voice_tr_list = soup.select("#cardbody > div.cardPage-voiceHolder > table > tbody > tr")[1:]

    image_id = driver.current_url.split("/")[-1]

    if len(voice_tr_list) != 0:
        for voice_tr in voice_tr_list:
            td_list = voice_tr.select("td")
            audio_tag = td_list[0].text.strip()
            audio_url = td_list[1].select_one("audio > source").get("src")
            saveAudio(Path(BASE_PATH, "audio"), audio_url, "{}_{}".format(image_id, audio_tag))

    if description_dict[KEY_TYPE] == "Follower":
        save_card_image(driver, image_id)
        save_raw_image(image_id)
        save_evolved_card_image(driver, image_id)
        save_evolved_raw_image(image_id)


def format_description(description_text: str):
    description_text = description_text.replace("Rarity:", "\n" + KEY_RARITY + ":")
    description_text = description_text.replace("Set:", "\n" + KEY_SET + ":")
    description_text = description_text.replace("CV:", "\n" + KEY_CV + ":")
    description_text = description_text.replace("Cost:", "\n" + KEY_COST + ":")
    description_text = description_text.replace("Base:Stats:", "\n" + KEY_BASE_STATS + ":")
    description_text = description_text.replace("Effect:", "\neffect:", 1)
    description_text = description_text.replace("Evolved:Stats:", "\n" + KEY_EVOLVED_STATS + ":", 1)
    description_text = description_text.replace("Effect:", "\n" + KEY_EVOLVED_EFFECT + ":", 1)
    description_text = description_text.replace("effect:", "\n" + KEY_BASE_EFFECT + ":", 1)
    description_list = [i for i in description_text.split("\n") if len(i) != 0]
    description_dict = {i.split(": ")[0]: i.split(": ")[1].replace(" ", "") for i in description_list}
    print(description_dict)
    return description_dict


def format_flavor(flavor_text: str):
    EVOLVED_FLAIR = "EvolvedFlair"
    flavor_text = flavor_text.replace("Base Flair", "")
    flavor_text = flavor_text.replace("\n", "")
    flavor_text = flavor_text.replace(" ", "")
    if EVOLVED_FLAIR not in flavor_text:
        return flavor_text, ""
    else:
        split_text = flavor_text.split(EVOLVED_FLAIR)
        return split_text[0], split_text[1]


def save_card_image(driver: WebDriver, image_code: str):
    image_url = "https://sv.bagoum.com/cardF/ja/c/{}".format(image_code)
    image_name = "{}_c".format(image_code)
    image_path = Path(BASE_PATH, "cardImage", image_name)
    driver.get(image_url)
    img = driver.find_element(By.TAG_NAME, 'img')
    driver.execute_script("arguments[0].style='background: #00FF00;';", img)
    with open(image_path, "wb") as f:
        f.write(img.screenshot_as_png)


def save_evolved_card_image(driver: WebDriver, image_code: str):
    image_path = Path(BASE_PATH, "cardImage")
    image_url = "https://sv.bagoum.com/cardF/ja/e/{}".format(image_code)
    image_name = "{}_e".format(image_code)
    saveImage(image_path, image_url, image_name)


def save_raw_image(image_code: str):
    image_path = Path(BASE_PATH, "rawImage")
    image_url = "https://sv.bagoum.com/getRawImage/0/0/{}".format(image_code)
    image_name = "{}_c".format(image_code)
    saveImage(image_path, image_url, image_name)


def save_evolved_raw_image(image_code: str):
    image_path = Path(BASE_PATH, "rawImage")
    image_url = "https://sv.bagoum.com/getRawImage/1/0/{}".format(image_code)
    image_name = "{}_e".format(image_code)
    saveImage(image_path, image_url, image_name)


def saveImage(path: Path, image_url: str, image_name: str):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
    request = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(request) as web_file:
        data = web_file.read()
        with open(Path(path, "{}.png".format(image_name)), mode='wb') as local_file:
            local_file.write(data)


def saveAudio(path: Path, audio_url: str, audio_name: str):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
    print("https://sv.bagoum.com" + audio_url)
    request = urllib.request.Request("https://sv.bagoum.com" + audio_url, headers=headers)
    with urllib.request.urlopen(request) as web_file:
        data = web_file.read()
        with open(Path(path, "{}.mp3".format(audio_name)), mode='wb') as local_file:
            local_file.write(data)


if __name__ == "__main__":
    main()
