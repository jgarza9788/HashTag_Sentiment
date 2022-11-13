import requests,json,re
from Config import Config
cd = Config().data

url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"



headers = {
	"X-RapidAPI-Key": cd["X-RapidAPI-Key"],
	"X-RapidAPI-Host": "twitter154.p.rapidapi.com"
}




def get_tweets(hashtag,limit=20):

    if hashtag.startswith('#'):
        pass
    else:
        hashtag = '#'+hashtag
    
    # section = 'top'
    section = 'latest'
    # section can be ..."value is not a valid enumeration member; permitted: 'top', 'latest', 'people', 'photos', 'videos'"


    querystring = {"hashtag":hashtag,"limit":str(limit),"section":section}
    # limits have to be 20 or less ... but it only returns a max of 18

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    if response.status_code == 200:
        # print(response.text)
        twts = json.loads(response.text)

        results = []
        for index,i in enumerate(twts['results']):
            # print(i['text'])
            results.append( re.sub(r"[^a-zA-Z\t\r\n\f\s]","",i['text']))
        
        return ' '.join(results)

    else:
        return False



if __name__ == '__main__':
    # test
    tweets = get_tweets('python',20)

    print(tweets)

