
from textblob import TextBlob
import json
import re

json_data=open('/Users/raphaelmerx/Dropbox/Mes Documents/Berkeley/Capstone/invalid.json').read()
data = json.loads(json_data)

for i in range(len(data)):
    if i%10==1:
        blob = data[i]['text']
        blob = blob[-1000:]
        blob = TextBlob(blob)
        
reverseSet = set()
affirmSet = set ()
for i in range(len(data)):
    text = data[i]['text']
    text = text.lower()
    if 'reverse' in text:
        reverseSet.add(i)
    if 'affirm' in text:
        affirmSet.add(i)
# 26 intersections
intersect = reverseSet.intersection(affirmSet)

#explore the intersection
for i in intersect:
    text = data[i]['text']
    indexes = [m.start() for m in re.finditer('ejection of claim', text)]
    for j in indexes:
        
revAff = {}
for i in intersect:
    text = data[i]['text']
    text = text.lower()
    reverseIndexes = [m.start() for m in re.finditer("reverse", text)]
    affirmIndexes = [m.start() for m in re.finditer("affirm", text)]
    revPercentage = float( len(reverseIndexes)) / (len(reverseIndexes) + len(affirmIndexes))
    revAff[i] = revPercentage



'''
for document in data:
    if 'rejection of claims' in document['text'] and 'reversed' in document['text']:
        rejectIndex = document['text'].index('rejection of claims')
        revIndex= document['text'][rejectIndex:].index('reversed')
        revIndex = revIndex + rejectIndex
        print document['text'][rejectIndex:revIndex + 10]
        print "------------------------------------------"
'''

#text = data[0]['text']
