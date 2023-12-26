import http.client

conn = http.client.HTTPSConnection("www.hackerrank.com")

payload = ""

headers = { 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}

conn.request("GET", "/rest/contests/2nd-year-cdc-17-12-2023/leaderboard?offset=0&limit=1", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))