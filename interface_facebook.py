#1 - Create app at https://developers.facebook.com/docs/apps/register/
#2 - Get App id and App secret (Settings on the developers app page) and put them at env.py

from facepy import GraphAPI
import webbrowser
import BaseHTTPServer
import urlparse
import ssl
import os

from env import facebook_oauth_url, user_id, ff_token
facebook_token = '-'

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        isdatoken = True
        o = urlparse.urlparse(s.path)
        xx = urlparse.parse_qs(o.query)
        try:
            datoken = xx['access_token']
        except Exception as e:
            isdatoken = False
        """Respond to a GET request."""
        if not isdatoken:
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("<html><head><title>Loading</title></head>")
            s.wfile.write('<body onload="myFunction();">')
            s.wfile.write('<p id="demo"></p>')
            s.wfile.write("<script>")
            s.wfile.write("function myFunction() {")
            s.wfile.write("var x = document.URL;")
            s.wfile.write('var userText = "Something went wrong, please try again";')
            s.wfile.write('if (x.includes("access_token")) {userText = "Facebook properly configurated, you can close this page."};')
            s.wfile.write('document.getElementById("demo").innerHTML = userText;')
            s.wfile.write('var res = x.replace("login#", "toktok?");')
            s.wfile.write('fetch(res).then(function(response) {});')
            s.wfile.write("}")
            s.wfile.write("</script>")
            s.wfile.write("</body></html>")
        else:
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,
                                           user_id +"-facebook.token")
            f = open(credential_path, 'w')
            f.write(datoken[0])
            f.close()


def wait_for_request(server_class=BaseHTTPServer.HTTPServer,
                     handler_class=MyHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./Certificates.pem', server_side=True)
    return httpd

def getPath():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    return os.path.join(credential_dir, user_id +"-facebook.token")

def browserOauth():
    webbrowser.open(facebook_oauth_url, new=2) 
    http_server = wait_for_request()
    http_server.handle_request()
    http_server.handle_request()

def get_credentials(forceLogin):
    if forceLogin:
        browserOauth()
    try:
        f = open(getPath(), 'r')
    except Exception as e:
        browserOauth()
        f = open(getPath(), 'r')
    ret = f.readline()
    f.close()
    while (len(ret) < 4):
        browserOauth()
        f = open(getPath(), 'r')
        ret = f.readline()
        f.close()
    return ret
    

def postVideo_wall(title, message, path):
    graph = GraphAPI(facebook_token)
    try:
        video_id = graph.post(
            path = 'me/videos',
            source = open(path),
            title = title,
            description = message
        )
    except Exception as e:
        return dict(success=False, message=e)
    return dict(success=True, message='video posted correctly')

def postVideo_page(title, message, path, pageName):
    graph = GraphAPI(getPageToken(pageName))
    try:
        graph.post(
            path =  "me/videos",
            source = open(path),
            title = title,
            description = message
        )
    except Exception as e:
        return dict(success=False, message=e)
    return dict(success=True, message='video posted correctly')

def getPageToken (name):
    graph = GraphAPI(facebook_token)
    try:
        pages = graph.get(
            path = "me/accounts"
        )
    except Exception as e:
        return False
    for page in pages['data']:
        if page['name'] == name:
            return page['access_token']
    return False;

ff_token = get_credentials(False)
facebook_token = ff_token.rstrip()
print postVideo_page('yas 2', 'uploading video from python', '/Users/arnaubennassarformenti/Downloads/Volley_Feroe_cut_min38.30.mp4', 'Dev testing')
