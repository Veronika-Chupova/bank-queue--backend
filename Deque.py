from Client import Client

class Deque:
    def __init__(self, type = None):
        self.type = type
        self.__content = []     #variable for holding queue elements
        self.__current_num = 1  #holds the number for the next client code in a queue
#----------GET Methods--------------
    def get_data(self):         #full queue data access
        return self.__content

    def get_front(self):        #head element access
        return self.__content[0]

    def get_rear(self):         #tail element access
        return self.__content[self.size-1]

    def len (self):             #queue size access
        return len(self.__content)

    def get_number(self):       #number for constracting next client code
        return self.__current_num
#----------SET Methods--------------
    def add_rear(self, new_element):    #addition to the end of queue
        self.__content.append(new_element)
        self.__current_num += 1 

    def add_front(self, new_element):   #addition to the head of queue
        self.__content.insert(0, new_element)

    def pop_front (self):               #removing head element
        self.__content.pop(0)

    def pop_rear (self):                #removing tail element
        self.__content.pop(self.__size-1)

    def find (self, code):              #client search by their code value
        client = None
        for each in self.__content:
            if each.code == code:
                client = each
                break
        return client

    def remove(self, client):           #client removing by their code value
        self.__content.remove(client)

