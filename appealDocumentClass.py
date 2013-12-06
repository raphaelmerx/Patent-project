from textblob import TextBlob
import json
import re

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

class AppealDocument:
    # class is built from an element of data such as data[5]
    def __init__(self,document):
        self.applicationNumber = document['number']
        self.text = document['text']
        self.rejectedClaims = self.identifyClaims()
        if self.rejectedClaims == {'affirmed':set(),'reversed':set()}:
            (self.reversed,self.affirmed) = self.reversedOrAffirmed()
        self.sections = self.identifySections()
        
            
    # look at what claim numbers appear, and at whether the E's decision is rejected or affirmed concerning those claims
    def identifyClaims(self):
        claimsInvolved = {'affirmed':set(),'reversed':set()}
        indexStart = [m.start() for m in re.finditer('reject[a-z]*( [a-z]* [a-z]*)? claims? (\d+(-\d+)?,? ?(and )?)*', self.text)]
        indexEnd = [m.end() for m in re.finditer('reject[a-z]*( [a-z]* [a-z]*)? claims? (\d+(-\d+)?,? ?(and )?)*', self.text)]
        for j in range(len(indexStart)):
            # a raw string is has the form 'rejection of claims 2,3,4-8, and 45'
            rawString = self.text[indexStart[j]:indexEnd[j]]
            # extendedString is rawString plus some text around
            extendedString = self.text[indexStart[j]-30:indexEnd[j]+30].lower()
            if 'not affirm' in extendedString or 'not sustain' in extendedString or 'reverse' in extendedString:
                claimsInvolved['reversed'] = claimsInvolved['reversed'].union(stringToSequence(rawString))
            elif 'affirm' in extendedString or 'sustain' in extendedString:
                claimsInvolved['affirmed'] = claimsInvolved['affirmed'].union(stringToSequence(rawString))
        return claimsInvolved

    # this function intervienes only if no affirmed/reversed claims were identifired
    def reversedOrAffirmed(self):
        if self.rejectedClaims == {'affirmed':set(),'reversed':set()}:            
            # upper-case is often used for the final decision
            reversed = 'REVERSE' in self.text
            affirmed = 'AFFIRM' in self.text
            # we now look at the rare ones that don't have the decision in upper-case letters
            if (reversed,affirmed) == (False,False):
                reversed = 'reverse' in self.text
                affirmed = 'affirm' in self.text
            return  (reversed,affirmed)

    # this gets the sections the document talks about, but does not connect them to the claims
    def identifySections(self):
        sections = set()
        # this keeps 102,103,112, but rejects 134,141 which do not concern the application rejection
        indexStart = [m.start() for m in re.finditer(ur'\u00A7 1[0-2]\d(\([a-z]\))?', self.text)]
        indexEnd = [m.end() for m in re.finditer(ur'\u00A7 1[0-2]\d(\([a-z]\))?', self.text)]
        for j in range(len(indexStart)):
            # a raw string is has the form 'rejection of claims 2,3,4-8, and'
            rawString = self.text[indexStart[j]:indexEnd[j]]
            # extendedString is rawString plus some text around
            extendedString = self.text[indexStart[j]-50:indexEnd[j]+60].lower()
            sections.add(rawString[2:])
        return sections
        
        
    
        
