from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500),  nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow )

    def __repr__(self) -> str:
        return f"{self.sno}- {self.title}"
@app.route("/" , methods=['GET', 'POST'])
def todo_func():
    if request.method=='POST':
        desc=request.form['desc']
        title=request.form['title']
        
        todo= Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo= Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route("/update")
def update():
    alltodo= Todo.query.all()
    print(alltodo)
    return "<p>This is my products page</p>"

@app.route("/delete/<int:sno>")
def delete(sno):
    alltodo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")
if __name__=='__main__':
	app.run(debug=True,port=5500)


	