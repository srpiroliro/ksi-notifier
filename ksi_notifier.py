import requests,telegram,json,time, traceback
from datetime import datetime


API_KEY="" # youtube data api key
TELEGRAM_BOT_TOKEN="" # telegram bot token
CHAT_ID="" # telegram chat id

if not (API_KEY or TELEGRAM_BOT_TOKEN or CHAT_ID):
    print("CHANGES REQUIRED TO THE FILE!")
    exit()

requrl=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1&playlistId=UUGmnsW623G1r-Chmo5RB4Yw&key={API_KEY}"
bot=telegram.Bot(token=TELEGRAM_BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="hello!")

try:
    prev_video={"id":"", "time":datetime.now()}
    cnt=0
    while True:
        current_hour=int(time.strftime("%H"))
        if 7<=current_hour<22:
            cnt+=1

            r=requests.get(requrl)
            if r:
                response=json.loads(r.text)
                if not "error" in response:
                    if len(response["items"])>0:

                        video=response["items"][0]["snippet"]
                        url=video["resourceId"]["videoId"]
                        publishedAt=datetime.strptime(video["publishedAt"].replace("T", " ").replace("Z",""), "%Y-%m-%d %H:%M:%S")

                        if url!=prev_video["id"] and (publishedAt>prev_video["time"] or not prev_video["id"]):
                            title=video["title"]
                            if "maxres" in video["thumbnails"]:
                                thumbnail=video["thumbnails"]["maxres"]["url"]
                            elif "high" in video["thumbnails"]:
                                thumbnail=video["thumbnails"]["high"]["url"]
                            else:
                                thumbnail=video["thumbnails"]["default"]["url"]

                            bot.send_message(chat_id=CHAT_ID, text=f"{title}\nhttps://www.youtube.com/watch?v={url}")
                            if any(x in title.lower() for x in ["laugh", "smile"]):
                                bot.send_message(chat_id=CHAT_ID, text=f"WARNING WARNING WARNING")
                                bot.send_message(chat_id=CHAT_ID, text=f"URGENT URGENT URGENT")
                            bot.send_message(chat_id=CHAT_ID, text=f"https://www.amazon.com/gc/redeem")
                            
                            prev_video={
                                "id":url,
                                "time":publishedAt
                            }
                else:
                    bot.send_message(
                        chat_id=CHAT_ID,
                        text="An ERROR ocurred:\n"+str(response['error'])
                    )
            else:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"An ERROR ocurred making the request:\n{r.text}"
                )
                
            print("\n-----------------\n")
            time.sleep(9)
except Exception as e:
    print(traceback.format_exc())
    bot.send_message(chat_id=CHAT_ID, text="try/except ERROR:")
    bot.send_message(chat_id=CHAT_ID, text=traceback.format_exc())