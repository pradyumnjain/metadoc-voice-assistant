from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)



class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


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
        




api.add_resource(HelloWorld, '/')
api.add_resource(testinfo,'/test')

if __name__ == '__main__':
    app.run(debug=True)