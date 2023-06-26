import os
from flask import Flask, request, flash, url_for, redirect, render_template, app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql   import func




# from sqlalchemy.sql import text
# from sqlalchemy.exc import DatabaseError
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy		import create_engine, select, and_, MetaData, Table


# ------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# ------------------------------------------------------------
class Student(db.Model):
    id   = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    maths = db.Column(db.Integer)
    sci = db.Column(db.Integer)
    position = db.Column(db.Integer)
    remarks = db.Column(db.String(100))
       

    def __init__(self, name, maths, sci, position, remarks):
        self.name = name
        self.maths = maths
        self.sci = sci
        self.position = position
        self.remarks = remarks

        #self.total = self.maths + self.eng + self.sci
        #self.mean = (self.maths + self.eng + self.sci)/3


    def total(self):
        return self.maths + self.sci
            
    def mean(self):
        return (self.maths + self.sci)/2

class School(db.Model):
    id   = db.Column('school_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
        
    def __init__(self, name):
        self.name = name
        
# ------------------------------------------------------------
@app.route('/')
def show_all():
    students = Student.query.all()
    return render_template('show_all.html', students=students)

@app.route('/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['maths'] or not request.form['sci']:
            flash('Please enter all the fields', 'error')
        else: 
            student = Student(request.form['name'], request.form['maths'], request.form['sci'], request.form['position'], request.form['remarks'])
            db.session.add(student)
            db.session.commit()

        return redirect(url_for('show_all'))
    return render_template('new.html', student={"maths":20})

@app.route("/edit/<id>", methods = ['GET', 'POST'])
def edit(id):
    # if request.method == 'GET':
    # student = db.session.query.get(id)
    student = Student.query.get(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.maths = request.form['maths']
        student.sci = request.form['sci']
        student.position = request.form['position']
        student.remarks = request.form['remarks']
        
        db.session.commit()
       
        return redirect(url_for('show_all'))
    return render_template('new.html', student=student)

@app.route('/schools')
def schools():
    schools = School.query.all()
    return render_template('schools.html', schools=schools)


@app.route('/schools/new_school', methods = ['GET', 'POST'])
def new_school():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter details', 'error')
        else: 
            school = School(request.form['name'])
            db.session.add(school)
            db.session.commit()

        return redirect(url_for('schools'))
    return render_template('new_school.html')

@app.route("/schools/edit/<id>", methods = ['GET', 'POST'])
def schools_edit(id):
    school = School.query.get(id)

    if request.method == 'POST':
        school.name = request.form['name']
                
        db.session.commit()
       
        return redirect(url_for('schools'))
    return render_template('new_school.html', school=school)



# ------------------------------------------------------------
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all() #test

#   app.run(debug=True)
    app.run(debug=True, use_reloader=False, threaded=True)


# alter table Student add position int; .., for adding a new field/column
# delete from Student where student_id = 6 .., for removing a row in a table