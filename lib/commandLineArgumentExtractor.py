import sys

def tryToGetIdFromCommandLineArgument():

  #check there is a command line argument
  if len(sys.argv) != 2:
    print("#############################")
    print("Dooooom, requires id argument")
    print("#############################")
    sys.exit()

  clientId = sys.argv[1]

  print  "is ", clientId

  #check arg is an int
  try:
    clientId = int(clientId)
  except:
    print("##################################")
    print("Dooooom, argument must be a number")
    print("##################################")
    sys.exit()

  #check it is valid
  if clientId not in range(1,5):
    print("######################################################")
    print("Dooooom, argument is not legal must be in range 1 to 4")
    print("######################################################")
    sys.exit()

  return str(clientId)
