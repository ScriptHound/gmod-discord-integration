import urllib3
http = urllib3.PoolManager()

data = {
	"name" : "testname",
	"group" : "testmsg",
	"msg" : "sometextmessage",
}
data["name"] = "a_user_name"
data["msg"] = "testmsg"

r = http.request('POST', '127.0.0.1:8881/send_message', fields=data)
print(r.status)

r = http.request('GET', '127.0.0.1:8881/get_messages')
print(r.status)
print(r.data)


