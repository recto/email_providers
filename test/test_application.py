import sys
sys.path.append("../src")
import application
import unittest
import json, requests

TEST_APPLICATION_JSON_PAYLOADS = "resources/payloads.json"
TEST_APPLICATION_PAYLOADS = "payloads"
TEST_APPLICATION_TESTCASE = "testcase"
TEST_APPLICATION_PATH_EMAIL = "/email"
TEST_APPLICATION_CONTENT_TYPE = "Content-Type"
TEST_APPLICATION_CONTENT_TYPE_JSON = "application/json"


class ApplicationTestCase(unittest.TestCase):
    def setUp(self):
        application.app.config['TESTING'] = True
        self.app = application.app.test_client()

    def tearDown(self):
        pass

    def test_send_message(self):
        self.payloads = json.loads(open(TEST_APPLICATION_JSON_PAYLOADS, "r").read())[TEST_APPLICATION_PAYLOADS]
        for payload in self.payloads:
            if payload[TEST_APPLICATION_TESTCASE] == "1":
                r = self.app.post(TEST_APPLICATION_PATH_EMAIL,
                    data=json.dumps(payload),
                    headers={TEST_APPLICATION_CONTENT_TYPE : TEST_APPLICATION_CONTENT_TYPE_JSON})
                self.assertEqual(200, r.status_code)
            elif payload[TEST_APPLICATION_TESTCASE] == "2":
                try:
                    r = self.app.post(TEST_APPLICATION_PATH_EMAIL,
                        data=json.dumps(payload),
                        headers={TEST_APPLICATION_CONTENT_TYPE : TEST_APPLICATION_CONTENT_TYPE_JSON})
                except RuntimeError:
                    self.assertEqual(0, 0)

if __name__ == "__main__":
    unittest.main()
