from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient

import json
import os
import logging
from bson import ObjectId

logger = logging.getLogger(__name__);
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def distinct(request):
    m = MongoClient(os.environ["MongoHost"]);
    items = m.girder.item;
    response = {}
    print("a bunch of logggin incoming");
    for field in request.GET.getlist("field_names[]"):
        print("Field "+field+" start");
        response[field] = items.distinct(field);
        print("Field "+field+" end");
    res = JsonResponse(response, encoder=JSONEncoder);
    res["Access-Control-Allow-Origin"] = "http://10.104.6.45"
    return res
