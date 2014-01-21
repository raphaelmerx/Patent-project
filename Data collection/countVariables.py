import appealDocumentClass
import json

json_data=open('/Users/raphaelmerx/Dropbox/Mes Documents/Berkeley/Capstone/invalid.json').read()
data = json.loads(json_data)

sections = {}
percentClaimsRev = {}
for i in range(len(data)):
	Document = AppealDocument(data[i])

	docSections = Document.sections
	for section in docSections:
		if section not in sections.keys():
			sections[section]=1
		else:
			sections[section] +=1

	print Document.applicationNumber

	'''
	numberReversed = len(Document.identifyClaims()['reversed'])
	numberAffirmed = len(Document.identifyClaims()['reversed'])
	if (numberAffirmed + numberReversed) != 0:
		percentClaimsRev[i] = numberReversed / (numberAffirmed + numberReversed)
	elif Document.affirmed == True:
		percentClaimsRev[i] = 0
	elif Document.reversed == True:
		percentClaimsRev[i] = 1
	'''
