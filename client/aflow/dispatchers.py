

"""
Aflow event dispatchers
"""



import asyncio

class ActionDispatcher(object):

    def __init__(self, debug=False):
        """Initialize Store"""
        self.queues = []
        self.debug = debug

    def connect(self, observer):
        """
        Connect observer to store,
        where observer is a function with dispatch loop.
        """
        # Create a new message queue
        queue = asyncio.Queue()

        # Execute observer on event loop
        asyncio.ensure_future(observer(self.dispatch, queue))
        self.queues.append(queue)

    def dispatch(self, action):
        """Dispatch a message to all observers"""
        if self.debug:
            print("Dispatching: {}".format(action))
            print("------------------------")

        for q in self.queues:
            asyncio.async(q.put(action))


