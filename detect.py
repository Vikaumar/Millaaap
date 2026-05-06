import requests
headers = {
	"app_id": "4985f625",
	"app_key": "aa9e5d2ec3b00306b2d9588c3a25d68e"
	}
data={
	"image":"https://pbs.twimg.com/profile_images/1150960759838371841/UhAIoM9q_400x400.jpg",
	"subject_id":"Elizabeth",
	"gallery_name":"MyGallery"
	}
url = "http://api.kairos.com/detect"
	# make request
r = requests.post(url, data=data, headers=headers)
print(r.content)