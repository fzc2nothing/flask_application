# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, render_template, request, session, redirect
from google.cloud import datastore
from google.oauth2 import id_token

import datetime
import sys
import requests

datastore_client = datastore.Client()
DEFAULT_KEY = 'guestbook-main'
key_name2 = DEFAULT_KEY

app = Flask(__name__)

app.secret_key = b'lkjadfsj009(*02347@!$&'

"""
User class I created, serves as a placeholder demonstrator
to store google user info
"""

# write new message to guestbook
# def store_greeting(message, username, email, dt, kn):
#     entity = datastore.Entity(key=datastore_client.key(kn))
#     entity.update({
#         'message': message,
#         'timestamp': dt,
#         'username': username,
#         'email': email
#     })

#     datastore_client.put(entity)

# use this function to store the game comes from

def store_shopping_games(message, ESRB, platform, developer, year,price,username, email, gameid, dt, kn):
    entity2 = datastore.Entity(key=datastore_client.key(email))
    entity2.update({
        'message': message,
        'ESRB' : ESRB,
        'platform' : platform,
        'developer' : developer,
        'year' : year,
        'price' : price,
        'timestamp': dt,
        'username': username,
        'email': email,
        'zeroid' : gameid
        
    })

    datastore_client.put(entity2)

def store_record_games(message, ESRB, platform, developer, year,price,username, email, dt, kn):
    entity3 = datastore.Entity(key=datastore_client.key(username))
    entity3.update({
        'message': message,
        'ESRB' : ESRB,
        'platform' : platform,
        'developer' : developer,
        'year' : year,
        'price' : price,
        'timestamp': dt,
        'username': username,
        'email': email,
        
    })

    datastore_client.put(entity3)






def store_games(message, ESRB, platform, developer, year,price,username, email, dt, kn):
    entity = datastore.Entity(key=datastore_client.key(kn))
    entity.update({
        'message': message,
        'ESRB' : ESRB,
        'platform' : platform,
        'developer' : developer,
        'year' : year,
        'price' : price,
        'timestamp': dt,
        'username': username,
        'email': email
    })

    datastore_client.put(entity)

# fetch most recent 'limit' number of messages from guestbook
def fetch_games(kn):
    query = datastore_client.query(kind=kn)
    #query.order = ['-timestamp']

    games = query.fetch()

    return games



def search_entity(kn_genre, _title,_rating,_platform,_developer,_year_release, _price):
    queries = datastore_client.query(kind = kn_genre)
    queries.order = ['-timestamp']
    
    greetings = list(queries.fetch())
    results = list()
    for query in greetings:
        if(query['message'].find(_title)!=-1 and query['ESRB'].find(_rating)!=-1 and query['platform'].find(_platform)!=-1 and query['developer'].find(_developer)!=-1 and query['year']==_year_release and query['price'].find(_price)!=-1):
            results.append(query)
    return results

# main page HTTP request processing
@app.route('/')
def root():

    

    return render_template(
        'index.html')

@app.route('/index')
def index():
   return render_template(
        'index.html')



@app.route('/firstPage', methods=['GET', 'POST'])
def firstPage():
    key_name = DEFAULT_KEY

    flag = 2

    if 'username' in session:
        username = session['username'] 
    else:
        username = ''

    if 'email' in session:
        useremail = session['email'] 
    else:
        useremail = ''

    
    # If POST, store the new message into Datastore in the appropriate guestbook
    if request.method == 'POST':

        if request.form['content']=='' or request.form['ESRB']=='' or request.form['platform'] =='' or request.form['developer'] =='' or request.form['year'] =='':
            flag = 0
        else:
            flag = 1
            key_name = request.form['guestbook_name'].lower()
            store_games(request.form['content'],request.form['ESRB'],request.form['platform'],request.form['developer'],request.form['year'], request.form['price'],username, useremail, datetime.datetime.now(), key_name)

    # Fetch the most recent 10 messages from the appropriate guestbook in Datastore
    games = fetch_games(key_name)

    return render_template(
        'firstPage.html', games=games, guestbook_name=key_name, flag = flag)

