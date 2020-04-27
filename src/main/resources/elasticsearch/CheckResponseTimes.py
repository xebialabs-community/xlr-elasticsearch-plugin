import json
import time

endTime = str(time.time() + timePeriod)
lastHits = []
totalResponseTime = 0
processed = 0

uri = "/{}/_search".format(index)
uri += "?size=1000&sort={0}:desc&_source_includes={0},{1}".format(
    timestampField, responseTimeField
)
if query not in ["", None]:
    uri += "&q={}".format(query)

request = HttpRequest(server, username, password)
response = request.get(uri, body="", contentType="application/json")

# Do not evaluate historic hits
if response.isSuccessful():
    hits = json.loads(response.getResponse())["hits"]["hits"]
    for hit in hits:
        lastHits.append(hit["_id"])
else:
    response.errorDump()
    raise Exception("Unable to get hits")

task.setStatusLine("Inspecting response times...")
task.schedule("elasticsearch/CheckResponseTimesInspecting.py")
