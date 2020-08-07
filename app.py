from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

urls = []
wikiLink = []
data = []
date = []

class Searches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100)) 
    content2 = db.Column(db.String(100)) 

    #def __repr__(self):


@app.route('/', methods=['POST', 'GET'])
def index():
    wikiLink.clear()
    urls.clear()
    data.clear()
    date.clear()
    return render_template('index.html')

@app.route('/hello', methods=["POST", 'GET'])
def hello():
    urls = []
    wikiLink = []
    data = []
    date = []
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found")

    test1 = request.form.get("name")
    test = request.form.get("name") + "tv show"
    

    # gets first 10 links on google search
    for j in search(test, tld="co.in", num=10, stop=10, pause=2):  
        urls.append(j)

    x = 'en.wikipedia.org'
 
    wikiLink = [i for i in urls if x in i]

    # special output if "parks and rec"

    try:
        if wikiLink[0] == "https://en.wikipedia.org/wiki/Parks_and_Recreation":
            release = "April 9, 2009-February 24, 2015"
            return render_template("hello.html", name=test1, release=release)
            wikiLink.clear()
            urls.clear()
        else:
            source = requests.get(wikiLink[0]).text

            soup = BeautifulSoup(source, 'lxml')
                             
            body = soup.find('body')

            mwbody = body.find('div', class_='mw-body')

            content = mwbody.find('div', id='bodyContent')

            content2 = content.find('div', class_='mw-content-ltr')

            content3 = content2.find('div', class_='mw-parser-output')

            table = content3.find('table', class_='infobox vevent')

            tbody = table.find('tbody')

            # To get to "Original release" section of column

            # try using find and find_all to look for "Original release" string
            data = []
            trTags = tbody.find_all('tr')
            for trTags in trTags:
                data.append(trTags.text)
                #print(trTags.text)
          
            i = 0
            x = 'Original release'

            temp = [i for i in data if x in i]
            temp2 = str(temp).split('e', 3)
            temp2.pop(0)
            temp2.pop(0)
            temp2.pop(0)
            temp3 = str(temp2).split('\\xa0')
            temp4 = str(temp3).split('\\')
            date = [temp4[0], temp4[4]]
            start = str(date[0]).replace('[\'["', '')
            end = date[1].replace('\', \'','')
            final = start + end

            new_task = Searches(content=test1)
            db.session.add(new_task)
            db.session.commit()

            another_task= Searches(content2=final)
            db.session.add(another_task)
            db.session.commit()  
            

            tasks = Searches.query.filter_by(content=test1).first()
            tasks2 = Searches.query.filter_by(content2=final).first()

            moreTasks = Searches.query.order_by(Searches.content).all()
            moreTasks2 = Searches.query.order_by(Searches.content2).all()

            
            return render_template("hello.html", name=test1, release=final, moreTasks=moreTasks, moreTasks2=moreTasks2)

    except:  
        return render_template('error.html')
        
@app.route('/error', methods=['POST'])
def error():
    wikiLink.clear()
    urls.clear()
    data.clear()
    date.clear()
    return render_template('index.html')

@app.route('/clear', methods=['POST'])
def clear():

    moreTasks = Searches.query.order_by(Searches.content).all()
    moreTasks2 = Searches.query.order_by(Searches.content2).all()

    for tasks in moreTasks:
        db.session.delete(tasks)
        db.session.commit()

    for tasks2 in moreTasks2:
        db.session.delete(tasks2)
        db.session.commit()

    return render_template('hello.html')
        
           

if __name__ == "__main__":
    app.run(debug=True)

# Put onto Google CLOUD as a W E B S I T E
# If error, try again and save search response to fix later, basically "how to handle those freakin errors"
# Figure out SQLAlchemy / Saves too many searches in a weird way

# To get into env, .\env\Scripts\activate