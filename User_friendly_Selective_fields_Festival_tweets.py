#Streaming API provides low latency access to Twitter's global stream of Tweet data.
#pip install TwitterAPI
#using Streaming API from TwitterAPI
#sample file in sample_api_test.py file

#Credentials stored in credentials.txt

from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
import json
from datetime import date
import codecs

def main():

###User Specifed Values
#Specify time to run script
        EndDate='2013-11-30'
#specify what feilds u need refer https://dev.twitter.com/docs/platform-objects/tweets for full list
		fields_needed=['text','entities','contributors','coordinates','place','created_at','source','retweet_count','favorite_count','id_str','in_reply_to_status_id_str','in_reply_to_screen_name','in_reply_to_user_id_str','possibly_sensitive','scopes','retweeted']
#specify search keywords seperated by commas
		search_keywords='thanksgiving, black friday, christmas, new year'
###

		
#loop to change filenames after day change
        while str(date.today())!=EndDate:
                dte=str(date.today())

# SAVE YOUR APPLICATION CREDENTIALS IN credentials.txt.
                o = TwitterOAuth.read_file('credentials.txt')
                api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret)

#see if authentications was successful
                r = api.request('account/verify_credentials')
                print(r.text)

#open timestamped file to store JSON tweets in: 
                d=date.today()
                d=str(d)
                filename=d+"_tweets_thanksgiving_blackfriday"
                file_twts= codecs.open(filename,"ab",encoding="utf-8")

#stream tweets with a given keyword and store it in a file
#given using statuses/filter and using track : text terms seperated with , are regarded as or and those seperated by whtespace are regarded as and
                try :   

                        for item in api.request('statuses/filter', {'track':search_keywords}):
                                item=convert_reduced_json(item,fields_needed)
                                json.dump(item,file_twts)
                                file_twts.write('\n')
                                if str(date.today())!=dte:
                                        break
                        file_twts.close()
                except Exception as e:
                                print(e)

#Extract only needed fieds from JSON
def convert_reduced_json(item, your_keys):
        item={ your_key: item[your_key] for your_key in your_keys }
        return item


if __name__=='__main__':
        main()

