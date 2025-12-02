import json
from urllib.request import urlopen
from flask import Flask , render_template,request,redirect,session,url_for
import requests
import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload,MediaFileUpload
import shutil

# Google Authention Scopes
SCOPES = ['https://www.googleapis.com/auth/drive',"https://www.googleapis.com/auth/youtube.upload"]
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'xDD'

#convert credentials to dict to store it in session later
def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

#list all trailers from iTunes 
@app.route('/list')
def trailer_list():
    #emepty list for HD trailers
    trailers_HD = []

    #request apple all trailers in json sorted by generes     
    request =requests.get('http://trailers.apple.com/trailers/home/feeds/genres.json')
    trailers = request.json()

    # add only HD trailer to list
    for trailer in trailers:
        for clip in trailer['trailers']:
            if clip['hd'] == True:
                trailers_HD.append(trailer)
                break
    
    # TODO make pages

    return render_template('trailers_list.html', traliers_HD=trailers_HD)


#add trailer clip to google drive
@app.route('/drive/<path:subpath>')
def save_to_drive(subpath):
    #request specific trailer json
    r = requests.get('https://trailers.apple.com/'+subpath+'data/page.json')
    trailer = r.json()

    #get url for trail clip
    trailer_url = trailer['clips'][0]['versions']['enus']['sizes']['sd']['srcAlt']

    #redirect for google script to handle upload to drive
    return redirect('https://script.google.com/macros/s/AKfycbyVG_-ZlgJOt1u9TDc2ME5F8-eOJq51hcWsoHEIFjgFGatN18o/exec?url='+ trailer_url)


@app.route('/MyDrive')
def get_mydrive():
    #check if user logged with google
    if 'credentials' not in session:
        return render_template('login.html')

    else:
        #get credentials from session
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])    
        #build service    
        service = build('drive', 'v3',credentials=credentials)

        #get a list of all folder thaat name Apple Trailers
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)",
            q="mimeType ='application/vnd.google-apps.folder' and name contains 'Apple Trailers'").execute()
        folders = results.get('files', [])
        #check if folder exist
        
        if not folders:
            return "Can't find Apple Trailers folder"

        #get Apple Trailers folder ID   
        folder_id = folders[0]['id']

        #search for all file that in folder Apple Trailers and type video
        results_in_folder = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name,mimeType,webContentLink,thumbnailLink,size)",
            q=f"mimeType contains 'video' and '{folder_id}' in parents").execute()
        files = results_in_folder.get('files', [])

        return render_template('mydrive.html', videos = files)


@app.route('/login')
def login():
    # cwd = os.getcwd()

    #send client credentials to google 
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', SCOPES)
    # set url that user redirect into after successfully login with google    
    flow.redirect_uri = url_for('auth', _external=True)  
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    session['state'] = state

    #redirect user to google to login
    return redirect(authorization_url)



@app.route('/auth')
def auth():
    state = session['state']
    #set flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', SCOPES, state=state)
    flow.redirect_uri = url_for('auth', _external=True)

    #get response from google
    authorization_response = request.url       
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    
    #save credentials in session
    session['credentials'] = credentials_to_dict(credentials)

    return redirect('/MyDrive')





@app.route('/youtube/<string:file_id>')
def upload(file_id):
    url = request.args.get('url', '')
    name = request.args.get('name', '')
    return render_template('upload.html',url =url , name=name)


@app.route('/youtube/sent', methods = ['POST'])
def upload_youtube():
    #check if user logged or not
    if 'credentials' not in session:
        return render_template('login.html')

    #get submit video detalis
    url = request.form.get("url")
    name = request.form.get("name")
    title = request.form.get("title")
    description = request.form.get("description")
    categoryId = request.form.get("categoryId")

    #download video in server
    with requests.get(url, stream=True) as r:
        with open(name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    #set youtube api detalis
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = build('youtube', 'v3',credentials=credentials)
    body = {'snippet': {'title': title,'description': description,'tags': 'ahmed ,api','categoryId': categoryId},'status': {'privacyStatus': 'unlisted'}}

    #upload video to youtube
    insert_request = service.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(name ,chunksize=-1, resumable=True)
    ).execute()  


    return 'success'







if __name__ == '__main__':
    app.run(debug=True)
