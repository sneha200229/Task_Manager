from flask import Flask, render_template,request,url_for, flash,redirect


tasks=[
     {
        "id": 1,
        "title": "Learn Flask Routing",
        "description": "Understand static and dynamic routes",
        "status": "Completed",
        "priority": "High"
    },
    {
        "id": 2,
        "title": "Learn Jinja2",
        "description": "Understand Jinja expressions and filters",
        "status": "Pending",
        "priority": "High"
    },
    {
        "id": 3,
        "title": "Build Flask Project",
        "description": "Create a task manager",
        "status": "Pending",
        "priority": "Medium"
    },
    {
        "id": 4,
        "title": "Practice Python",
        "description": "Solve five Python problems",
        "status": "Completed",
        "priority": "Low"
    }  
    
]
app=Flask(__name__)
app.secret_key="my-task-manager-secret"



def show_data(template_name,display_tasks):
    total_tasks=len(tasks)
    completed_tasks=sum(1 for task in tasks if task["status"]=="Completed")
    pending_tasks=sum(1 for task in tasks if task["status"]=="Pending")
    
    return render_template(template_name,tasks=display_tasks,total_tasks=total_tasks,completed_tasks=completed_tasks,pending_tasks=pending_tasks)
    


@app.route("/")
def home():
    return show_data("index.html",tasks)

@app.route("/tasks")
def show_tasks():
    status=request.args.get("status")
    if status:
        filtered_tasks=[]
        for task in tasks:
            if task["status"].lower()==status.lower():
                filtered_tasks.append(task)
        return show_data("tasks.html",filtered_tasks)
    return show_data("tasks.html",tasks)

@app.route("/tasks/<int:id>")
def show_task_byid(id):
    for task in tasks:
        if task["id"]==id:
            return render_template("task_detail.html", task=task)
    return "Task not found", 404


#route to add new task
@app.route("/tasks/add",methods=["GET","POST"])
def taskadd():
    if request.method=="POST":
        title=request.form.get("title")
        desc=request.form.get("description")
        status=request.form.get("status")
        priority=request.form.get("priority")
        new_id=max((task["id"] for task in tasks), default=0)+1
        new_task={
        "id":new_id,
        "title":title,
        "description":desc,
        "status":status,
        "priority":priority
        }
        tasks.append(new_task)
        flash("Task added succesffully!")
        return redirect(url_for("show_tasks"))
    return render_template("add_task.html")

if __name__=="__main__":
    app.run(debug=True,port=5002)