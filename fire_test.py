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

def check_avail(date):
  
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


if __name__ == '__main__':
    check_avail(15)