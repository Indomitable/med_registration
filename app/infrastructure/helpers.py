import json
from django.http.response import HttpResponse


def json_response(data):
    json_data = json.dumps(data, indent=4)
    return HttpResponse(json_data, content_type="application/json")