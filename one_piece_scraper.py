import requests
from bs4 import BeautifulSoup
import json
import notion_df
import pandas as pd

url = "https://www.animefillerguide.com/2019/06/one-piece-filler-list.html"
html = requests.get(url)

soup = BeautifulSoup(html.content, "html.parser")

filler_episode_list = []
for filler in soup.find_all(class_="red"):
    try:
        filler_episode_list.append(int(filler.get_text().split(".")[0]))
    except:
        continue

mixed_episode_list = []
for filler in soup.find_all(class_="blue"):
    try:
        mixed_episode_list.append(int(filler.get_text().split(".")[0]))
    except:
        continue

it = 0
i = 1
arc_based_episodes = {}
for arc in soup.find_all("h4"):
    episodes = {}
    for episode in soup.find_all("ul")[it]:
        episode_details = {}
        try:
            if (i in filler_episode_list):
                episode_details["title"] = episode.get_text().split('"')[1]
                episode_details["type"] = "filler"
                episodes[i] = episode_details
            elif (i in mixed_episode_list):
                episode_details["title"] = episode.get_text().split('"')[1]
                episode_details["type"] = "mixed"
                episodes[i] = episode_details
            else:
                episode_details["title"] = episode.get_text().split('"')[1]
                episode_details["type"] = "canon"
                episodes[i] = episode_details
            i += 1
        except IndexError:
            continue
    it += 1
    arc_based_episodes[arc.get_text()] = episodes

episodes = []
titles = []
types = []
arcs = []
for arc, arc_details in arc_based_episodes.items():
    for episode_number, episode_details in arc_details.items():
        episodes.append(episode_number)
        arcs.append(arc)
        for key, value in episode_details.items():
            if(key == "title"):
                titles.append(value)
            elif(key == "type"):
                types.append(value)

df = pandas.DataFrame()
df["Episode"] = episodes
df["Title"] = titles
df["Type"] = types
df["Arc"] = arcs

notion_df.upload(df, notion_page_url, title="One Piece", api_key=api_key)