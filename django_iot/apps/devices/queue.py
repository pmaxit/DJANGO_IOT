import boto3
import time
import json


class Queue:
    def __init__(self):
        self.QueueName = 'command'
        self.sqs = boto3.resource('sqs')
        self.getQueue()

    def create(self):
        self.queue = self.sqs.create_queue(QueueName=self.QueueName)

    def getQueue(self):
        self.queue = self.sqs.get_queue_by_name(QueueName=self.QueueName)

    def pushMessage(self, msg):
        jMsg = json.dumps(msg)
        self.queue.send_message(MessageBody=jMsg)