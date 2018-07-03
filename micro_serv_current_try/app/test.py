from app import db, models
import datetime

u1 = models.User.query.get(1)
# u2 = models.User.query.get(2)
# p = models.Task(body='my first post!', timestamp=datetime.datetime.utcnow(), user_id=u1.id)
# p2 = models.Task(body='my sec post!', timestamp=datetime.datetime.utcnow(), user_id=u2)
# db.session.add(p)
# db.session.commit()
# print(list(filter(lambda x: x.id == 1, u1.tasks.all())))
for task in u1.tasks.all():
	print(task.__dict__)
print(u1.tasks.all())
