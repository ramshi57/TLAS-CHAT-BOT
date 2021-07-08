from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import *

import numpy as np
import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('portal/dataset/dataset.csv',
                 header=0,
                 names=['Questions', 'Answers'])

InputTraffic = []
welcomeResponse = []
def Entry_Page(request):
	return render(request, 'Entry_Page.html')

def Chatbot_Page(request):
    if request.method == "POST":
        x = request.POST['message']
        welcome = "Chatbot : You are welcome.."
        bye = "Chatbot : Bye!!! "
       
        if x:
            vectorizer = CountVectorizer()
            count_vec = vectorizer.fit_transform(df['Questions']).toarray()
            welcome_input = ("hello", "hi", "greetings", "sup", "what's up","hey")
            welcome_response = ["hey", "hi there", "hello", "I am glad! You are talking to me"]

            def bot(user_response):
                text = vectorizer.transform([user_response]).toarray()
                df['similarity'] = cosine_similarity(count_vec, text)
                return df.sort_values(['similarity'], ascending=False).iloc[0]['Answers']
            
            def welcome(user_response):
                for word in user_response.split():
                    if word.lower() in welcome_input:
                        return random.choice(welcome_response)

            user_response = x
            user_response = user_response.lower()
            InputTraffic.append(user_response)
            if(user_response not in ['bye','shutdown','exit', 'quit']):
                    if(welcome(user_response)!=None):
                        wResponse  = welcome(user_response)
                        welcomeResponse.append(wResponse)
                        # print('welcomeResponse',welcomeResponse)
                    else:
                        # print("Chatbot : ",end="")
                        cResponse = bot(user_response)
                        welcomeResponse.append(cResponse)
                        # print('welcomeResponse',welcomeResponse)

            welcomeTrafficResponse = zip(InputTraffic,welcomeResponse)
            context = {'welcomeTrafficResp':welcomeTrafficResponse} 
            return render(request,'Chatbot_Page_Dark.html',context) 

    return render(request,'Chatbot_Page_Dark.html')    

