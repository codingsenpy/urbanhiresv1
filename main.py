from flask import Flask, render_template, request, redirect, url_for,jsonify

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

joblist=[{
    "jobtype":"defualt",
"pay":"nomoney",
    "location":"earth",
    "time":"anytime"
}]
accepted_jobs_data = []

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/hire",methods=["GET","POST"])
def hire():
    if(request.method=="POST"):
        newjob={
            "jobtype": request.form["jobtype"],
            "pay":request.form["pay"],
            "location":request.form["location"],
            "time":request.form["time"]
        }
        joblist.append(newjob)
        return 'success'

    return render_template("hire.html")
@app.route("/work",methods=['POST' , 'GET'])
def work():
    return render_template("work.html",jobs=joblist)

@app.route("/accept_job", methods=['POST'])
def accept_job():
    job_data = request.get_json()
    job_index = job_data['job_index']
    accepted_job = joblist[job_index]
    accepted_jobs_data.append(accepted_job)
    return jsonify({'status': 'success'})
@app.route("/accepted_jobs", methods=['GET'])
def show_accepted_jobs():
    return render_template("accepted_jobs.html", accepted_jobs=accepted_jobs_data)
if __name__ == "__main__":
    app.run(debug=True)
# 	<ul>
#         {{ jobs }}
# <!--        {% for job in jobs %}-->
# <!--        <li>{{ job['jobtype'] }} - {{job.pay}} - {{job.location}} - {{job.time}}</li>-->
# <!--        {% endfor %}-->
#     </ul>