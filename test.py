import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(BASE_DIR)

with open ("posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

video_posts = data["video_posts"]

for video in video_posts:
    print(video["file"])

