from django.shortcuts import render
from django.shortcuts import render, redirect
import webbrowser

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
        #welcome = "Chatbot : You are welcome.."
        #bye = "Chatbot : Bye!!! "
       
        if x:
            vectorizer = CountVectorizer()
            count_vec = vectorizer.fit_transform(df['Questions']).toarray()
            welcome_input = ("hello", "hi","hai", "greetings", "sup", "what's up","hey")
            welcome_response = ["hey", "hi there", "hello", "I am glad! You are talking to me"]

            def bot(user_response):
                text = vectorizer.transform([user_response]).toarray()
                df['similarity'] = cosine_similarity(count_vec, text)
                sim_val=df.sort_values(['similarity'], ascending=False).iloc[0]['similarity']
                if sim_val > 0.60:
                    return df.sort_values(['similarity'], ascending=False).iloc[0]['Answers']
                else:
                    return "I am sorry! I don't understand you"
            
            def welcome(user_response):
                for word in user_response.split():
                    if word.lower() in welcome_input:
                        return random.choice(welcome_response)

            user_response = x
            user_response = user_response.lower()
            InputTraffic.append(user_response)
            if(user_response not in ['bye','shutdown','exit', 'quit','thank you']):
                    if(welcome(user_response)!=None):
                        wResponse  = welcome(user_response)
                        welcomeResponse.append(wResponse)
                        # print('welcomeResponse',welcomeResponse)
                    elif "indian laws" in user_response:
                        welcomeResponse.append("You can find Indian laws here at Indian kanoon. Let me take you there..")
                        webbrowser.open('https://indiankanoon.org')	
                    else:
                        cResponse = bot(user_response)
                        welcomeResponse.append(cResponse)
                        # print('welcomeResponse',welcomeResponse)
            else:
                 welcomeResponse.append('Bye! take care..')			

            welcomeTrafficResponse = zip(InputTraffic,welcomeResponse)
            context = {'welcomeTrafficResp':welcomeTrafficResponse} 
            return render(request,'Chatbot_Page_Dark.html',context) 

    return render(request,'Chatbot_Page_Dark.html')
