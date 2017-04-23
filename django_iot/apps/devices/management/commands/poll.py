from django.core.management.base import BaseCommand, CommandError
from django_iot.apps.interactions.tasks import *
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
        self.start_time = int(time.time())
        self.past_queue = []
        self.window_size= 60
        self.num_windows = 5

    def prediction(self):
        h = {}
        for d in self.past_queue:
            k = d.keys()[0]
            if d.values()[0]  == 'OFF':
                if k not in h:
                    h[k] = 1
                else:
                    h[k]+=1
        # get average for h
        cnt = len(h)
        s   = 0
        print 'h value',h.values()

        for l in h.values():
            s+= l
        pred = s*1.0/cnt
        print 'prediction ' , pred
        status = self.past_queue[0].values()[0]

        w = 30*24*60*60 / self.window_size
        total = self.window_size*w/2
        off = pred*w

        on = total - off

        bill = (on/(60*60))* 5.0/1000*4.8

        data = {"Device Internet Connection": status,
                "Average Power Usage"       : str(on/(60*60)) + "KW/hour",
                "Average Daily Usage"       : str(24*((self.window_size/2-pred)/(self.window_size/2))) + "hours/day",
                "Estimated Bill"            : "$" +str(bill)
                }

        print "Prediction for next window", data

        pusher_client.trigger('messages', 'update', data)

    def create(self):
        self.queue = self.sqs.create_queue(QueueName=self.QueueName)

    def getQueue(self):
        self.queue = self.sqs.get_queue_by_name(QueueName=self.QueueName)

    def checkMessage(self,msg):
        print 'Checking message', msg
        device = msg['device']

        if msg['rpm'] % 2:
            print 'turning on the device'
            set_attributes.delay(devices=[device,], command = "ON")
        else:
            print 'turning off the device'
            set_attributes.delay(devices=[device,], command = "OFF")

    def poll(self, delta=1):
        oldk = -1

        while(True):
            time.sleep(delta)
            for message in self.queue.receive_messages(
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=['All'],
                    WaitTimeSeconds=4
                    ):
                jObj = json.loads(message.body)
                self.checkMessage(jObj)
                
                mTime = int(jObj['time'])
                status = jObj['status']
                # remove the message
                message.delete()
                print 'received ' ,jObj, (mTime - self.start_time) /(self.window_size)
                k = (mTime - self.start_time) / self.window_size
                # running average

                if k >= self.num_windows and oldk != k:
                    n = len(self.past_queue)
                    first = self.past_queue[-1]
                    todelete = first.keys()[0]
                    while todelete == first.keys()[0]:
                        self.past_queue.pop()
                        first = self.past_queue[-1]

                self.past_queue.insert(0,{k:status})
                oldk = k
                #pusher_client.trigger('messages', 'update', jObj)
                self.prediction()
                #print 'queue', self.past_queue

class Command(BaseCommand):
    help = ' Polls data from SQS and sends data through celery'
    
    def handle(self, *args, **options):
        q = Queue()
        q.poll()

        
