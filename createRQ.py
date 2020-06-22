from app.backgoundJobs import foo
from rq import Queue
from worker import conn

q = Queue(connection=conn)
#result = foo(15,40)
result = q.enqueue(foo, 225,250)
print("\nIn calling program createRQ:  function foo with arguments start=25, end=55 returned a count of ", result)