@app.route('/search', methods=['GET', 'POST'])
def search():
    key_name = DEFAULT_KEY
    global key_name2
    games = list()

    mark = 0

    flag = 2

    if 'username' in session:
        username = session['username'] 
    else:
        username = ''

    if 'email' in session:
        useremail = session['email'] 
    else:
        useremail = ''

    # If POST, store the new message into Datastore in the appropriate guestbook
    if request.method == 'POST':

        

        if request.form['put'] == "Entergameinfo":

            

            key_name2 = request.form['guestbook_name'].lower()
            

            if request.form['content']=='' and request.form['ESRB']=='' and request.form['platform'] =='' and request.form['developer'] =='' and request.form['year'] =='':
                flag = 0
            else:
                flag = 1
                games = search_entity(key_name2, request.form['content'], request.form['ESRB'], request.form['platform'], request.form['developer'],request.form['year'],request.form['price'])

                # Fetch the most recent 10 messages from the appropriate guestbook in Datastore

        if request.form['put'] == "Intocart":

            

            flag = 1

            id_game = request.form['searchgame']

            

            games2 = fetch_games(key_name2)

            check_games = fetch_games(useremail)

            for game in games2:

                

                if (str(game.id) == id_game):

                    for check_game in check_games:

                        if game.id == check_game['zeroid']:

                            mark = 1
                    if mark == 0:
                        store_shopping_games(game['message'], game['ESRB'], game['platform'], game['developer'], game['year'], game['price'],username, useremail, game.id,datetime.datetime.now(), useremail)
            return redirect("/")

    print(flag)
    return render_template(
    'search.html', games=games, guestbook_name=key_name, flag = flag)


@app.route('/display/<string:genre>', methods=['GET', 'POST'])
def display(genre):

    mark = 0

    emailID = 0

    if 'username' in session:
        username = session['username'] 
    else:
        username = ''

    if 'email' in session:
        useremail = session['email'] 
    else:
        useremail = ''

    

    key_name = useremail

    if request.method == 'POST':

        if useremail == '':

            emailID = 2

        else:

            emailID = 1
            id_games = request.form.getlist('displaygame')

            games = fetch_games(genre)

            checks = fetch_games(useremail)
        

            for game in games:
                for id_game in id_games:
                    if (str(game.id) == id_game):
                        
                        for check in checks:
                            if game.id == check['zeroid']:

                                mark = 1
                        if mark == 0:
                            store_shopping_games(game['message'], game['ESRB'], game['platform'], game['developer'], game['year'], game['price'],username, useremail, game.id,datetime.datetime.now() ,key_name)
    


    games = fetch_games(genre)

    return render_template(
        'display.html',games = games, emailID = emailID)

@app.route('/shoppingcart', methods=['GET', 'POST'])
def shoppingcart():

    mark = 0

    key_name = DEFAULT_KEY
   
    games= list()

    if 'username' in session:
        username = session['username'] 
    else:
        username = ''

    if 'email' in session:
        useremail = session['email'] 
    else:
        useremail = ''

    if request.method == "POST":

        if request.form['cart'] == "Delete":

            id_games = request.form.getlist('displaygame')

            games = fetch_games(useremail)

            for game in games:

                for id_game in id_games:
                    if (str(game.id) == id_game ):
                        datastore_client.delete(game.key)
        
        if request.form['cart'] == "Checkout":

            mark = 1

            games = fetch_games(useremail)

            games2 = fetch_games(useremail)

            for game in games:

                store_record_games(game['message'], game['ESRB'], game['platform'], game['developer'], game['year'], game['price'],username, useremail, datetime.datetime.now() ,key_name)

                

            for game in games2:

                datastore_client.delete(game.key)


   
    games = fetch_games(useremail)

    pricetags = fetch_games(useremail)

    price = 0

    for pricetag in pricetags:
        price = price + int(pricetag['price'])

   

    return render_template(
        'shoppingcart.html',games = games, price = price, mark = mark)

@app.route('/record')
def record():

    emailID = 0

    key_name = DEFAULT_KEY
    
    if 'username' in session:
        username = session['username'] 
    else:
        username = ''

    if 'email' in session:
        useremail = session['email'] 
    else:
        useremail = ''
    if useremail != '':  
        emailID = 1

       
        games = fetch_games(username)

        return render_template(
            'record.html',games = games,emailID = emailID)

    emailID = 2
    return render_template(
            'record.html',games = '' ,emailID = emailID)

@app.route('/login', methods=['POST'])
def login():

    # Decode the incoming data
    token = request.data.decode('utf-8')

    # Send to google for verification and get JSON return values
    verify = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token=" + token)
    
    # Use a session cookie to store the username and email

    session['username'] = verify.json()["name"]
    session['email'] = verify.json()["email"]

    return redirect("/")




@app.route('/logout', methods=['GET'])
def logout():

   

    session['username'] = ''
    session['email'] = ''

    

    return redirect("/")



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
