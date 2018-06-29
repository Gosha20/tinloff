import json
import datetime
from user import User

"""problem with prety write to file"""
class MyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, User):
			return json.dumps(obj, default=lambda x: x.isoformat() if isinstance(x, datetime.datetime)
			else  x.__dict__)

		return json.JSONEncoder.default(self, obj)
