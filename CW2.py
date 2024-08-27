import time, random
from Deque import Deque
from bank import Bank, operators

bank = Bank(operators) #set initial bank conditions
log = Deque()          #queue for completed clients
end_queue = False      

def client_generator(service_types):    #function for creating client with random service request
  winner = random.randint(0,len(service_types)-1)
  return service_types[winner]

while not end_queue:
  try: role = int (input ("\nIf you are a CLIENT press 1 / If you are a BANK WORKER press 2:\t"))
  except ValueError: 
    print ("\nIncorrect input. Please, follow instructions.\n")
    continue
#-----------CLIENT ROLE---------------#
  if role == 1:     
    try: command = int (input ("To GET IN the queue press 1 / To LEAVE the queue press 2:\t"))
    except ValueError: 
      print ("\nIncorrect input. Please, follow instructions.\n")
      continue
    #----new client creation----#
    if command == 1:  #put new client in a queue
      client_type = client_generator(bank.services)
      queue = bank.queue_definer(client_type)   #optimisation
      #new_client = queue.new_client(time.time(), client_type)    #output client object 
      new_client = bank.new_client(time.time(), client_type, queue)    #new version
      queue.add_rear(new_client)
      print ("\nNEW CLIENT\nType: ", client_type, "\nClient code: ", new_client.code)
      print(f"\n--> RESULT:\tClient {new_client.code} is put to the {queue.type.upper()} QUEUE")
      free_operators = bank.get_free_operator()
      if len(free_operators) > 0:
        for operator in free_operators: operator.take_client()
      bank.state_output()
      bank.queue_output()
    #----client withdrawal----#
    elif command == 2:  
      client_code = input ("\nEnter your CODE:\t")
      bank.remove_client(client_code.upper())
      bank.state_output()
      bank.queue_output()
    else: print ("\nIncorrect input. Please, follow instructions.\n")
#-----------WORKER ROLE---------------#
  elif role == 2: 
    try: command = int (input ("\nCHOOSE ACTION\nTo TAKE a client press 1 \nTo REDIRECT client press 2 \nTo TERMINATE the queue press 3 \n"))
    except ValueError: 
      print ("\nIncorrect input. Please, follow instructions.\n")
      continue
    #----take in a client from queue----#
    if command == 1:
      print ("\nWhich OPERATOR are you?", *[each.title + ": press " + str (each.number) for each in bank.get_data()], sep = "\n", end = "\n")
      try: operator_num = int (input ())
      except ValueError: 
        print ("\nIncorrect input. Please, follow instructions.\n")
        continue
      operator = bank.find_operator(operator_num)
      if operator != None:
        log.add_rear(operator.customer)
        operator.release_client()
        message = operator.take_client()
        if message != None: print (message)
        bank.state_output()
        bank.queue_output()
      else: print ("\nIncorrect input. Please, follow instructions.\n")
    #----redirect a client----#
    elif command == 2: 
      print ("\nWhich OPERATOR are you?", *[each.title + ": press " + str (each.number) for each in bank.get_data()], sep = "\n", end = "\n")
      try: donor = int (input (""))
      except ValueError: 
        print ("\nIncorrect input. Please, follow instructions.\n")
        continue
      operator_from = bank.find_operator(donor)
      if operator_from.customer != None:
        try: acceptor = int (input ("--> Destination OPERATOR: "))
        except ValueError: 
          print ("\nIncorrect input. Please, follow instructions.\n")
          continue
        operator_to = bank.find_operator(acceptor)
        queue = operator_to.queue
        queue.add_front(operator_from.customer)
        print(f"\n--> RESULT:\tClient {operator_from.customer.code} is put to the {queue.type.upper()} QUEUE")
        operator_from.release_client()
        free_operators = bank.get_free_operator()
        if len(free_operators) > 0:
          for operator in free_operators: operator.take_client()
        bank.state_output()
        bank.queue_output()
      else: print ("You DON'T have clients on service!")
    #----stop queue and exit----#
    elif command == 3:  
      end_queue = True
      if log.len()>0:
        print ("Log of the day shift: ", *[each.code for each in log.get_data()])
      print ("BANK SHIFT IS STOPPED")
    else: print ("\nIncorrect input. Please, follow instructions.\n")
  else: print ("\nIncorrect input. Please, follow instructions.\n")

