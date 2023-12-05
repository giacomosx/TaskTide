from app import db
from models import Project
import datetime

new_item = Project(creation_date=datetime.date.today(), description='First Project')
db.session.add(new_item)
db.session.commit()