#1 - Create app at https://developers.facebook.com/docs/apps/register/
#2 - Get App id and App secret (Settings on the developers app page) and put them at env.py

from facepy import GraphAPI
from facepy.exceptions import OAuthError
import urllib2
# import robobrowser
# import re


from env import facebook_access_token

FB_AUTH = "https://www.facebook.com/v2.11/dialog/oauth?client_id=144624289508638&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=publish_actions,publish_pages"

def postVideo_wall(title, message, path):
    graph = GraphAPI(facebook_access_token)
    try:
        video_id = graph.post(
            path = 'me/videos',
            source = open(path),
            title = title,
            description = message
        )
    except OAuthError as e:
        if e.code == 190:
            print 'invalid token, please get the token here:'
            print FB_AUTH
            return False
        print 'ERROR: '
        print e
        return False
    return True
def postVideo_page(title, message, path, pageName):
    graph = GraphAPI(getPageToken(pageName))
    try:
        graph.post(
            path =  "me/videos",
            source = open(path),
            title = title,
            description = message
        )
    except OAuthError as e:
        if e.code == 190:
            print 'invalid token, please get the token here:'
            print FB_AUTH
            return False
        print 'ERROR: '
        print e
        return False
    return True
def getPageToken (name):
    graph = GraphAPI(facebook_access_token)
    try:
        pages = graph.get(
            path = "me/accounts"
        )
    except OAuthError as e:
        if e.code == 190:
            print 'invalid token, please get the token here:'
            print FB_AUTH
            return False
        print 'ERROR: '
        print e
        return False
    for page in pages['data']:
        if page['name'] == name:
            return page['access_token']
    print "You are not admin of "+name
    return False;

print postVideo_page('yas 2', 'uploading video from python', '/Users/arnaubennassarformenti/Downloads/Volley_Feroe_cut_min38.30.mp4', 'Dev testing')
