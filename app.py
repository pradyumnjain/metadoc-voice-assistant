from flask import Flask
from flask_restful import Resource, Api, reqparse
# from quickstart import set_google_reminder

app = Flask(__name__)
api = Api(app)


import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAZUYBEQi1kY64T30oetYfC3b4ZyhBUoEk",
    "authDomain": "marvel-cinematic-univers-55f23.firebaseapp.com",
    "databaseURL": "https://marvel-cinematic-univers-55f23.firebaseio.com",
    "projectId": "marvel-cinematic-univers-55f23",
    "storageBucket": "marvel-cinematic-univers-55f23.appspot.com",
    "messagingSenderId": "144181365638",
    "appId": "1:144181365638:web:a9e434f5b10120978bfa07"
    }

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class checkslots(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date',type=str,required=True,help="cant be blank")
        data = parser.parse_args()
        date = data['date']
        for dat in date:
            try:
                if type(int(dat)) == int:
                    date = int(dat)
            except:
                continue
        db = firebase.database()
        try:
            all_dates = db.child("date_slots").get()
            for dat in all_dates.each():
                cur = dat.val()
                if cur['date'] == '{}'.format(date):
                    flag = 1
                    break
                else:
                    flag=0
        if flag==1:
            print(1)
        else:
            data = {"date":"{}".format(date),"slots":{"3pm":"available","4pm":"available","5pm":"available"}}
            db.child("date_slots").child("{}".format(date)).set(data)
            return {"availability":"available slots are 3 to 4 pm , 4 to 5 pm , 5 to 6 pm "}
    except:
        data = {"date":"{}".format(date),"slots":{"3pm":"available","4pm":"available","5pm":"available"}}
        db.child("date_slots").child("{}".format(date)).set(data)
        print(2)
        return {"availability":"available slots are 3 to 4 pm , 4 to 5 pm , 5 to 6 pm "}


class checkdate(Resource):
    def post(self):
        parser =  reqparse.RequestParser()
        parser.add_argument('date',type=str,required=True,help="cant be blank")
        data = parser.parse_args()
        date = data['date']
        date = date.split(" ")
        for dat in date:
            try:
                if type(int(dat)) == int:
                    return {"validity":"valid"}
            except:
                continue
        return {"validity":"invalid"}


class testinfo(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('disease',type=str,required=True,help='cant be blank')
        try:
            parser.add_argument('date',type=str,required=True,help='cant be blank')
        except:
            print("invalid data type")


        data = parser.parse_args()

        print(data['disease'])
        print(data['date'])
        return {"status":"successfull"}
        



api.add_resource(checkdate,'/checkdate')
api.add_resource(HelloWorld, '/')
api.add_resource(testinfo,'/test')
api.add_resource(checkslots,'/checkslots')

if __name__ == '__main__':
    app.run(debug=True)