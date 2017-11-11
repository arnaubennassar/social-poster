#1 - Create app at https://developers.facebook.com/docs/apps/register/
#2 - Get App id and App secret (Settings on the developers app page) and put them at env.py

from facepy import GraphAPI
import robobrowser
import re

from env import facebook_password, facebook_email


# def getAccessToken():
#     browser = robobrowser.RoboBrowser(
#         history=True,
#         user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
#     )

#     browser.open('https://m.facebook.com')
#     form = browser.get_form(id='login_form')

#     form['email'].value = facebook_email
#     form['pass'].value = facebook_password

#     browser.submit_form(form)
#     ##get access token from the html response##
#     access_token = 'ja - ja'#re.search(r"access_token=([\w\d]+)", browser.response.content.decode()).groups()[0]
#     return access_token

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://www.facebook.com/v2.11/dialog/oauth?client_id=144624289508638&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=publish_actions,publish_pages"

def get_access_token():
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    ##submit login form##
    f = s.get_form(id='login_form')
    f["pass"] = facebook_password
    f["email"] = facebook_email
    s.submit_form(f)
    ##get access token from the html response##
    return s.response.content.decode()
    #access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]

    return access_token

def postVideo(message, path):
    print get_access_token()
    #print getAccessToken()
    # graph = GraphAPI(getAccessToken())
    # # Post a photo of a parrot
    # graph.post(
    #     path = 'me/photos',
    #     source = open(path)
    # )
    return

postVideo('', '/Users/arnaubennassarformenti/Downloads/white-gloss-tile-board-709106-64_300.jpg')
