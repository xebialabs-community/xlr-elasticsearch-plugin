import time
import json


uri = "/{}/_search".format(index)
uri += "?size={0}&sort={1}:desc&_source_includes={1},{2}".format(
    maxCount, timestampField, responseField
)
if query not in ["", None]:
    uri += "&q={}".format(query)

request = HttpRequest(server, username, password)
response = request.get(uri, body="", contentType="application/json")

if response.isSuccessful():
    rawData = json.loads(response.getResponse())
else:
    response.errorDump()
    raise Exception("Unable to get hits from elasticsearch")

data = {
    "rawData": rawData,
    "timestampKeyName": timestampField,
    "responseKeyName": responseField,
    "selectedTimespan": units,
}
