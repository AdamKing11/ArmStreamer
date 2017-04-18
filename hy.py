import sys, tweepy, json, re
from datetime import datetime
import os.path


# one way to import all the keys you need for the Twitter API...
# there are other/better ways, this one is just simple
# and keeps the actual codes outside of the source code
from keys import keys

class lil_Listener(tweepy.StreamListener):

    def __init__(self, c_key, c_secret, auth_token, auth_secret):
        # build an API in the API, so we can look up reply tweets
        auth = tweepy.OAuthHandler(c_key, c_secret)
        auth.set_access_token(auth_token, auth_secret)
        self.api = tweepy.API(auth)
    
    def parse_tweet(self, tweet, as_reply = False):
        # pass in a dict for the tweet
        td = {}
        # numbers for sorting
        td['1_tweet_id'] = tweet['id'] 
        td['2_user_id'] = tweet['user']['id']
        td['3_text'] = re.sub('[\n\t]', ' ', tweet['text'])
        td['4_date'] = tweet['created_at']
        td['5_lang'] = tweet['lang']
        td['6_geotags'] = tweet['geo']
        td['7_as_reply'] = as_reply
        td['8_reply_to'] = tweet['in_reply_to_status_id_str']

        return td

    def write_tweet(self, td):
        # write the tweet to our output file
        today_date = datetime.today().date()
        file_name = str(today_date) + 'hye_output.csv'
        # if the file doesn't already exist, create it and make col heads
        if not os.path.exists(file_name):
            with open(file_name, 'w') as wf:
                title_line = 'tweet_id\tuser_id\ttext\tcreated_at'
                title_line += '\tgeotags\tlanguage\tas_reply\treply_id'
                wf.write(title_line + '\n')

        # write the values for the tweet
        with open(file_name, 'a') as wf:
            wf.write('\t'.join([str(td[k]) for k in sorted(td)]))
            wf.write('\n')

        return True

    def on_data(self, data):
        # turn the JSON tweet object into a dictionary
        tweet = json.loads(data)
        td = self.parse_tweet(tweet)
        try:
            x = x + 1
            if x >= 1000000:
                x = 0
                y += 1
            print(x,y)
        except:
            pass
        print('\t'.join([str(td[k]) for k in sorted(td)]))
        self.write_tweet(td)

        if td['8_reply_to'] != None:
            try:
                orig_tweet = self.api.get_status(td['8_reply_to'])._json
                tdo = self.parse_tweet(orig_tweet, as_reply = True)
                try:
                    x = x + 1
                    if x >= 1000000:
                        x = 0
                        y += 1
                    print(x,y)
                except:
                    pass
                print('\t'.join([str(tdo[k]) for k in sorted(tdo)]))
                self.write_tweet(tdo)
            except:
                pass
        return True



###############################c################################################

if __name__ == '__main__':
    
############################
# keywords
    # top 50 most frequent words in EANC
    keywords = ['է', 'եվ','որ','են','էր','ու',
    'մի','ես','այդ','էլ','իր','թե','համար',
    'նա','եմ', 'էին','այն','այս','ինչ','հետ',
    'ոչ', 'բայց', 'իսկ','նրա', 'մեր', 'մեջ',
    'չի', 'վրա', 'նաեվ','մասին','շատ','ա',
    'ինչպես','կարող','երբ','հետո','կամ','իմ',
    'ավելի','միայն','չէ','ինձ','ի','եթե',
    'պետք','մեծ','իրենց','նրան','այլ','ենք']
############################
    x = 0
    y = 0
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])    

    listener = lil_Listener(keys[0], keys[1], keys[2], keys[3])
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=keywords)
   

        

