import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity







bigreels=pd.read_csv('bigreelsplusdata.csv')
bigreels.fillna('NA',inplace=True)
#print(bigreels.info())

tempdata=bigreels.loc[:,~bigreels.columns.isin(['displayUrl','url','videoUrl','shortCode','videoDuration','ownerFullName','id','type','source'])]
#print(tempdata.info())

tempdata['tags']='NA'
tdatacolumns=tempdata.columns


for i in tdatacolumns:
    tempdata[i].replace(to_replace='NA',value='',inplace=True)
for i in tdatacolumns:
    tempdata[i]=tempdata[i].apply(lambda x:x.split())



for i in tdatacolumns:
    tempdata['tags']=tempdata['tags']+tempdata[i]


#print(tempdata['tags'][520])



tempdata['tags']=tempdata['tags'].apply(lambda x:" ".join(x))



tempdata['tags']=tempdata['tags'].apply(lambda x:x.lower())
newtempdata=tempdata['tags']
newbigreels=bigreels['shortCode']
newbigreels1=bigreels['caption']
newbigreels2=bigreels['source']
newbigreels3=bigreels['ownerUsername']

finaltempdata=pd.concat([newbigreels,newtempdata,newbigreels1,newbigreels2,newbigreels3],axis=1)





cv= CountVectorizer(max_features=5000, stop_words="english")
vectors= cv.fit_transform(finaltempdata['tags']).toarray()
featurenames=cv.get_feature_names_out()




simmatrix=cosine_similarity(vectors)



def recommend(reelid):
    index= finaltempdata[finaltempdata['shortCode']==reelid].index[0]
    distances=simmatrix[index]
    '''enumerate the matrix so that the similarity score will retain its index even after sorting'''
    r_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    resultlist=[]

    for i in r_list:
       
       resultdict={
           "id":finaltempdata.iloc[i[0]].shortCode,
           "source":finaltempdata.iloc[i[0]].source,
           "username":finaltempdata.iloc[i[0]].ownerUsername,
           "description":finaltempdata.iloc[i[0]].caption
       }

       resultlist.append(resultdict)

       ''' resultlist.append(finaltempdata.iloc[i[0]].shortCode)
       resultlist.append(finaltempdata.iloc[i[0]].source)
       resultlist.append(finaltempdata.iloc[i[0]].ownerUsername)
       resultlist.append(finaltempdata.iloc[i[0]].caption)'''
          
       
       #print(finaltempdata.iloc[i[0]].shortCode,finaltempdata.iloc[i[0]].source,finaltempdata.iloc[i[0]].ownerUsername,finaltempdata.iloc[i[0]].caption)

        
    ''', tempdata.iloc[i[0]].caption ''' 
    
    return resultlist
 

#print(recommend('ChCdBPflNx4'))

