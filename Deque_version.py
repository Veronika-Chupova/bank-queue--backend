from Client import Client

class Deque:
    def __init__(self, type = None):
        self.type = type
        self.__content = [] 
        self.__size = len(self.__content)
        self.__current_num = 1  
#----------GET Methods--------------
    def get_data(self):
        return self.__content

    def get_front(self):
        return self.__content[0]

    def get_rear(self):
        return self.__content[self.size-1]

    def len (self):
        return self.__size

    def get_number(self):
        return self.__current_num
#----------SET Methods--------------
    def add_rear(self, new_element):
        self.__content.append(new_element)
        self.__size = len(self.__content)
        self.__current_num += 1      #keep a code sequence

    def add_front(self, new_element):
        self.__content.insert(0, new_element)
        self.__size = len(self.__content)

    def pop_front (self):
        self.__content.pop(0)
        self.__size = len(self.__content)

    def pop_rear (self):
        self.__content.pop(self.__size-1)
        self.__size = len(self.__content)

    def find (self, code):    #return client object
        client = None
        for each in self.__content:
            if each.code == code:
                client = each
                break
        return client

    def remove(self, client):
        self.__content.remove(client)
        self.__size = len(self.__content)