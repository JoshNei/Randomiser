import base64
import http.client
import MB
import logging
import secrets
import time

"""
Dynamic text is now available for messages and emails. A message or email can include dynamic information about the trigger event (i.e. the name of the controller where the event took place). The dynamic codes available are as follows (without quotes):
Cardholder Name: "%ch%"
Controller Name:"%controllerName%"
Controller UID:"%controllerUID%"
Input Name: "%input%"
Input UID: "%inputUID%"
Reader Name: "%reader%"
Reader UID: "%readerUID%"
Log Date:"%logDate%"

Dynamic codes that do not have a corresponding value will either not appear or appear in code form. For example, a cardholder name would not appear for an alarm trigger event.


Process:
    GR calls script.
    Script decides to hold CH via RNG:
        Pass CH:
            Trigger door relay via API. 
        Hold CH:
            Log to journal.
            Show popup with CH info and prompt with Allow, Deny:
                Allow:
                    Trigger door relay via API. 
                    Log to journal.
                Deny:
                    Prompt for deny reason.
                    Log to journal.
    Exit script.
                    
"""


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('main')


def call_api(method, path, host="LOCALHOST", port=10695, auth="admin:00000000-0000-0000-0000-000000000000", payload="", timeout=2):
    conn = http.client.HTTPConnection(host, port, timeout=timeout)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Basic " + base64.b64encode(auth.encode('ascii')).decode('ascii')
    }
    log.info(f"Connecting to API on {host}:{port}...")
    log.debug(f"API request header: \"{headers}\"")
    log.debug(f"API request payload: \"{payload}\"")
    start_time = time.time()
    try:
        conn.request(method, path, payload, headers)
        # conn.request("GET", "/odata", "", headers)
    except (TimeoutError, ConnectionRefusedError) as e:
        log.error(f"No response from API - {e}")
        return False
    response = conn.getresponse()
    response_str = response.read().decode("utf-8")
    # log_string = f"API Response: {response.reason} ({response.status})"
    log_string = f"API Response: {response.reason} ({response.status}) in {round((time.time() - start_time)*1000)}ms"
    if 200 <= response.status <= 299:
        log.info(log_string)
        log.debug("API response: " + response_str)
        return response_str
    else:
        log.error(log_string)
        log.debug("API response: " + response_str)
        return None


def select(top):
    rand_n = secrets.randbelow(top)
    rand_b = not bool(rand_n)
    log.debug(f"Random draw out of {top}: {rand_n}, {'Check' if rand_b else 'Allow'} cardholder")
    return bool(rand_b)


def test_select(sample, top):
    true_val = 0
    for i in range(sample):
        if select(top):
            true_val += 1
    log.info(f"{true_val}/{sample} holds, {true_val / sample}% hold rate")


if __name__ == "__main__":
    log.info("Running randomiser check")
    if select(3):
        log.info("Cardholder selected for random check")
        if MB.popup("Cardholder selected for random check.\nAllow access?", style=MB.BTN_YESNO | MB.ICN_WARNING) == MB.YES:
            log.info("Cardholder access allowed")
            log.debug("Activating relay")
            call_api("POST", "/odata/API_Outputs/Activate", payload='{"apiKeys":["RND"],"period":"5"}')
            log.debug("Logging to journal")
            call_api("POST", "/odata/API_Workstations/LogIntoEventsLog", payload='{"workstations":["DESKTOP-T65HV7U_GUI"],"logData":"This is a log From API","logType":"Information"}')
        else:
            log.info("Cardholder access denied")
            log.debug("Logging to journal")
            call_api("POST", "/odata/API_Workstations/LogIntoEventsLog", payload='{"workstations":["DESKTOP-T65HV7U_GUI"],"logData":"This is a log From API","logType":"Information"}')
    else:
        log.info("Cardholder not selected for random check")
        log.debug("Activating relay")
        call_api("POST", "/odata/API_Outputs/Activate", payload='{"apiKeys":["RND"],"period":"5"}')
