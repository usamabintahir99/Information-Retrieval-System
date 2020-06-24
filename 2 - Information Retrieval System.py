#!/usr/bin/env python
# coding: utf-8

# In[80]:


from bs4 import BeautifulSoup
import requests

source=requests.get('https://www.theverge.com/tech/archives').text
next_link=' '
counter=0
while(True):
    response=BeautifulSoup(source,'lxml')
    links_list=response.find_all('h2',class_='c-entry-box--compact__title')

    for i in links_list:
        title=i.a.text
        print(title)
        link=i.a['href']
        link_source=requests.get(link).text
        link_response=BeautifulSoup(link_source,'lxml')
        content=link_response.find('div',class_='c-entry-content').text
        with open('.\Data\\' + str(counter) + '.txt', 'w',encoding=('utf-8')) as fout:
            fout.write(title+'\n'+content)
        counter=counter+1

    next_link=response.find('a',class_="c-pagination__next c-pagination__link p-button")['href']
    
    if (next_link [0:5]=='https'):
        url='https://www.theverge.com/science/archives'
    else:        
        url='https://www.theverge.com'+next_link
    
    if (counter>=1000):
        break
    
    source=requests.get(url).text

print(counter)


# In[131]:


#Reading files and populating set
import string
import os
vocab_set=set()
for filename in os.listdir('.\Data'):
    with open('.\Data\\' + filename, 'r',encoding=('utf-8')) as fhand:
        for line in fhand:
            for word in line.lower().translate(str.maketrans(dict.fromkeys(string.punctuation))).split():
                vocab_set.add(word)


# In[132]:


#populating vocabulary dictionary
vocab_dict=dict()
i=0
while(len(vocab_set)>0):
    vocab_dict[vocab_set.pop()]=i
    i=i+1    


# In[133]:


#matrix population
import numpy as np
term_doc_matrix = np.zeros((counter, len(vocab_dict)), dtype=int)
for filename in os.listdir('.\Data'):
    with open('.\Data\\' + filename, 'r',encoding=('utf-8')) as fhand:
        for line in fhand:
            for word in line.lower().translate(str.maketrans(dict.fromkeys(string.punctuation))).split():
                term_doc_matrix[int(filename.rstrip('.txt')),vocab_dict[word]]=1


# In[134]:


# query and rank vector population
query_vector = np.zeros((len(vocab_dict),), dtype=int)
query = input("Write your query: ")

for word in query.lower().translate(str.maketrans(dict.fromkeys(string.punctuation))).split():
    try:
        query_vector[vocab_dict[word]]=1
    except:
        pass

rank_vector = term_doc_matrix.dot(query_vector)


# In[135]:


#printing results
if rank_vector.sum()==0:
    print('No Results Found.')
else:
    import operator
    result=dict()
    i=0
    for i in range(counter):
        result[i]=rank_vector[i]
        sorted_result= dict( sorted(result.items(),key=operator.itemgetter(1),reverse=True))
        
    for k,v in sorted_result.items():
        if v>0:
            print(str(k)+'.txt')


# In[ ]:




