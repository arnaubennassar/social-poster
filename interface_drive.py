#https://developers.google.com/drive/v3/web/quickstart/python


from __future__ import print_function
from env import drive_app_name, user_id

import httplib2
import os

from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'drive_client_secret.json'
APPLICATION_NAME = drive_app_name
def callback(request_id, response, exception):
	return

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   user_id +"-drive-credentials.json")

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def uploadVideo(title, path):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    try:
    	media = MediaFileUpload(path, mimetype='video/mp4', resumable=True)
    except Exception as e:
    	return dict(success=False, message=e)
    try:
    	file = service.files().create(body={'name': title}, media_body=media, fields='id').execute()
    except Exception as e:
    	return dict(success=False, message=e)
    return dict(success=True, message=file.get('id'), service=service)

def shareVideo(title, path, recievers):
	uploadedVideo = uploadVideo(title, path)
	if not uploadedVideo['success']:
		return uploadedVideo
	file_id = uploadedVideo['message']
	service = uploadedVideo['service']
	batch = service.new_batch_http_request(callback=callback)
	for reciever in recievers:
		user_permission = {
		    'type': 'user',
		    'role': 'writer',
		    'emailAddress': reciever
		}
		batch.add(service.permissions().create(
		        fileId=file_id,
		        body=user_permission,
		        fields='id',
		))
	try:
		batch.execute()
	except Exception as e:
		return dict(success=False, message=e)
	return dict(success=True, message='succesfully shared video using Google Drive')


