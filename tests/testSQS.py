__author__ = 'wei'
import boto.sqs
from boto.sqs.message import Message
'''
url: http://boto.readthedocs.org/en/latest/sqs_tut.html

'''
conn = boto.sqs.connect_to_region("us-west-2")
print conn.get_all_queues()

m = Message()


m.message_attributes = {
    "name1": {
        "data_type": "String",
        "string_value": "I am a string"
    },
    "name2": {
        "data_type": "Number",
        "string_value": "12"
    }
}
m.set_body("This is a test message")
q = conn.get_queue("test_queue")

q.write(m)
print q.count()

rs = q.read(60)

m = rs


q.delete_message(m)

print q.count()

# print m.message_attributes["name1"]["string_value"]
print m.get_body()