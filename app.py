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
        parser =  reqparse.RequestParser()
        parser.add_argument('date',type=str,required=True,help="cant be blank")
        data = parser.parse_args()
        date = data['date']
        date = date.split(" ")
        for dat in date:
            try:
                if type(int(dat)) == int:
                    date = int(dat)
                    break
            except:
                continue
        db = firebase.database()
        try:
            all_dates = db.child("date_slots").get()
            for dat in all_dates.each():
                cur = dat.val()
                if cur['date'] == '{}'.format(date):
                    flag = 1
                    d = cur["slots"]
                    avail = "available slots are from"
                    for val in d.keys():
                        if "available" in d[val]:
                            avail + "{} and".format(val)
                        return {"availability":"{}".format(avail)}


                else:
                    flag=0
            if flag==1:
                pass
            else:
                data = {"date":"{}".format(date),"slots":{"3pm":"available","4pm":"available","5pm":"available"}}
                db.child("date_slots").child("{}".format(date)).set(data)
                return {"availability":"available slots are from 3 pm and 4 pm and 5 pm"}
        except:
            data = {"date":"{}".format(date),"slots":{"3pm":"available","4pm":"available","5pm":"available"}}
            db.child("date_slots").child("{}".format(date)).set(data)
            print(2)
            return {"availability":"available slots are from 3 pm and 4 pm and 5 pm"}


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


class bookslot(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('slot',type=str,required=True,help='cant be blank')
        parser.add_argument('date',type=str,required=True,help='cant be blank')
        data = parser.parse_args()
        date = data['date']
        date = date.split(" ")
        for dat in date:
            try:
                if type(int(dat)) == int:
                    date = int(dat)
                    break
            except:
                continue
        slot = data['slot']
        slot = slot.split(" ")
        for dat in slot:
            try:
                if type(int(dat)) == int:
                    slot = dat
                    break
            except:
                continue
        
        slot =  slot + "pm"

        db =  firebase.database()
        all_dates = db.child("date_slots").get()
        for dat in all_dates.each():
                cur = dat.val()
                if cur['date'] == '{}'.format(date):
                    for k in cur['slots'].keys():
                        if slot in k:
                            cur['slots']['k'] = "taken"
                            break
        db.child("date_slots").child("date").update(cur)
        return {"result":"{}".format(cur)}








        


api.add_resource(bookslot,'/bookslot')
api.add_resource(checkdate,'/checkdate')
api.add_resource(HelloWorld, '/')
api.add_resource(testinfo,'/test')
api.add_resource(checkslots,'/checkslots')

if __name__ == '__main__':
    app.run(debug=True)