import requests
import os
import hashlib
from PIL import Image
from requests.exceptions import RequestException
from src.data_store import data_store
from src.config import url

from src.error import InputError

def download_photo(auth_user_id, img_url):
	try:
		image_response = requests.get(img_url)
	except RequestException as invalid_url:
		raise InputError('Invalid URL was entered') from invalid_url

	if image_response.status_code != 200:
		raise InputError('Invalid image, could not be uploaded')
	elif 'image/jpeg' not in image_response.headers['Content-Type']:
		raise InputError('Invalid image, could not be uploaded')
	
	salted = f'{auth_user_id}namakishqka'
	hashed_id = hashlib.md5(salted.encode())
	file_id = hashed_id.hexdigest()[:9]
	unique_name = f'{os.getcwd()}/imgurl/{file_id}.jpg'

	with open(unique_name, 'wb+') as outfile:
		outfile.write(image_response.content)

	return (unique_name, file_id)

def upload_photo_v1(auth_user_id, img_url, x_start, y_start, x_end, y_end):
	'''
	Description:
		- Given a URL of an image on the internet, crops the image within bounds 
		(x_start, y_start) and (x_end, y_end). Position (0,0) is the top left. 

    Parameters:
		auth_user_id: user uploading the photo
		img_url: url that indicates the photo being uploaded
		x_start: start of horizontal bound
		y_start: start of vertical bound
		x_end: end of horizontal bound
		y_end: end of vertical bound

    Return:
		None

    Exceptions:
	InputError when any of:
        - img_url returns an HTTP status other than 200
        - any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL
        - x_end is less than x_start or y_end is less than y_start
        - image uploaded is not a JPG

    Changes to data store:
		modifies users
	'''
	downloaded_data = download_photo(auth_user_id, img_url)
	local_url = downloaded_data[0]
	file_id = downloaded_data[1]
	
	profile_pic = Image.open(local_url)
	if profile_pic.format != 'JPEG':
		raise InputError('The profile picture must be a jpeg file')

	width, height = profile_pic.size

	if x_start not in range(width) or x_end not in range(width):
		raise InputError('The crop width is invalid')

	if y_start not in range(height) or y_end not in range(height):
		raise InputError('The crop height is invalid')

	if x_start > x_end or y_start > y_end:
		raise InputError('The crop start cannot be greater than the end')

	cropped = profile_pic.crop((x_start, y_start, x_end, y_end))
	cropped.save(local_url)

	store = data_store.get()
	users = store['users']
	users[auth_user_id]['profile_img_url'] = f'{url}imgurl/{file_id}.jpg'

	channels = store['channels']
	dms = store['dms']

	for channel in channels:
		for user in channel['all_members']:
			if user['u_id'] == auth_user_id:
				user['profile_img_url'] = f'{url}imgurl/{file_id}.jpg'

		for user in channel['owner_members']:
			if user['u_id'] == auth_user_id:
				user['profile_img_url'] = f'{url}imgurl/{file_id}.jpg'

	for dm in dms:
		for user in dm['all_members']:
			if user['u_id'] == auth_user_id:
				user['profile_img_url'] = f'{url}imgurl/{file_id}.jpg'

		for user in dm['owner_members']:
			if user['u_id'] == auth_user_id:
				user['profile_img_url'] = f'{url}imgurl/{file_id}.jpg'

	store['channels'] = channels
	store['dms'] = dms
	store['users'] = users
	data_store.set(store)
	return {}