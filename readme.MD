
# Python SDK for interacting with TelQ API

### Python version required
- Python 3.7+

## Interacting with the TelQ Python SDK

### Instantiate the TelQTelecomAPI

---
```go
from telq import TelQTelecomAPI


test_client = TelQTelecomAPI()
```
---

### Authentication:

---
```go
test_client.authenticate(api_id="<yourAppKey>", api_key="<yourAppId>")

/* 
Make sure to pass your app key and app id in the authenticate call.
Furthermore, keep in mind that your token will be automatically requested, but if for any reason
you destruct the test client, you will have to initialize it again with your app key and id.
*/
```
---

### Get the list of available networks

---
```go
available_networks = test_client.get_networks()

/*
Keep in mind that to use TelQTelecomAPI,
first you need to initialise it with your app key and app id (step above).
*/
  

/*
This will return the list of all available networks at the current moment.
Keep in mind, that this list is updated frequently and it's not recommended to use this list to initiate tests after
a long time has passed.
*/
```
---
### Request new tests

---
```go
/*
A request with all the optional parameters set up within the test client object will 
have the following structure:
*/

destinationNetworks = [
        {
            "mcc": "206",
            "mnc": "10",
            "portedFromMnc": "20"
        },
        {
            "mcc": "716",
            "mnc": "06"
        }
    ]

requested_tests = test_client.initiate_new_tests(
    destinationNetworks=destinationNetworks,
    resultsCallbackUrl="https://my-callback-url.com/telq_result",
    maxCallbackRetries=3,
    testIdTextType="ALPHA_NUMERIC",
    testIdTextCase="MIXED",
    testIdTextLength=7,
    testTimeToLiveInSeconds=3000
)


/*
A request with only the mandatory (networks) parameter set up within the test client 
object will have this structure:
*/

requested_tests = test_client.initiate_new_tests(destinationNetworks=destinationNetworks)
```
---
### Test Results

---
```go
/*
Each test initiation returns a JSON response, containing the test details.
Most importantly, it contains the phoneNumber, testIdText, and id. 
You will need the (test) id to request the test results.
*/

/*
You can get the test id (of the first test) this way:
*/

test_id = requested_tests[0].get('id')

/*
Getting your test result would look like this:
*/

test_result = test_client.get_test_results(test_id)
```
---