#coding:utf-8

import random
from  datetime import timedelta
import model
from run import app, db

random.randint(100000, 999999)

print(timedelta(minutes=60))

user1 = model.User()
user1.email = 'xxxxxx'

user2 = model.User()
user2.email = 'yyyyyy'

db.session.add(user1)
db.session.add(user2)

xxx = db.session
print(len(db.session.new))