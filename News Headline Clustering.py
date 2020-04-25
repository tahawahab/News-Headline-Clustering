import csv; from nltk import PorterStemmer;from nltk import WordNetLemmatizer;
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster
import pandas

porter=PorterStemmer()
lemmatizer=WordNetLemmatizer()
vector = TfidfVectorizer()

newwordlist=[]
dic=dict()
for i in range(999):
    newwordlist.append([])
with open("NEWS Headline Clustering - WOG/stopwords1.txt") as stop:
    word1 = stop.read()
    stop.close()
    word1 = word1.split('\n')
itr=0
with open("NEWS Headline Clustering - WOG/demo.csv",mode="r",encoding="ANSI") as file1:
    readfile=csv.reader(file1)
    for row in readfile:
        listword=row[1].split()
        if len(listword)==1:
            continue
        else:
            print("new row")
            for i in listword:
                if i not in word1:
                    put=True
                    if (put==True):
                        i=lemmatizer.lemmatize(i)
                        i=porter.stem(i)
                        print(i)
                        newwordlist[itr].append(i)


            itr+=1
itr=0
docnum=1

newlist=[]

newlist= [" ".join(x) for x in newwordlist]
while(itr<999):
    itr1=len(newwordlist[itr])
    numitr = 0
    while(numitr<itr1-1):
        if numitr+2<=itr1:
            key = newwordlist[itr][numitr]
            value=newwordlist[itr][numitr+1]
        print("key",key,"value is",value)
        if docnum not in dic:
            dic[docnum] = {}
            dic[docnum].setdefault(key, []).append(value)
        else:
            dic[docnum].setdefault(key, []).append(value)
        numitr+=1
    itr+=1
    docnum+=1

print(dic)
word_sequence={}
for x in dic:
     list2=[]
     list=dic[x]
     for x2 in list:
         l=list[x2]
         for l3 in range(len(l)):
            u=x2 + ' ' + l[l3]
            print(x)
            print(u)
            list2.append(u)
     word_sequence[x]=list2
for x in word_sequence:
    print(word_sequence[x])


finallist=[*word_sequence.values()]
finallist= [" ".join(x) for x in finallist]
tfidf=vector.fit_transform(finallist)
distance = 1 - cosine_similarity(tfidf)

linkage_matrix = ward(distance)
fig, ax = plt.subplots(figsize=(15, 20))


ax = dendrogram(linkage_matrix, orientation="right", labels=newlist);

plt.tick_params(\
    axis= 'x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')

plt.tight_layout()

plt.savefig('ward_clustersnewfinalmemcheck.png', dpi=200)
plt.close()

# fl = fcluster(linkage_matrix,2,criterion='maxclust')
# print(fl)

# cluster_output = pandas.DataFrame({'Headline':newlist , 'cluster':fl})
# print(cluster_output)


file1.close()