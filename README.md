# Email Providers
## Overview
In order to prevent downtime during an email service provider outage, you’re
tasked with creating a service that provides an abstraction between two
different email service providers. This way, if one of the services goes down,
you can quickly failover to a different provider without affecting your
customers.

## Language, Framework, and Prerequisites
This application is written in Python. It uses Flask as the framework. I chose
Python/Flask because it's fairly light-weight and scalable framework and also
it is easy to implement the required service with JSON data.

The following is Prerequisites for this application.
* Python 2.7 (Tested with 2.7.6, Don't use 3.x.)
* Flask 0.10 (Tested with 0.10.1) (Note: Flask has the prerequisites such
  as Jinja2. You will need them in your environment.)
* requests 2.2 or above (Tested with 2.2.1)

## Installation
To install the application, please follow the below steps.
* Download and install Python 2.7 from https://www.python.org/downloads/.
* Install pip for easy installation for the prerequisites. (Note: you can
  still install the prerequisites without pip.) To install pip, please refer to
  https://pip.pypa.io/en/stable/installing/.
* Install Flask 0.10 by following the instruction at http://flask.pocoo.org.
* Install requests if it's not available after installing Flask and its
  prerequisites.
* Get the application from https://github.com/recto/email_providers.git.

## Getting Started
Once all prerequisites and the application is checked out into your environment,
you can start the application and also run its test cases as below.

### Features
The application supports all basic features given in the instruction. In
addition to that, it supports the following feature mentioned in "Bonus Points".

* Instead of relying on a configuration change for choosing which email provider
to use, dynamically select a provider based on their error responses.
For instance, if Mailgun started to timeout or was returning errors,
automatically switch to Mandrill.

### Content
You will find the following at your workspace where you checked out
the application.
* README.md - this file.
* src/application.py - application main.
* src/providers.py - providers module used by application.py.
* src/resources/providers.json - provider configuration file.
* test/simple_app.py - simple client application to test the service.
* test/test_applicatoin.py - Test case for Flask application.
* test/test_providers.py - Test case for providers module.

### Configuring and Running Application
* This application requires Mailgun and/or Mandrill services. Please create
  your account with them and have the necessary information such as service
  URL and API key.
* From your file manager, go to the workspace where you checked out the
  application. Please find "src/resources/providers.json".
* Open "src/resources/providers.json" with text editor and modify as needed.
  Here is a sample.
```python
{ "default" : "mailgun_email",  <-- Default mail provider.
  "providers": [
    { "name": "mailgun_email", <-- You can name the mail provider as you like.
      "type": "mailgun", <-- "type" should be set to either "mailgun" or "mandrill".
      "url": "https://api.mailgun.net/v3/<your sandbox>.mailgun.org/messages",
      "api_key": "<your API key given by Mailgun>"
    },
    { "name": "mandrill_email",
      "type": "mandrill",
      "url": "https://mandrillapp.com/api/1.0/messages/send.json",
      "api_key": "<your API key given by Mandrill>"
    }
  ]
}
```
* Save your changes.
* Start the terminal or command prompt.
* Go to the workspace where you checked out the application in the terminal.
* Change directory to "src"
* Perform "python application.py"
* Application will be running at http://localhost:8000/email.
* If you have your own client application, stop here and your client
  application. Otherwise, you can use <your workspace>/test/simple_app.py.
* Open <your workspace>/test/simple_app.py and edit payload part with your
  email information.
```python
def test_email():
    payload = {
        "to": "fake@example.com",
        "to_name": "Ms. Fake",
        "from": "noreply@uber.com",
        "from_name": "Uber",
        "subject": "A message from Uber.",
        "body": "<h1>Your billing amount:</h1><p>$10</p>"
    }
    return requests.post(
        "http://localhost:8000/email",
        data=json.dumps(payload),
        headers={"Content-Type" : "application/json"}
    )
```
* Save your changes.
* Start the terminal or command prompt.
* Go to the workspace where you checked out the application in the terminal.
* Change directory to "test".
* Perform "python simple_app.py".
* Check your email inbox.

### Configuring and Running Test Cases
* Test cases require both Mailgun and Mandrill services. Please create
  your account with them and have the necessary information such as service
  URL and API key.
* From your file manager, go to the workspace where you checked out the
  application. Please find "test/resources/providers.json". (Note: This is
  the different JSON file from the one for application.)
* Open "test/resources/providers.json" with text editor and modify only
  placeholders. Here is a sample.
```python
{ "default" : "mailgun",
  "providers": [
    { "name": "mailgun",
      "type": "mailgun",
      "url": "https://api.mailgun.net/v3/<your sandbox>.mailgun.org/messages",
      "api_key": "<your API key given by Mailgun>"
    },
    { "name": "mandrill",
      "type": "mandrill",
      "url": "https://mandrillapp.com/api/1.0/messages/send.json",
      "api_key": "<your API key given by Mandrill>"
    },
    { "name": "mailgun_with_wrong_key",
      "type": "mailgun",
      "url": "https://api.mailgun.net/v3/sandbox.mailgun.org/messages",
      "api_key": "key-wrong"
    },
    { "name": "missing_url",
      "type": "mailgun",
      "api_key": "any-key"
    }
  ]
}
```
* Save your changes.
* Open "test/resources/payloads.json" with your text editor and modify only
  placeholders. Here is a sample.
```python
{ "payloads" : [
    {
      "testcase" : "1",
      "to": "<your target address>",
      "to_name": "Ms. Fake",
      "from": "<your email address>",
      "from_name": "Uber",
      "subject": "Billing Information",
      "body": "<h1>Your billing amount:</h1><p>$10</p>"
    },
    {
      "testcase" : "2",   <-- this test case 2 is missing body on purpose.
      "to": "<your target address>",
      "to_name": "Ms. Fake",
      "from": "<your email address>",
      "from_name": "Uber",
      "subject": "Billing Information",
    }
  ]
}
```
* Save your changes.
* Start the terminal or command prompt.
* Go to the workspace where you checked out the application in the terminal.
* Change directory to "test".
* Perform "python test_providers.py".
* Perform "python test_application.py".

## Trade-offs
If I had more time, I could probably do better in switching between mail
services. It currently checks the response from mail service and switches to
other service at global level. So, the following requests will try to use
the service set by other request first. This might be what's expected but I am
not sure. It should better check more details of response and decides whether
it's caused by the outage of the service or the problem caused by payload.

I was in the middle of implementing the feature to keep a record of emails in
database. But I ran out time and stopped.

## Misc
One of the reasons why I ran out time was Mandrill setup. While Mailgun setup
was easy and straight forward, Mandrill requires domain verification these
days. Refer to the bottom of [About Domain Verification]
(https://mandrill.zendesk.com/hc/en-us/articles/205582247-About-Domain-Verification)
for details. It seems this is only applicable for users, who sign up after
Dec 1, 2015.

Since I have the domain (I actually struggled more with GoDaddy DNS control
panel than Mandrill because their new control panel no longer allow us to modify
SPF setting.), I could do this but it may not be the case for other candidates.
You may want to look for some other mail service for this exercise.
