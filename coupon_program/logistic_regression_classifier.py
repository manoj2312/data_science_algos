from __builtin__ import type
import re
import numpy
import sklearn
from sklearn import linear_model
from email import _name
import csv
def load_into_file(path):
    File=open(path,'r')
    lines=File.readlines()
    data=[]
    for line in lines:
            message = line.split(':')[1:]
            data.append(message)
    File.close()
    return data
def write_into_file(path, content, delimiter):
    with open(path, "wb") as csv_file:
        for line in content:
            csv_file.write(line + delimiter)
        #=======================================================================
        # writer = csv.writer(csv_file)
        # for line in content:
        #     print line
        #     writer.writerow(line)
        #=======================================================================
    return
def process_data(data):
    processed_data = []
    for message in data:
        msg = message[0]
        special_characters_list=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','}','[',']','|',';',':','"',',','<','>','.','?','/']
        for spec_char in special_characters_list:
            split_message = msg.split(spec_char)
            msg = " ".join(split_message)
        processed_data.append(msg)
    return processed_data
def process_test_data(data):
    processed_data = []
    for message in data:
        if message is not None:
            msg = message[0]
            special_characters_list=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','}','[',']','|',';',':','"',',','<','>','.','?','/']
            for spec_char in special_characters_list:
                split_message = msg.split(spec_char)
                msg = " ".join(split_message)
            processed_data.append(msg)
    return processed_data
def feature_vector(data, vec):
    for message in data:
        for word in message.split(' '):
            if word not in vec:
                vec.append(word)
    return vec
def freq_count(word, list_of_words):
    count = 0
    for words in list_of_words.split():
        if word in words:
            count += 1
    return count
def find_term_vector(data, vec):
    term_vector_list = []
    for msg in data:
        term_vector=[]
        for word in vec:
            term_vector.append(freq_count(word, msg))
        term_vector_list.append(term_vector)
    return term_vector_list
if __name__ == '__main__':   
    vec=[]
    path = '/home/manu/Documents/Coupons/coupons.txt'
    data = load_into_file(path)
    processed_data = process_data(data)
    vec = feature_vector(processed_data, vec)
    
    coupons_data = load_into_file('/home/manu/Documents/Coupons/coupons.txt')
    processed_coupons_data = process_data(coupons_data) 
    vec = feature_vector(processed_coupons_data, vec)
    not_coupons_data = load_into_file('/home/manu/Documents/Coupons/ads.txt')
    processed_not_coupons_data = process_data(not_coupons_data)
    vec = feature_vector(processed_not_coupons_data, vec)
    
    coupons_term_vector = find_term_vector(processed_coupons_data, vec)
    not_coupons_term_vector = find_term_vector(processed_not_coupons_data, vec)
    X = coupons_term_vector + not_coupons_term_vector
    X=numpy.reshape(X, (len(X), len(X[0])))
    class_labels = []
    for i in range(len(coupons_term_vector)):
        class_labels.append(0)
    for i in range(len(not_coupons_term_vector)):
        class_labels.append(1)
        
    logit = linear_model.LogisticRegression()
    logit.fit(X,class_labels)
    # print logit.get_params()
    logit.predict(X)
    logit.predict_proba(X)
    
    test_data = load_into_file('/home/manu/Documents/Coupons/sms_test_data.txt')
    processed_test_data = process_test_data(test_data)
    test_term_vector = find_term_vector(processed_test_data, vec)
     
    print "Testing on test data"
    X = test_term_vector
    X=numpy.reshape(X, (len(X), len(X[0])))
    predictions = logit.predict(X)
    for index, message in enumerate(test_data):
        print message, "Class:", predictions[index]
    
#     vec = feature_vector(processed_test_data, vec)
#     write_into_file('/home/manu/Documents/Coupons/feature_vector.txt', vec, delimiter=",")