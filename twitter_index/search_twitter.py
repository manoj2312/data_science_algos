# import all the libraries required
import twitter
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from collections import Counter
import webbrowser

#Setting up Twitter API
api = twitter.Api(consumer_key='TIEiulS6RPmeWHWTulCEQG3zf', consumer_secret='DVlPZBR6CRP0nVZlrs4Tl5WvpMSaqMvBaTHb3c3rCJYN3H0gEj', access_token_key='1648388227-HBTEJlzvR6970ep5Wy1xdn6Qoo3Pzqwym7XSzVK', access_token_secret='ZdxSPP0rAMbi2rwzq7TFngdfjAfwezsvTbB3FLG0XnXHK')
#querying twitter api
search = api.GetSearch(term='superman', lang='en', result_type='recent', count=100, max_id='')
tweets=[]
count=0
print "## The following are the top 100 tweets on the given query"
for tweet in search:
    tweets.append(tweet.text.encode('utf-8'))
    count+=1
    print count,':', tweet.text.encode('utf-8')
    
# Filtering the tweets and extracting the words
spec_char = ['~','!','@','#','$','%','^','&','*','(',')','_','+','|','}','{',':','"','?','>','<','`','-','=',';','/','.',',']
wordlist=[]
for tweet in tweets:
    for word in tweet.split(' '):
        for char in word:
            if char in spec_char:
                word = ''.join(char for char in word if char not in spec_char)
                break
        if 'http' not in word:
            wordlist.append(word)
print "### The following is the list of words extracted"
print wordlist

# Finding the most common words
most_common_words = Counter(wordlist).most_common(100)
wordlist = ''
for pair in most_common_words:
    wordlist += str(pair[0])
    wordlist += ' '

# Displaying the results in a png file
tags = make_tags(get_tag_counts(str(wordlist)), maxsize=100)
# List of Font Names: (Should be one of Nobile, Old Standard TT, Cantarell, Reenie Beanie, Cuprum, Molengo, Neucha, Philosopher, Yanone Kaffeesatz, Cardo, Neuton, Inconsolata, Crimson Text, Josefin Sans, Droid Sans, Lobster, IM Fell DW Pica, Vollkorn, Tangerine, Coustard, PT Sans Regular)
fontnames_list = ['Nobile', 'Old Standard TT', 'Cantarell', 'Reenie Beanie', 'Cuprum', 'Molengo', 'Neucha', 'Philosopher', 'Yanone Kaffeesatz', 'Cardo', 'Neuton', 'Inconsolata', 'Crimson Text', 'Josefin Sans', 'Droid Sans', 'Lobster', 'IM Fell DW Pica', 'Vollkorn', 'Tangerine', 'Coustard', 'PT Sans Regular'] 
#for name in fontnames_list:
create_tag_image(tags, 'twitter_opinion.png', size=(900, 600), fontname='Neucha')
webbrowser.open('twitter_opinion.png') # see results