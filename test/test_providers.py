import sys

sys.path.append("../src")
import unittest
from providers import ProviderFactory, Provider, Mailgun, Mandrill
import json, requests

TEST_PROVIDERS_JSON_PROVIDERS = "resources/providers.json"
TEST_PROVIDERS_JSON_PAYLOADS = "resources/payloads.json"
TEST_PROVIDERS_PROVIDERS = "providers"
TEST_PROVIDERS_PAYLOADS = "payloads"
TEST_PROVIDERS_MAILGUN = "mailgun"
TEST_PROVIDERS_MANDRILL = "mandrill"
TEST_PROVIDERS_TESTCASE = "testcase"


class ProviderFactoryTestCase(unittest.TestCase):
    """
    Test case for ProviderFactory.
    """
    def setUp(self):
        self.config = json.loads(
            open(TEST_PROVIDERS_JSON_PROVIDERS, "r").read())
        self.default = self.config[Provider.PROVIDER_DEFAULT]
        self.providers = self.config[Provider.PROVIDER_PROVIDERS]
        self.factory = ProviderFactory(self.providers)

    def tearDown(self):
        pass

    def test_validate_providers(self):
        """
        validate_providers is called by constructor. "missing_url" should be
        removed when ProviderFactory is instantiated.
        """
        test_name = "missing_url"
        result = True
        for provider in self.factory.providers:
            if provider[Provider.PROVIDER_NAME] == test_name:
                result = False
        self.assertTrue(result)

    def test_get_provider(self):
        """
        Test case for ProviderFactory.get_provider.
        """
        provider = self.factory.get_provider(self.default)
        self.assertIsInstance(provider, Mailgun)
        provider = self.factory.get_provider(TEST_PROVIDERS_MANDRILL)
        self.assertIsInstance(provider, Mandrill)
        try:
            provider = self.factory.get_provider("fake")
        except RuntimeError:
            self.assertEqual(0, 0)


class ProviderTestCase(unittest.TestCase):
    """
    Test case for Provider. This tests methods implemented in Provider.
    Since send_message is implemented in subclass, it's not tested.
    """
    def setUp(self):
        self.config = json.loads(
            open(TEST_PROVIDERS_JSON_PROVIDERS, "r").read())
        self.default = self.config[Provider.PROVIDER_DEFAULT]
        self.providers = self.config[Provider.PROVIDER_PROVIDERS]
        self.factory = ProviderFactory(self.providers)
        self.provider = self.factory.get_provider(TEST_PROVIDERS_MAILGUN)
        self.payloads = \
        json.loads(open(TEST_PROVIDERS_JSON_PAYLOADS, "r").read())[
            TEST_PROVIDERS_PAYLOADS]

    def tearDown(self):
        pass

    def test_validate_payload(self):
        """
        Test case for Provider.validate_payload. It should raise RuntimeError
        when the given payload has some error.
        """
        for payload in self.payloads:
            if payload[TEST_PROVIDERS_TESTCASE] == "1":
                self.assertTrue(self.provider.validate_payload(payload))
            elif payload[TEST_PROVIDERS_TESTCASE] == "2":
                try:
                    self.provider.validate_payload(payload)
                except RuntimeError:
                    self.assertEqual(0, 0)

    def test_get_plain_text(self):
        """
        Test case for Provider.get_plain_text. This API should remove HTML tags
        in payload body and add "text" attribute to the given payload.
        :return:
        """
        for payload in self.payloads:
            if payload[TEST_PROVIDERS_TESTCASE] == "1":
                self.assertTrue(Provider.PAYLOAD_TEXT not in payload)
                payload[Provider.PAYLOAD_BODY] = "<h1>Some Text</h1><p>Test</p>"
                self.provider.get_plain_text(payload)
                self.assertTrue(Provider.PAYLOAD_TEXT in payload)
                self.assertEqual(payload[Provider.PAYLOAD_TEXT],
                                 "Some TextTest")


class MailgunTestCase(unittest.TestCase):
    """
    Test case for Mailgun. send_message is tested with both valid payload
    and invalid payload.
    """
    def setUp(self):
        self.config = json.loads(
            open(TEST_PROVIDERS_JSON_PROVIDERS, "r").read())
        self.default = self.config[Provider.PROVIDER_DEFAULT]
        self.providers = self.config[Provider.PROVIDER_PROVIDERS]
        self.factory = ProviderFactory(self.providers)
        self.provider = self.factory.get_provider(TEST_PROVIDERS_MAILGUN)
        self.payloads = \
        json.loads(open(TEST_PROVIDERS_JSON_PAYLOADS, "r").read())[
            TEST_PROVIDERS_PAYLOADS]

    def tearDown(self):
        pass

    def test_send_message(self):
        for payload in self.payloads:
            if payload[TEST_PROVIDERS_TESTCASE] == "1":
                r = self.provider.send_message(payload)
                self.assertEqual(200, r.status_code)
            elif payload[TEST_PROVIDERS_TESTCASE] == "2":
                try:
                    r = self.provider.send_message(payload)
                except RuntimeError:
                    self.assertEqual(0, 0)


class MailgunWithWrongKeyTestCase(unittest.TestCase):
    """
    Test case for Mailgun. But this is tested with wrong api_key. This
    test is to ensure Maingun class can handle the erroneous configuration
    properly.
    """
    def setUp(self):
        self.config = json.loads(
            open(TEST_PROVIDERS_JSON_PROVIDERS, "r").read())
        self.default = self.config[Provider.PROVIDER_DEFAULT]
        self.providers = self.config[Provider.PROVIDER_PROVIDERS]
        self.factory = ProviderFactory(self.providers)
        self.provider = self.factory.get_provider("mailgun_with_wrong_key")
        self.payloads = \
        json.loads(open(TEST_PROVIDERS_JSON_PAYLOADS, "r").read())[
            TEST_PROVIDERS_PAYLOADS]

    def tearDown(self):
        pass

    def test_send_message(self):
        for payload in self.payloads:
            if payload[TEST_PROVIDERS_TESTCASE] == "1":
                r = self.provider.send_message(payload)
                self.assertEqual(401, r.status_code)
                break


class MandrillTestCase(unittest.TestCase):
    """
    Test case for Mandrill. send_message is tested with both valid and
    invalid payload.
    """
    def setUp(self):
        self.config = json.loads(
            open(TEST_PROVIDERS_JSON_PROVIDERS, "r").read())
        self.default = self.config[Provider.PROVIDER_DEFAULT]
        self.providers = self.config[Provider.PROVIDER_PROVIDERS]
        self.factory = ProviderFactory(self.providers)
        self.provider = self.factory.get_provider(TEST_PROVIDERS_MANDRILL)
        self.payloads = \
        json.loads(open(TEST_PROVIDERS_JSON_PAYLOADS, "r").read())[
            TEST_PROVIDERS_PAYLOADS]

    def tearDown(self):
        pass

    def test_send_message(self):
        for payload in self.payloads:
            if payload[TEST_PROVIDERS_TESTCASE] == "1":
                r = self.provider.send_message(payload)
                self.assertEqual(200, r.status_code)
            elif payload[TEST_PROVIDERS_TESTCASE] == "2":
                try:
                    r = self.provider.send_message(payload)
                except RuntimeError:
                    self.assertEqual(0, 0)


if __name__ == "__main__":
    unittest.main()
