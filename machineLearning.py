import boto3
import pusher
import time
import json

pusher_client = pusher.Pusher(
        app_id='330825',
        key='a9603eebc0a6a7c05d7e',
        secret='56b571ab2b832dbabee1',
        ssl=True
        )

class Queue:
    def __init__(self):
        self.QueueName = 'test'
        self.sqs = boto3.resource('sqs')
        self.getQueue()

    def create(self):
        self.queue = self.sqs.create_queue(QueueName=self.QueueName)

    def getQueue(self):
        self.queue = self.sqs.get_queue_by_name(QueueName=self.QueueName)

    def poll(self, delta=1):
        while(True):
            time.sleep(delta)
            for message in self.queue.receive_messages(
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=['All'],
                    WaitTimeSeconds=4
                    ):
                jObj = json.loads(message.body)
                # remove the message

                #message.delete()
                print 'received ' ,jObj
                #pusher_client.trigger('messages', 'update', jObj)

if __name__ == '__main__':
    q = Queue()
    q.poll()
    #q.create()

