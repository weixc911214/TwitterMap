__author__ = 'wei'
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
users = Table('TwitterMap')

johndoe = users.get_item(id = 1)

print johndoe