import requests,json,urllib
from Config import Config
cd = Config().data

url = "https://text-sentiment.p.rapidapi.com/analyze"

headers = {
    "content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": cd["X-RapidAPI-Key"],
	"X-RapidAPI-Host": "text-sentiment.p.rapidapi.com"
}


def get_sentiment(text):

    text = urllib.parse.quote(text)
    querystring = {"text":text}
    response = requests.request("POST", url, data=querystring, headers=headers)

    # print(response)

    if response.status_code == 200:
        sentiment = json.loads(response.text)
        return sentiment
    else:
        return False

if __name__ == '__main__':
    # test
    senti = get_sentiment("i hate everything")

    print(type(senti),senti)
