# Redis Queue
Welcome to this repo. In here I want to give a most basic example of using the **python rq** library for someone who has neither used redis, nor rq ever before. As a beginner myself, I was motivated by the lack of ressources on this topic and a bug which was never encountered before and took me days to solve by mere luck. For details you can check out the [stackoverflow thread](https://stackoverflow.com/questions/76593563/redis-queue-task-is-queued-but-never-executed?noredirect=1#comment135071141_76593563).

### 1. Initialize the Redis server
For the redis-worker to run we need to have a redis server running, the easiest way is running it locally on your mashine. You can see how to install redis on your mashine on the [official redis documentation](https://redis.io/docs/getting-started/installation/)
Once this is installed you will have access to several new commands: *redis-server* to start your server and *redis-cli* to connect to that server to run commands . Now, you can try running ```redis-server``` in another terminal (You should get a nice confirmation that the server is up and running) and then run ```redis-cli ping``` in another one, this should return the word PONG, which means everything is working perfectly.

### 2. activate the Redis Worker
The **worker** is the part of the **redis queue** which processes the task in the background. We first need to install the redis-queue library by doing ```pip install rq```. Now we should be able to run the ```rq worker default``` command. This will initialize a worker which will listen to the **default** queue (you can change it however you want but remember the name, you will need it later.)

### 3. create a queue and feed it a task
Now we are going to create the queue itself which will take tasks, and let the worker run these tasks.
Unfortunately, at this moment, the rq library can only take external functions, which mean we need to create a **python package**. For this, we first create a folder in our directory (in this case I will call it testModule), which should contain two .py files: __init__ and the file with the task itself (I named it testFile). For testing purposes we will do a very simple task, which takes a number of seconds to wait and then prints something out (this will go into the testFile.py).

``` python
import time

def testFunction(seconds):
    print("start")
    time.sleep(seconds)
    print("end")
```
In order to make the directory a real package we need to add an __init__.py file. I will not be going indepth on how and why to write an init file, so in this case we will just add the following to the file to make our function importable later on:

``` python
from .testFile import *
```

Our project structure now looks like this:

```
project/
├── main.py
└── testModule/
    ├── __init__.py
    └── testFile.py
```

Now we will get to the most important part: initializing the queue. For that we first run ```pip install redis``` to be able to connect to our redis server inside python. Into our main.py file we write the following:

``` python
from redis import Redis
from rq import Queue

from testModule.testFile import testFunction

conn = Redis()
q = Queue("default", connection=conn)

job = q.enqueue(testFunction,
                5)
```

Here we first import our redis, and rq package, as well as our own function. By running *Redis()* We can connect to a redis server on a specific adress and port, however since we run it locally, we can just leave it empty and use the default parameters. next we create a queue called "default" into which we insert our function (the 5 is the input to the function, in this case it is the time it should wait. If you have multiple inputs, you just add another one, separated by a comma, f.e. (testFunction, 5, "hello", [1, 3, 4])).This will return the job, from which we can extract information like the job-id, -state, and more. If you now open the terminal window with the worker running you should see the print statements of our function.



## debugging
1. If you get an error message while running the command and this isn't your first time using redis, theres a good chance you have a server running in the background and blcoking the port. Try running ```redis-cli shutdown```

2.  If you get "ValueError: Invalid attribute name: <function path>", usually your package is not being imported correctly. Another bug that I personally experienced and which motivated me to make this repo is using the built in mac terminal, which yielded me the error for no reason. If you encounter this, try running both the main.py and the worker in f.e. the builtin vscode terminal and use the same virtual environment for both. Also make sure that when you are calling rq worker, your working directory is where your main python file and module is located.

More bugs or solutions? Add a pull request or message me!
