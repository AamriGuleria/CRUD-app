from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///emp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class Employee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    job=db.Column(db.String(100),nullable=False)
    salary=db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return f"{self.id}--{self.name}--{self.job}--{self.salary}"

@app.route('/add',methods=['GET','POST'])
def form():
    if request.method=='POST':
        name=request.form.get('name')
        job=request.form.get('job')
        salary=request.form.get('salary')
        entry=Employee(name=name,job=job,salary=salary)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    u=db.session.get(Employee,id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    employee = Employee.query.filter_by(id=id).first()
    if request.method=='POST':
        name=request.form['name']
        job=request.form['job']
        salary=request.form['salary']
        employee=Employee(id=id,name=name,job=job,salary=salary)
        db.session.merge(employee)
        db.session.commit()
        return redirect('/')
    
    return render_template('update.html',employee=employee)

@app.route('/')
def display():
    alldata=Employee.query.all()
    return render_template('index.html',alldata=alldata)

@app.route('/form')
def temp():
    return render_template('form.html')

if __name__=="__main__":
    from app import db
    db.create_all()
    app.run(debug=True)

