import twitter
import json
import collections

def addHashtags(hashtag_list):
	hashtag = []
	for i in hashtag_list:
		temp = {}
		temp["tag"] = i["text"]
		hashtag.append(temp)
	return hashtag

def filterDetail(pic,term):
	img = collections.OrderedDict()
	img["url"] = pic["entities"]["media"][0]["media_url"]
	img["imgId"] = pic["entities"]["media"][0]["id"]
	img["user_id"] = pic["user"]["id"]
	img["user_name"] = pic["user"]["name"]
	img["geo_status"] = pic["geo"]
	img["hashtags"] = addHashtags(pic["entities"]["hashtags"])
	img["dateUploaded"] = pic["created_at"]
	img["positionInStatus"] = 1
	img["searchTermUsed"] = term
	return img

def filterExtraPictures(pic, index,term):
	img = collections.OrderedDict()
	img["url"] = pic["extended_entities"]["media"][index]["media_url"]
	img["imgId"] = pic["extended_entities"]["media"][index]["id"]
	img["user_id"] = pic["user"]["id"]
	img["user_name"] = pic["user"]["name"]
	img["geo_status"] = pic["geo"]
	img["hashtags"] = addHashtags(pic["entities"]["hashtags"])
	img["dateUploaded"] = pic["created_at"]
	img["positionInStatus"] = index + 2
	img["searchTermUsed"] = term
	return img

def filterStatusWithMedia(results):
	filter = []
	for i in results["statuses"]:
		if "media" in i["entities"]:
			filter.append(i)
	return filter

def mediaInfo(results,searchTerm):
	media = []
	for i in results["statuses"]:
		if "media" in i["entities"]:
			media.append(filterDetail(pic = i,term = searchTerm))
		if "extended_entities" in i:
			if "media" in i["extended_entities"]:
				for k in range(1,len(i["extended_entities"]["media"])):
					media.append(filterExtraPictures(pic = i, index = k,term = searchTerm))
	return media

def gatherData(api, searchTerm,final):
	results = api.GetSearch(term = searchTerm,count = 500,since = '2014-07-19',return_json=True)
	filter = filterStatusWithMedia(results)
	media = mediaInfo(results,searchTerm)
	for i in media:
		imgIdList.append(i["imgId"])
	finalData[searchTerm] = filter
	finalMedia[searchTerm] = media
	finalImages[searchTerm] = imgIdList
	final[searchTerm] = [finalData,finalMedia,finalImages]
	return final

def createUrlFile(media):
	tempList = []
	for i in media:
		print i
		for j in media[i]:
			tempList.append(j["url"])
	with open('urlList.txt', 'w') as outfile:
	    json.dump(tempList, outfile,sort_keys=True, indent=4)


api = twitter.Api(consumer_key='enter yours here',
                  consumer_secret='enter yours here',
                  access_token_key='enter yours here',
                  access_token_secret='enter yours here')

filter = []
media = []
finalData = {}
finalMedia = {}
finalImages = {}
imgIdList = []
final = {}
searchTerms = ["Grevy Zebra","Plains Zebra","Reticulated Giraffe","Rothschild Giraffe", "Masai Giraffe", "Tiger","Cheetah", "Savannah Elephant"]

for i in searchTerms:
	final = gatherData(api, i,final)

for i in searchTerms:
	finalData[i] = final[i][0][i]
	finalMedia[i] = final[i][1][i]
	finalImages[i] = final[i][2][i]

createUrlFile(finalMedia)

with open('data.txt', 'w') as outfile:
	json.dump(finalData, outfile,sort_keys=True, indent=4)

with open('media.txt', 'w') as outfile:
    json.dump(finalMedia, outfile,sort_keys=True, indent=4)

with open('imageList.txt', 'w') as outfile:
    json.dump(finalImages, outfile,sort_keys=True, indent=4)

