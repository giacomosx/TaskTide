from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app import app, db
from flask import render_template, request, url_for, redirect, flash
from models import Task, Project
import datetime


all_projects_global = Project.query.all()
all_projects_global_list = [item.id for item in all_projects_global]

class TaskForm(FlaskForm):
    task_description = StringField(validators=[DataRequired()])
    task_responsible = StringField(validators=[DataRequired()])
    prj_rel = SelectField(choices=all_projects_global_list)
    task_priority = SelectField('Priority: ', choices=[1, 2, 3, 4], default=4)
    task_due = DateField(format='%Y-%m-%d')
    task_submit = SubmitField("Add Task")


class PrjForm(FlaskForm):
    prj_description = StringField(validators=[DataRequired()])
    prj_submit = SubmitField("Add Project")

@app.route('/remove_task/<int:task_id>')
def remove_task(task_id):
    task_to_remove = Task.query.get(task_id)
    db.session.delete(task_to_remove)
    db.session.commit()

    return redirect('/')

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    task_to_complete = Task.query.get(task_id)
    task_to_complete.status = 1
    task_to_complete.completed_date = datetime.date.today()
    db.session.commit()

    return redirect('/')
#inizio
@app.route('/remove_project/<int:proj_id>')
def remove_project(proj_id):
    project_to_remove = Project.query.get(proj_id)
    db.session.delete(project_to_remove)
    db.session.commit()

    return redirect('/')

@app.route('/complete_project/<int:proj_id>')
def complete_project(proj_id):
    project_to_complete = Project.query.get(proj_id)
    project_to_complete.status = 1
    project_to_complete.completed_date = datetime.date.today()
    db.session.commit()

    return redirect('/')
#fine

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    task_form = TaskForm()
    prj_form = PrjForm()
    if task_form.task_submit.data:
        new_task = Task(date_added=datetime.date.today(),
                        description=task_form.task_description.data,
                        project_id=task_form.prj_rel.data,
                        responsible=task_form.task_responsible.data,
                        priority=task_form.task_priority.data,
                        due_date=task_form.task_due.data)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('dashboard'))

    else:
        flash(task_form.errors)

    if prj_form.prj_submit.data:
        new_prj = Project(creation_date=datetime.date.today(), description=prj_form.prj_description.data)
        db.session.add(new_prj)
        db.session.commit()

        return redirect(url_for('dashboard'))

    else:
        flash(task_form.errors)

    all_tasks = Task.query.filter(Task.status == 0)
    done_tasks = Task.query.filter(Task.status == 1)

    all_projects = Project.query.filter(Project.status == 0)
    done_projects = Project.query.filter(Project.status == 1)
    
    task_form.prj_rel.choices = [project.id for project in all_projects]


    print(task_form.errors)

    return render_template('dashboard.html', all_projects=all_projects, all_tasks=all_tasks, task_form=task_form, done_tasks=done_tasks, prj_form=prj_form, done_projects=done_projects)