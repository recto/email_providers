from flask import Flask, request, make_response
import json
from providers import ProviderFactory, Provider

APP_PROVIDERS_JSON = "resources/providers.json"
APP_CONTENT_TYPE = "Content-Type"
APP_CONTENT_TYPE_JSON = "application/json"
app = Flask(__name__)

config = json.loads(open(APP_PROVIDERS_JSON, "r").read())
default_provider = config[Provider.PROVIDER_DEFAULT]
provider_factory = ProviderFactory(config[Provider.PROVIDER_PROVIDERS])
provider = provider_factory.get_provider(default_provider)
APPLICATION_NAME = "Email Providers"

##
# Routing functions
##


@app.route("/email", methods=["POST"])
def email():
    """
    Receive a request to send e-mail with JSON format. This validates the
    incoming JSON payload and send e-mail through the specified mail service
    provider.
    :return: e-mail delivery result.
    """
    global provider
    failed = []
    data = request.get_json()
    if data is None:
        response = make_response(json.dumps({"message": "JSON data is not valid."}),
                    400)
        response.headers[APP_CONTENT_TYPE] = APP_CONTENT_TYPE_JSON
        return response

    try:
        r = provider.send_message(data)
    except RuntimeError as e:
        app.logger.debug(str(e))
        response = make_response(json.dumps({"message": str(e)}), 400)
        response.headers[APP_CONTENT_TYPE] = APP_CONTENT_TYPE_JSON
        return response

    if r.status_code != 200:
        app.logger.debug("%s failed with %d: %s." %
            (provider.provider[Provider.PROVIDER_NAME], r.status_code, r.text))
        failed.append(provider.provider[Provider.PROVIDER_NAME])
        for p in provider_factory.providers:
            if p[Provider.PROVIDER_NAME] in failed:
                continue
            else:
                provider = provider_factory.get_provider(p[Provider.PROVIDER_NAME])
                try:
                    r = provider.send_message(data)
                except RuntimeError as e:
                    app.logger.debug(str(e))
                    response = make_response(json.dumps({"message": str(e)}), 400)
                    response.headers[APP_CONTENT_TYPE] = APP_CONTENT_TYPE_JSON
                    return response
                if r.status_code == 200:
                    break
    app.logger.debug("%s : %s" % (r.status_code, r.text))
    response = make_response(json.dumps({"message": r.text}), r.status_code)
    response.headers[APP_CONTENT_TYPE] = APP_CONTENT_TYPE_JSON
    return response

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
