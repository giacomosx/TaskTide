from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date(), index=True, unique=False)
    description = db.Column(db.String(100), index=True, unique=False)
    project_id = db.Column(db.String(50), db.ForeignKey('project.id'))
    responsible = db.Column(db.Integer, index=True, unique=False)
    status = db.Column(db.Integer(), index=True, unique=False, default=0)
    due_date = db.Column(db.Date(), index=True, unique=False)
    priority = db.Column(db.Integer(), index=True, unique=False, default=4)
    completed_date = db.Column(db.Date(), index=True, unique=False)

    # representation method
    def __repr__(self):
        return "{} - Resp. {} - Due date: {}".format(self.description, self.project_id, self.responsible, self.due_date)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date(), index=True, unique=False)
    description = db.Column(db.String(50), index=True, unique=False)
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    status = db.Column(db.Integer(), index=True, unique=False, default=0)

    # representation method
    def __repr__(self):
        return "Project: {} -  {} - date: {}".format(self.id, self.description, self.creation_date, self.status)

