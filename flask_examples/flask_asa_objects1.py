'''
This is a flask practice script.
The purpose is also to find out if the api uri suits my current needs or not.
This is also to evaluate with the team if the uri makes sense.
'''

# request is required to get the json body from post method.
from flask import Flask, request
from flask_restful import Resource, Api

# usage example of flask and flask_restful
app = Flask(__name__)
api = Api(app)

# for capturing the objects
fwobjs = []


# each class is an api resource.
# this resource get and post one object.
# each firewall object has an ip address.
class AsaObject(Resource):
    # get method.
    def get(self, obj_name):
        # search through the list of firewall objects until a match is found.
        for fwobj in fwobjs:
            # return the object dictionary if found.
            if fwobj['name'] == obj_name:
                return fwobj, 200
        # else not found, 404.
        return {
            "name": None
        }, 404
    # post method
    def post(self, obj_name):
        # read the json body submitted from the client such as curl, postman or insomnia.
        # request.get_json only parse the json body, if the body is not json an exception is thrown.
        # silent=True will prevent exception from happening, invalid json can still be posted but
        # no exception, instead 404 not found is returned.
        data = request.get_json(silent=True)
        # parse the json data and store into fw obj, then append to the list.
        fwobj = {"name": obj_name, "ip_address": data.get('ip_address', None)}
        fwobjs.append(fwobj)
        # 201 post ok
        return fwobj, 201

# this resource get the list of asa object dictionaries.
class AsaObjectList(Resource):
    def get(self):
        # returns a list of dictionaries - fwobjs.
        return {
            "asa_objects": fwobjs
        }

# same as http://127.0.0.1:5000/asa/object/<name>
api.add_resource(AsaObject, '/asa/object/<string:obj_name>')

# same as http://127.0.0.1:5000/asa/objects
api.add_resource(AsaObjectList, "/asa/objects")

# default is port=5000, debug=False
app.run()