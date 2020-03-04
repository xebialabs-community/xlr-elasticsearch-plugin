import time
import json


def hitsTable(hits, processed):
    if processed == 0:
        return "No hits processed"
    else:
        return """
| Status Code | Hits |
|:---:|:---:|
| 1xx | %.2f%% |
| 2xx | %.2f%% |
| 3xx | %.2f%% |
| 4xx | %.2f%% |
| 5xx | %.2f%% |
        """ % (
            100 * float(hits[0]) / processed,
            100 * float(hits[1]) / processed,
            100 * float(hits[2]) / processed,
            100 * float(hits[3]) / processed,
            100 * float(hits[4]) / processed,
        )


uri = "/{}/_search".format(index)
uri += "?size=1000&sort={0}:desc&_source_includes={0},{1}".format(
    timestampField, responseField
)
if query not in ["", None]:
    uri += "&q={}".format(query)

request = HttpRequest(server, username, password)
response = request.get(uri, body="", contentType="application/json")

if response.isSuccessful():
    hits = json.loads(response.getResponse())["hits"]["hits"]
    for hit in hits:
        if hit["_id"] not in lastHits:
            if int(hit["_source"]["response"]) < 200:
                hits1xx += 1
            elif int(hit["_source"]["response"]) < 300:
                hits2xx += 1
            elif int(hit["_source"]["response"]) < 400:
                hits3xx += 1
            elif int(hit["_source"]["response"]) < 500:
                hits4xx += 1
            elif int(hit["_source"]["response"]) < 600:
                hits5xx += 1
            processed += 1
    lastHits = [hit["_id"] for hit in hits]
else:
    response.errorDump()
    raise Exception("Unable to get hits")

if processed > 0:
    if acceptable1xx != -1 and float(hits1xx) / processed > float(acceptable1xx) / 100:
        print(hitsTable([hits1xx, hits2xx, hits3xx, hits4xx, hits5xx], processed))
        raise Exception("Exceeded permitted 1xx hits")
    if acceptable2xx != -1 and float(hits2xx) / processed > float(acceptable2xx) / 100:
        print(hitsTable([hits1xx, hits2xx, hits3xx, hits4xx, hits5xx], processed))
        raise Exception("Exceeded permitted 2xx hits")
    if acceptable3xx != -1 and float(hits3xx) / processed > float(acceptable3xx) / 100:
        print(hitsTable([hits1xx, hits2xx, hits3xx, hits4xx, hits5xx], processed))
        raise Exception("Exceeded permitted 3xx hits")
    if acceptable4xx != -1 and float(hits4xx) / processed > float(acceptable4xx) / 100:
        print(hitsTable([hits1xx, hits2xx, hits3xx, hits4xx, hits5xx], processed))
        raise Exception("Exceeded permitted 4xx hits")
    if acceptable5xx != -1 and float(hits5xx) / processed > float(acceptable5xx) / 100:
        print(hitsTable([hits1xx, hits2xx, hits3xx, hits4xx, hits5xx], processed))
        raise Exception("Exceeded permitted 5xx hits")

if time.time() > float(endTime):
    print(hitsTable([hits1xx, hits2xx, hits3xx, hits4xx, hits5xx], processed))
    task.setStatusLine("Checked")
else:
    task.setStatusLine("Inspecting hits...")
    task.schedule("elasticsearch/CheckHitsInspecting.py", 1)
