import re
import twitter_sentiment

def look_for_phone_number(numbers):
    phone_number=[]
    for number in numbers:
        if len(number)>=7:
            phone_number.append(number)
    return phone_number
def look_for_website(symbols):
    websites=[]
    for symbol in symbols:
        if 'http://' == symbol[0:7] or 'https://' == symbol[0:8]:
            websites.append(symbol)
        else:
            searchObj = re.search( r'^[a-zA-Z0-9\-\.]+\.(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU|co.in)$', symbol, re.I)
            if searchObj:
                websites.append(symbol)
    return websites
def look_for_email(symbols):
    email=[]
    for symbol in symbols:
        searchObj = re.search( r'[a-z0-9\._]{1,}@[a-z0-9\.]{1,}.[a-z]{2,3}', symbol, re.I)
        if searchObj:
            email.append(searchObj.group())
    return email
def look_for_time(symbols, tokens):
    time=[]
    for symbol in symbols:
        if ':' in symbol and len(symbol.split(':')) == 2 and symbol.split(':')[0].isdigit() and symbol.split(':')[1].isdigit():
            period = tokens[tokens.index(symbol) + 1]
            if period.lower() == 'am' or period.lower() == 'pm':
                time.append(symbol+' '+period)
            else:
                time.append(symbol)
    return time

sentence = "PizzaHut Fantastic Friday. Buy 1 Pizza Get 1 Pizza Absolutely Free. www.myntra.com manoj.gootam@gmail.com Call 68886888 or Order Online/Thru Mobile @dominos.co.in. Coupon MoB06 Hurry!Offer ends today.T&C, Date 23/04/2014, 05:00 Pm"
# tokens = nltk.word_tokenize(sentence)
# print tokens
# 
# # print nltk.help.upenn_tagset()  #List of all POS tags used. POS tagset
# POS_Tags=['CD','LS','SYM','NNP','NNPS']
# tagged = nltk.pos_tag(tokens)

tokens = sentence.split(' ')
# print tokens
numbers=[]
coupons=[]
symbols=[]
dates=[]
for word in tokens:
    if word.isalnum():
        if word.isdigit():
            numbers.append(word)
        else:
            for letter in word:
                if letter.isdigit():
                    coupons.append(word)
                    break
    elif not word.isalnum():
        symbols.append(word)
    else:
        print "Not what we are looking for, ", word
        
        
print 'Phone Number', look_for_phone_number(numbers)
print 'Website', look_for_website(symbols)
print 'Email', look_for_email(symbols)
print 'Coupon Code', coupons
print 'Time', look_for_time(symbols, tokens)
# print numbers, coupons, symbols