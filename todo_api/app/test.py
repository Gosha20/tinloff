from app import db, models

u = models.User.query.all()

p = u[0].tasks[1]
# p1 = models.Task(body='make tea', timestamp=datetime.datetime.utcnow(), user_id=u.id)
# u2 = models.User.query.get(2)
# p = models.Task(body='my first post!', timestamp=datetime.datetime.utcnow(), user_id=u1.id)
# p2 = models.Task(body='my sec post!', timestamp=datetime.datetime.utcnow(), user_id=u2)
# db.session.add(u)

# db.session.add(p)
# db.session.add(p1)
print(p.timestamp.replace(hour=23))
p.timestamp = p.timestamp.replace(hour=23)
print(p)
db.session.commit()
