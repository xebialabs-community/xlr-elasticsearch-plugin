# get the configuration properties from the UI
params = {
    "url": configuration.url,
    "authenticationMethod": configuration.authenticationMethod,
    "username": configuration.username,
    "password": configuration.password,
    "domain": configuration.domain,
    "proxyHost": configuration.proxyHost,
    "proxyPort": configuration.proxyPort,
    "proxyUsername": configuration.proxyUsername,
    "proxyPassword": configuration.proxyPassword,
}

request = HttpRequest(params)
response = request.get("/", contentType="application/json")

if not response.isSuccessful():
    raise Exception(response.status, response.headers, response.response)
