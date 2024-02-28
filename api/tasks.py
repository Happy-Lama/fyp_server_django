from fyp_server.celery import app

@app.task
def hello_world():
    print("Hello Task is running...")
    return "Success"