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
        '''
        :param obj_name: This is the name of the firewall object
        :return: fwobj dictionary from the list of dictionaries - fwobjs.
        the lambda function evaluations if there is a value of key name
        that matches the obj_name queried, if there is return the dictionary fwobj.
        else returns None.
        Do note that filter returns a filter object not a list, hence next() is used.
        The next() function gets the first item that matches in filter function.
        next() function throws an exception if object is Nonetype, hence the default
        value None is put as an argument in next() so that if there is no value,
        next() will not throw an exception.
        '''
        fwobj = next(filter(lambda x: x["name"] == obj_name, fwobjs), None)
        return {
            "object": fwobj
        }, 200 if fwobj is not None else 404

    # post method
    def post(self, obj_name):
        # firewall object has to be unique.
        # if firewall object ip address has to be modified then should call a put method.
        # put method is currently not implemented.
        if next(filter(lambda x: x['name'] == obj_name, fwobjs), None):
            return {
                "message": f"Firewall object {obj_name} already exist."
            }, 400
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