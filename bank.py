from Deque import Deque
from Client import Client
operators = [{
    "title": "Office A",
    "number": 1,
    "service": ["business"],
    "customer": None,
    "type": "office",
    "queue": None
},
{
    "title": "Office B",
    "number": 2,
    "service": ["business"],
    "customer": None,
    "type": "office",
    "queue": None
},
{
    "title": "Cash A",
    "number": 3,
    "service": ["cash", "payment"],
    "customer": None,
    "type": "cash",
    "queue": None
},
{
    "title": "Counter A",
    "number": 4,
    "service": ["private", "mortgage"],
    "customer": None,
    "type": "counter",
    "queue": None
},
{
    "title": "Counter B",
    "number": 5,
    "service": ["private", "mortgage"],
    "customer": None,
    "type": "counter",
    "queue": None
},
{
    "title": "Counter C",
    "number": 6,
    "service": ["private", "mortgage"],
    "customer": None,
    "type": "counter",
    "queue": None
}]

class Operator():
    def __init__(self, new_operator):
        self.title = new_operator.get("title")
        self.number = new_operator.get("number")
        self.service = new_operator.get("service")
        self.type = new_operator.get("type")
        self.customer = new_operator.get("customer")
        self.queue = new_operator.get("queue")
        self.prefix = new_operator.get("prefix")
    
    def take_client(self):
        message = None
        if self.queue.len() > 0:
            self.customer = self.queue.get_front()
            self.queue.pop_front()
            print ("\n<-- RESULT:\tClient " + self.customer.code + " is assigned to " + self.title)
        else: message = "RESULT:\t" + self.type.upper() + " QUEUE is empty"
        return message
    
    def release_client(self):
        if self.customer != None:
            self.customer = None

class Bank():
    def __init__(self, operators):
        self.services = self.__service(operators)               #holds a list of available bank services
        self.__prefixes = self.__prefix_generator(operators)      #creating queue prefixes (for clients code constructing)
        active_queues = self.__queue_generator(operators)       #creating queue objects
        for element in operators: 
            element.update({"queue": active_queues[element["type"]], "prefix": self.__prefixes[element["type"]]})  #updating queue field in the starting operators list
        self.__content = [Operator(each) for each in operators]                       #creating and keeping operator objects from the starting operators list
        self.__active_queues = list (active_queues.values())                          #variable for keeping all queue objects 
        print ("BANK SHIFT")    
        print (*["Operator: " + each.title + "\tType: " + each.type + "\tService: " + ",".join(each.service) + "\tQueue Prefix: " + each.prefix for each in self.__content], sep = "\n")

    def __service (self, operators):        #obtaining all possible services from starting operators list         
        client_types = []
        for each in operators:
            client_types.extend(each.get("service"))
        return list(dict.fromkeys(client_types))

    def __prefix_generator(self, operators):        #creating prefixes for each bank counter type
        prefix_index = 90
        prefixes = dict.fromkeys([each.get("type") for each in operators])
        for each in prefixes: 
            prefixes.update({each: chr(prefix_index)})
            prefix_index -= 1
        return prefixes

    def __queue_generator(self, operators):         #creating queue objects for each bank counter type
        active_queues = dict.fromkeys([each.get("type") for each in operators])
        for each in active_queues: active_queues.update({each: Deque(each)})
        return active_queues

    def get_data (self):
        return self.__content

    def state_output (self):                #the operators load state output (table)
        max = 0
        for operator in self.__content:
            if len(operator.title) > max:
                max = len(operator.title)
        output_headings = [(" {:^" + str(max) + "} ").format(operator.title) for operator in self.__content]
        output_data = [(" {:^" + str(max) + "} ").format(operator.customer.code) if operator.customer!= None else (" {:^" + str(max) + "} ").format("None") for operator in self.__content]
        lid = ["-"*len(each) for each in output_headings]
        print("", *[each for each in lid], sep ="+", end = "+\n")
        print("", *[each for each in output_headings], sep = "|", end = "|\n")
        print("", *[each for each in lid], sep ="+", end = "+\n")
        print("", *[each for each in output_data], sep = "|", end = "|\n")
        print("", *[each for each in lid], sep ="+", end = "+\n")

    def queue_output(self):                 #the general queue otput in chronological order
        def sorting(element):
            return element.timestamp
        common_queue = []
        for each in self.__active_queues:
            common_queue += each.get_data()
        common_queue.sort(key=sorting)
        print ("\n~~~ BANK QUEUE ~~~")
        if len(common_queue) > 0:
            print (*["|{:^16}|".format(each.code) for each in common_queue], sep = "\n", end = "\n~~~~~~~~~~~~~~~~~~\n")
        else: print ("|{:^16}|".format("empty"), end = "\n~~~~~~~~~~~~~~~~~~\n")  

    def get_free_operator (self):           #searches all operators without clients
        free_operator = [each for each in self.__content if each.customer == None]
        return free_operator

    def find_operator(self, index):         #searches operator by his number
        operator = None
        for each in self.__content:
            if each.number == index:
                operator = each
        return operator

    def new_client (self, timestamp, client_type, queue):    #creating new client object 
        for each in self.__content:
            if client_type in each.service:
                prefix = each.prefix
                break
        code = prefix + str (queue.get_number())
        new_client = Client (code, client_type, timestamp)
        return new_client

    def remove_client(self, code):      #removing client object from queue
        queue = None
        client = None
        index = 0
        while index < len(self.__active_queues) and client == None:
            queue = self.__active_queues[index]
            client = queue.find(code)
            index += 1
        if client != None:    
            queue.remove(client)
            print(f"\nRESULT:\tClient {client.code} is REMOVED from the {queue.type.upper()} QUEUE")
        else: print ("\nClient with that code IS NOT FOUND!")


    def queue_definer(self, client_type):   #defining an appropriate queue for a client
        queue = None
        for each in self.__content:
            if client_type in each.service:
                queue = each.queue
                break
        return queue

        


