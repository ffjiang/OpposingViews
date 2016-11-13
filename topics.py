import json
import requests
import os
import LDA
import numpy as np

keyPhrasesURL = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
topicModelURL = 'https://ussouthcentral.services.azureml.net/workspaces/d049d23b99c54a6ca22ee16defb4532c/services/ac4a75d33a714a2d8407d7e3bf0fa711/execute?api-version=2.0&details=true'
articleTopicURL = 'https://ussouthcentral.services.azureml.net/workspaces/d049d23b99c54a6ca22ee16defb4532c/services/7f2aca8b176b4e949657cfe7e422c883/execute?api-version=2.0&details=true'

def getKeyPhrases(text):
    headers = {'Ocp-Apim-Subscription-Key': '7d6d7cd16aed419b9c50713cf944a958',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    payload = {'documents': [
                    {
                        'language': 'en',
                        'id': '1',
                        'text': text[:1000]
                    }
                ]
           }
    response = requests.post(keyPhrasesURL, data=json.dumps(payload), headers=headers)
    print(response.status_code)

    data = response.text
    print(data)
    return data

def getTopicModel():
    headers = {'Authorization': 'Bearer gDgMMBxHvum2wkA7Q4C0ZQwmZSniI8TuemSOUV9KIHcT5L9EEUDgrPT9rvibfwyrDm+bqqStSCVq99qpZn/0JA==',
               'Content-type': 'application/json',
               'Accept': 'application/json'}
    response = requests.post(topicModelURL, data=json.dumps({}), headers=headers)
    print(response.status_code)
    data = response.text
    print(data)
    with open('transformed_data', 'a') as f:
        f.write(data)
    print(data['Results']['transformed_data']['value']['ColumnNames'])
    return data

#getTopicModel()

def getArticleTopic(text):
    headers = {'Authorization': 'Bearer LTfhtQm7ucstX/6fSLiAfqJJn0i3lY1Jv0L187dHRhjyjpEmIHoTQ/dqpx3HXl2vfD+YR4iczWKUEOnYT8XrAg==',
               'Content-type': 'application/json',
               'Accept': 'application/json'}
    payload = {
                  'Inputs': {
                      'input1': {
                          'ColumnNames': [
                              'Col1'
                          ],
                          'Values': [
                              [
                                  text
                              ]
                          ]
                      }
                  },
                  'GlobalParameters': {}
              }
    response = requests.post(articleTopicURL, data=json.dumps(payload), headers=headers)
    print(response.status_code)
    data = response.text
    print(data)
    #print(data['Results']['topic']['value']['ColumnNames'])
    return data

def getArticleTopicSK(text, model, vectorizer, transformed):
    input = LDA.preprocess(text, vectorizer)[0]
    output = model.transform(input)
    maxIndex = np.argmax(output)

    tf_feature_names = vectorizer.get_feature_names()
    print('Article was most likely to contain topic #%d' % maxIndex) 
    print(' '.join([tf_feature_names[i]
                        for i in model.components_[maxIndex].argsort()[:-19:-1]]))

    leftAligned = True

    # Select two from the opposite end of political spectrum and one from the
    # same
    sameTransformed = None
    oppTransformed = None
    if leftAligned:
        sameTransformed = transformed[:317]
        oppTransformed = transformed[317:]
    else:
        sameTransformed = transformed[317:]
        oppTransformed = transformed[:317]
    sameSimilarity = np.array([np.linalg.norm(article - output[0]) for article in sameTransformed])
    oppSimilarity = np.array([np.linalg.norm(article - output[0]) for article in oppTransformed])
    maxSameIndex = np.argmin(sameSimilarity)
    maxOppIndices = np.argpartition(oppSimilarity, 2)[:2]
    maxIndices = []
    if leftAligned:
        maxIndices.append(maxSameIndex)
        maxIndices.append(maxOppIndices[0] + 317)
        maxIndices.append(maxOppIndices[1] + 317)
    else:
        maxIndices.append(maxSameIndex + 317)
        maxIndices.append(maxOppIndices[0])
        maxIndices.append(maxOppIndices[1])
    print('The most likely topic of the three most similar articles:')
    for ind in maxIndices:
        print(ind)
        print(output)
        print(transformed[ind])
        print(np.argmax(transformed[ind]))
    return maxIndices

    


