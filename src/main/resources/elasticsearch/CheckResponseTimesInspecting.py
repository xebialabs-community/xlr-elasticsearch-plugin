import time
import json

uri = "/{}/_search".format(index)
uri += "?size=1000&sort={0}:desc&_source_includes={0},{1}".format(
    timestampField, responseTimeField
)
if query not in ["", None]:
    uri += "&q={}".format(query)

request = HttpRequest(server, username, password)
response = request.get(uri, body="", contentType="application/json")

if response.isSuccessful():
    hits = json.loads(response.getResponse())["hits"]["hits"]
    for hit in hits:
        if hit["_id"] not in lastHits:
            totalResponseTime += int(hit["_source"][responseTimeField])
            processed += 1
    lastHits = [hit["_id"] for hit in hits]
else:
    response.errorDump()
    raise Exception("Unable to get hits")

if processed > 0 and float(totalResponseTime)/processed > float(threshold):
    raise Exception("Exceeded permitted threshold for average response times: %.2f > %.2f" % (float(totalResponseTime)/processed, float(threshold)))

if time.time() > float(endTime):
    if processed > 0:
        print("Average response time of %.2f across %s hits" % (float(totalResponseTime)/processed, processed))
    else:
        print("No hits processed")
    task.setStatusLine("Checked")
else:
    task.setStatusLine("Inspecting response times...")
    task.schedule("elasticsearch/CheckResponseTimesInspecting.py", 1)
