import twitter
import json
import collections
import datetime

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
	img["description"] = pic["text"]
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
	img["description"] = pic["text"]
	img["positionInStatus"] = index + 1
	img["searchTermUsed"] = term
	return img

def filterStatusWithMedia(results):
	filter = []
	for i in results["statuses"]:
		if "media" in i["entities"]:
			filter.append(i)
	return filter

def getUsers(results):
	users = []
	for i in results["statuses"]:
		if "media" in i["entities"]:
			users.append(photographerDetail(pic = i))
	return users

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
	users = getUsers(results)
	for i in media:
		imgIdList.append(i["imgId"])
	finalData[searchTerm] = filter
	finalMedia[searchTerm] = media
	finalImages[searchTerm] = imgIdList
	finalUsers[searchTerm] = users
	final[searchTerm] = [finalData,finalMedia,finalImages,finalUsers]
	return final

def createUrlFile(media):
	tempList = []
	for i in media:
		print i
		for j in media[i]:
			tempList.append(j["url"])
	with open('urlList.txt', 'w') as outfile:
	    json.dump(tempList, outfile,sort_keys=True, indent=4)

def photographerDetail(pic):
	user = collections.OrderedDict()
	user["memberSince"] = pic["user"]["created_at"]
	user["description"] = pic["user"]["description"]
	user["numFollowers"] = pic["user"]["followers_count"]
	user["id"] = pic["user"]["id"]
	user["name"] = pic["user"]["name"]
	user["isVerified"] = pic["user"]["verified"]
	user["homeTown"] = pic["user"]["location"]
	user["numStatus"] = pic["user"]["statuses_count"]
	user["imgId"] = pic["entities"]["media"][0]["id"]
	return user

api = twitter.Api(consumer_key='enter yours here',
                  consumer_secret='enter yours here',
                  access_token_key='enter yours here',
                  access_token_secret='enter yours here')

filter = []
media = []
finalData = {}
finalMedia = {}
finalImages = {}
finalUsers = {}
imgIdList = []
final = {}
searchTerms = ["Grevy Zebra","Plains Zebra","Reticulated Giraffe","Rothschild Giraffe", "Masai Giraffe", "Tiger","Cheetah", "Savannah Elephant","Lion","Indonesian Rhino","White Rhino", "Black Rhino", "Whale Shark", "Humpback Whales"]

for i in searchTerms:
	final = gatherData(api, i,final)

for i in searchTerms:
	finalData[i] = final[i][0][i]
	finalMedia[i] = final[i][1][i]
	finalImages[i] = final[i][2][i]
	finalUsers[i] = final[i][3][i]

createUrlFile(finalMedia)

with open('data - ' + datetime.datetime.now().strftime("%m-%d-%y") + '.txt', 'w') as outfile:
	json.dump(finalData, outfile,sort_keys=True, indent=4)

with open('media - ' + datetime.datetime.now().strftime("%m-%d-%y") + '.txt', 'w') as outfile:
    json.dump(finalMedia, outfile,sort_keys=True, indent=4)

with open('imageList - ' + datetime.datetime.now().strftime("%m-%d-%y") + '.txt', 'w') as outfile:
    json.dump(finalImages, outfile,sort_keys=True, indent=4)

with open('usersList - ' + datetime.datetime.now().strftime("%m-%d-%y") + '.txt', 'w') as outfile:
    json.dump(finalUsers, outfile,sort_keys=True, indent=4)

