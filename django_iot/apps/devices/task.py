from celery import Celery

app = Celery("tasks", backend ='amqp', broker='amqp://puneet:password@52.36.59.156/myhost')

@app.task
def reverse(arg):
    return arg[::-1]
