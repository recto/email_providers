import requests
import json
import xml.etree.ElementTree


class ProviderFactory(object):
    """
    ProviderFactory provides factory method to produce the instance of
    Provider according the given provider name.
    """
    def __init__(self, providers):
        self.providers = providers
        self.validate_providers()

    def validate_providers(self):
        """
        Validate the given providers and remove the invalid providers.
        :return: No return value.
        """
        required = [Provider.PROVIDER_NAME, Provider.PROVIDER_TYPE,
                    Provider.PROVIDER_URL, Provider.PROVIDER_API_KEY]
        failed = []
        for p in self.providers:
            for param in required:
                if param in p:
                    continue
                else:
                    failed.append(p)
                    self.providers.remove(p)
                    break

    def get_provider(self, provider_name):
        """
        Factory method to produce Provider instance with the given
        provider name.
        :param provider_name: the name of provider in configuration.
        :return: Provider instance.
        """
        provider = None
        for p in self.providers:
            if provider_name == p[Provider.PROVIDER_NAME]:
                if p[Provider.PROVIDER_TYPE] == Provider.PROVIDER_TYPE_MAILGUN:
                    provider = Mailgun(p)
                elif p[Provider.PROVIDER_TYPE] == Provider.PROVIDER_TYPE_MANDRILL:
                    return Mandrill(p)

        if provider is None:
            message = "Could not instanciate %s." % (provider_name)
            raise RuntimeError(message)

        return provider


class Provider(object):
    """
    Base class for providers. This class provides a few methods, which can be
    used by subclasses.
    """
    PROVIDER_TYPE_MAILGUN = "mailgun"
    PROVIDER_TYPE_MANDRILL = "mandrill"
    PROVIDER_DEFAULT = "default"
    PROVIDER_PROVIDERS = "providers"
    PROVIDER_NAME = "name"
    PROVIDER_TYPE = "type"
    PROVIDER_URL = "url"
    PROVIDER_API_KEY = "api_key"
    PAYLOAD_TO = "to"
    PAYLOAD_TO_NAME = "to_name"
    PAYLOAD_FROM = "from"
    PAYLOAD_FROM_NAME = "from_name"
    PAYLOAD_SUBJECT = "subject"
    PAYLOAD_BODY = "body"
    PAYLOAD_TEXT = "text"

    required = [PAYLOAD_TO, PAYLOAD_TO_NAME, PAYLOAD_FROM, PAYLOAD_FROM_NAME,
                PAYLOAD_SUBJECT, PAYLOAD_BODY]

    def __init__(self, provider):
        """
        Constructor of Provider class.
        :param provider: provider information such as url, api_key.
        :return: No return value
        """
        self.provider = provider

    def validate_payload(self, payload):
        """
        Validate payload and check if it has the required attributes.
        :param payload: payload data.
        :return: True if it's valid. Otherwise, raise RuntimeError.
        """
        for p in self.required:
            if p not in payload:
                message = "Incoming payload is missing the required field, %s." % (
                    p)
                raise RuntimeError(message)
        return True

    def get_plain_text(self, payload):
        """
        Utility method to remove HTML tags from payload's body.
        :param payload: payload data
        :return: payload data with "text" attribute.
        """
        body = payload[self.PAYLOAD_BODY]
        # adding <body> tag so ElementTree can parse the incoming body text.
        text = "".join(xml.etree.ElementTree.fromstring(
            "<body>" + body + "</body>").itertext())
        payload[self.PAYLOAD_TEXT] = text
        return payload

    def send_message(self, payload):
        """
        Placeholder for send_message. Provider.send_message is not supposed to
        be called. Thus, this raises RuntimeError when it's called.
        :param payload: payload data.
        :return: No return value.
        """
        message = "You are calling Provider class directly. You should use get_provider method to get the instance."
        raise RuntimeError(message)


class Mailgun(Provider):
    """
    Provider implementation for Mailgun.
    """
    REQ_API = "api"
    REQ_KEY = "key"
    REQ_FROM = "from"
    REQ_TO = "to"
    REQ_SUBJECT = "subject"
    REQ_TEXT = "text"

    def send_message(self, payload):
        """
        send message with payload to mailgun.
        :param payload: payload data.
        :return: Response returned by Mailgun.
        """
        self.validate_payload(payload)
        payload = self.get_plain_text(payload)
        data = {
            Mailgun.REQ_FROM: payload[Provider.PAYLOAD_FROM_NAME] + "<" +
                              payload[Provider.PAYLOAD_FROM] + ">",
            Mailgun.REQ_TO: payload[Provider.PAYLOAD_TO_NAME] + "<" + payload[
                Provider.PAYLOAD_TO] + ">",
            Mailgun.REQ_SUBJECT: payload[Provider.PAYLOAD_SUBJECT],
            Mailgun.REQ_TEXT: payload[Provider.PAYLOAD_TEXT],
        }
        return requests.post(
            self.provider[Provider.PROVIDER_URL],
            auth=(Mailgun.REQ_API, self.provider[Provider.PROVIDER_API_KEY]),
            data=data)


class Mandrill(Provider):
    """
    Provider implementation for Mandrill.
    """
    REQ_KEY = "key"
    REQ_MESS = "message"
    REQ_SUBJECT = "subject"
    REQ_TEXT = "text"
    REQ_FROM = "from_email"
    REQ_FROM_NAME = "from_name"
    REQ_TO = "to"
    REQ_TO_EMAIL = "email"
    REQ_TO_NAME = "name"
    REQ_TYPE = "type"
    REQ_TYPE_TO = "to"

    def send_message(self, payload):
        """
        send message with payload to mandrill.
        :param payload: payload data.
        :return: Response returned by Mandrill.
        """
        self.validate_payload(payload)
        payload = self.get_plain_text(payload)
        data = {
            Mandrill.REQ_KEY: self.provider[Provider.PROVIDER_API_KEY],
            Mandrill.REQ_MESS: {
                Mandrill.REQ_TEXT: payload[Provider.PAYLOAD_TEXT],
                Mandrill.REQ_SUBJECT: payload[Provider.PAYLOAD_SUBJECT],
                Mandrill.REQ_FROM: payload[Provider.PAYLOAD_FROM],
                Mandrill.REQ_FROM_NAME: payload[Provider.PAYLOAD_FROM_NAME],
                Mandrill.REQ_TO: [
                    {
                        Mandrill.REQ_TO_EMAIL: payload[Provider.PAYLOAD_TO],
                        Mandrill.REQ_TO_NAME: payload[Provider.PAYLOAD_TO_NAME],
                        Mandrill.REQ_TYPE: Mandrill.REQ_TYPE_TO
                    }
                ]
            }
        }
        return requests.post(
            self.provider[Provider.PROVIDER_URL],
            data=json.dumps(data))
