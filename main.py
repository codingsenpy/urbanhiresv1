from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
db = mongo.db
app.secret_key = os.urandom(24)
@app.route('/')
def home():
    return render_template("index.html")

@app.route("/hire", methods=["GET", "POST"])
def hire():
    if request.method == "POST":
        # Generate or retrieve a session ID for the user
        if 'user_id' not in session:
            session['user_id'] = str(ObjectId())

        new_job = {
            "jobtype": request.form["jobtype"],
            "pay": request.form["pay"],
            "location": request.form["location"],
            "time": request.form["time"],
            "user_id": session['user_id']
        }
        db.jobs.insert_one(new_job)
        return redirect(url_for('my_jobs'))  # Redirect to a new page to show posted jobs

    return render_template("hire.html")             # Render hire.html for GET request

@app.route("/my_jobs", methods=["GET"])
def my_jobs():
    if 'user_id' in session:
        user_jobs = list(db.jobs.find({"user_id": session['user_id']}))
        return render_template("my_jobs.html", jobs=user_jobs)
    return "No jobs found for this user."


@app.route("/work", methods=['POST', 'GET'])
def work():
    jobs = list(db.jobs.find())
    print(jobs)
    return render_template("work.html", jobs=jobs)

@app.route("/accept_job", methods=['POST'])
def accept_job():
    job_data = request.get_json()
    job_id = job_data["job_id"]
    job = db.jobs.find_one({"_id": ObjectId(job_id)})

    if job:
        db.accepted_jobs.insert_one(job)
        db.jobs.delete_one({"_id": ObjectId(job_id)})
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Job not found'}), 404

@app.route("/accepted_jobs", methods=['GET'])
def show_accepted_jobs():
    accepted_jobs = list(db.accepted_jobs.find())
    print(accepted_jobs) 
    return render_template("accepted_jobs.html", accepted_jobs=accepted_jobs)

@app.route("/delete_job/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    result = db.jobs.delete_one({"_id": ObjectId(job_id)})
    if result.deleted_count > 0:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Job not found'}), 404

@app.route("/edit_job/<job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    if request.method == "POST":
        updated_job = {
            "jobtype": request.form["jobtype"],
            "pay": request.form["pay"],
            "location": request.form["location"],
            "time": request.form["time"]
        }
        db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": updated_job})
        return redirect(url_for('my_jobs'))

    job = db.jobs.find_one({"_id": ObjectId(job_id)})
    return render_template("edit_job.html", job=job)

if __name__ == "__main__":
    app.run(debug=True)
