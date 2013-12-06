# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

from textblob import TextBlob
import json
import re

json_data=open('/Users/raphaelmerx/Dropbox/Mes Documents/Berkeley/Capstone/invalid.json').read()
data = json.loads(json_data)

def main():
    # takes as an argument a string 'i-j' like '34-37'
    def rangeToSequence(s):
        rangeString = re.findall(r'\d+', s)
        begin = int(rangeString[0])
        end = int(rangeString[1])
        return range(begin, end+1)

    # takes as an argument a string like 'rejection of claims 3, 5-8, and 45'
    # returns a set of claims the string talks about
    def stringToSequence(s):
        claims = set()
        rangesFound = re.findall(r'\d+-\d+', s)
        for stringRange in rangesFound:
            for claimNumber in rangeToSequence(stringRange):
                claims.add(claimNumber)
        numbers = re.findall(r'\d+', s)
        for claimNumber in numbers:
            claims.add(int(claimNumber))
        return claims

    claimsInvolved = {}
    for i in range(len(data)):
        text = data[i]['text']
        claimsInvolved[i] = {'affirmed':set(),'reversed':set()}
        indexStart = [m.start() for m in re.finditer('rejections? of( [a-z]+)? claims? (\d+(-\d+)?,? ?(and )?)*', text)]
        indexEnd = [m.end() for m in re.finditer('rejections? of( [a-z]+)? claims? (\d+(-\d+)?,? ?(and )?)*', text)]
        for j in range(len(indexStart)):
            # a raw string is has the form 'rejection of claims 2,3,4-8, and'
            rawString = text[indexStart[j]:indexEnd[j]]
            # extendedString is rawString plus some text around
            extendedString = text[indexStart[j]-30:indexEnd[j]+30].lower()
            if 'not affirm' in extendedString or 'not sustain' in extendedString or 'reverse' in extendedString:
                claimsInvolved[i]['reversed'] = claimsInvolved[i]['reversed'].union(stringToSequence(rawString))
            elif 'affirm' in extendedString or 'sustain' in extendedString:
                claimsInvolved[i]['affirmed'] = claimsInvolved[i]['affirmed'].union(stringToSequence(rawString))

    # For those left, look for 'REVERSE' or 'AFFIRM' in text
    for i in range(len(data)):
        text = data[i]['text']
        if 'REVERSE' in text and claimsInvolved[i]['reversed']==set():
            claimsInvolved[i]['reversed'].add(True)
        if 'AFFIRM' in text and claimsInvolved[i]['affirmed']==set():
            claimsInvolved[i]['affirmed'].add(True)

    # Now for the last empty ones, we look for 'reverse' or 'affirm' in lower case
    for i in range(len(data)):
        text = data[i]['text']
        text = text.lower()
        if 'reverse' in text and claimsInvolved[i]['reversed']==set() and claimsInvolved[i]['affirmed']==set():
            claimsInvolved[i]['reversed'].add(True)
        if 'affirm' in text and claimsInvolved[i]['affirmed']==set() and claimsInvolved[i]['reversed']==set():
            claimsInvolved[i]['affirmed'].add(True)


    return claimsInvolved

if __name__=="__main__":
    main()


