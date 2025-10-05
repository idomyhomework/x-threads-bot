import tweepy, os, time, random, schedule, json, traceback
from dotenv import load_dotenv

# loading API KEYS 

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# creating twitter client 

client = tweepy.Client(
    consumer_key = API_KEY,
    consumer_secret = API_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET,
    wait_on_rate_limit = True
)

# creating twitter client for uploading media

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# json file where I store my posts 

with open ("posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

video_posts = data["video_posts"]
promo_posts = data["promo_posts"]

# function for promo posts

def post_promo_on_x(promo_data):
    try:
        text = random.choice(promo_data)
        response = client.create_tweet(text=text)
        print("✅ Tweet posted successfully!")
        print(f"Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

# function for snippet posts (with media)

def post_snippet(caption, file):
    try:
        media = api.media_upload(file, media_category="tweet_video")
        client.create_tweet(text=caption, media_ids = [media.media_id])
        print(f"✅ Snippet posted: {caption}")
    except Exception as e:
        print(f"❌ Error posting snippet: {e}")
        traceback.print_exc()

def post_now(video):
    try:
        post_snippet(video["caption"], video["file"])
        print(f"✅ Snippet posted immediately: {video['caption']}")
    except Exception as e:
        print(f"❌ Error posting snippet immediately: {e}")
        traceback.print_exc()

# schedule video posts

for video in video_posts:
   day = video["day"].lower()
   video_time = video["time"]
   schedule.every().__getattribute__(day).at(video_time).do(
       lambda caption=video["caption"], file=video["file"]: post_snippet(caption, file)
   )

#schedule promo posts

schedule.every(6).hours.do(post_promo_on_x, promo_posts)

print("🤖 Bot running...")

post_now(video_posts[1])

#infinite loop where everything runs

# while True:
#     schedule.run_pending()
#     time.sleep(60)



