
## text classification

import numpy as np
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.datasets import load_files

nltk.download('stopwords')

# importing

reviews= load_files('txt_sentoken/')
X,y=reviews.data,reviews.target # review and its class=0=neg,1=positive

# storing as pickle

with open('X.pickle','wb') as f:
    pickle.dump(X,f)
    
with open('y.pickle','wb') as f:
    pickle.dump(y,f)    
    
 #unpickle when x and y varianle you have to load so..time  
with open('X.pickle','rb') as f:
     X=pickle.load(f)
 
with open('y.pickle','rb') as f:
     y=pickle.load(f)       
    
 # creating the corpus  preprocseessing
   
corpus=[]
for i in range (len(X)):
    review=re.sub(r'\W',' ',str(X[i])) # removing all the non word,puctution
    review=review .lower()
    review=re.sub(r'\s+[a-z]\s+',' ',review) # to remove a single character space before and after into single space
    review=re.sub(r'^[a-z]\s+',' ',review) # to remove a single character in start that has one space after
    review=re.sub(r'\s+',' ',review) ## to remove a lot of space into one
    corpus.append(review)

## transforming into BOW model
    
from sklearn.feature_extraction.text import CountVectorizer  
# using count vectorizer to create BOW     
vectorizer=CountVectorizer(max_features=2000,min_df=3,max_df=0.6,stop_words=stopwords.words('english'))    
x=vectorizer.fit_transform(corpus).toarray() # created BOW model

# converting BOW model to create TF-idf model
#tf-idf transformer can convert simple BOW model into tf-idf

from sklearn.feature_extraction.text import TfidfTransformer
transformer=TfidfTransformer()
x=transformer.fit_transform(x).toarray() # converted into td-idf model

## tf-idf vectorizer so to avoid creating two pickles

from sklearn.feature_extraction.text import TfidfVectorizer  
     
vectorizer=TfidfVectorizer(max_features=2000,min_df=3,max_df=0.6,stop_words=stopwords.words('english'))    
x=vectorizer.fit_transform(corpus).toarray()



#splitting the data into test and train

from sklearn.model_selection import train_test_split

text_train,text_test,sent_train,sent_test=train_test_split(x,y,test_size=0.2,random_state=0)    

# using the logistic regression to fit the model

# each dentence is mapped to point the by thresh it is descided whether it is negative or positive

from sklearn.linear_model import LogisticRegression

classifier=LogisticRegression()
classifier.fit(text_train,sent_train)

# performance matrix
sent_pred=classifier.predict(text_test)

from sklearn.metrics import confusion_matrix
cm=confusion_matrix(sent_test,sent_pred)

from sklearn import metrics
accur_score=metrics.accuracy_score(sent_test,sent_pred)
print('accuracy of the model',accur_score*100)
    
# to save it as pickle file and use for prediction
#pickeling the classifier

with open('classifier.pickle','wb') as f:
    pickle.dump(classifier,f)    
# we cant directly save and use it coz its input should also be in vectorized format
# pickeling the vectorizer
    
with open('tfidfmodel.pickle','wb') as f:
    pickle.dump(vectorizer,f)

# unpickling the classifer and vectorizer
    
with open('classifier.pickle','rb') as f:
    clf=pickle.load(f)
    
with open('tfidfmodel.pickle','rb') as f:
    tfidf=pickle.load(f)   
    
##
sample=['you are a bad person']    
sample=tfidf.transform(sample).toarray()
 
if clf.predict(sample)==0:
    print('negative')
else:
    print('positive')
    
##
sample=['you are a good person']    
sample=tfidf.transform(sample).toarray() 
if clf.predict(sample)==0:
    print('negative')
else:
    print('positive')
    
    
    
    
    
    