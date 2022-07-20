import binascii
import http.client

host = "localhost"
port = 10695
timeout = 5000
method = "GET"
path = "/"
payload = None
headers = {}

conn = http.client.HTTPConnection(host, port, timeout=timeout)

try:
    conn.request(method, path, payload, headers)
    # conn.request("GET", "/odata", "", headers)
except (TimeoutError, ConnectionRefusedError) as e:
    print(f"No response from API - {e}")
except Exception as e:
    print(f"Unkown classified Error - {e}")

print(f"Finished")
r = conn.getresponse().read()
s = binascii.b2a_hex(r)
print(s)

print(r)