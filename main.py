from redis import Redis
from rq import Queue

from testModule.testFile import testFunction

conn = Redis()
q = Queue("default", connection=conn)

job = q.enqueue(testFunction,
                5)
