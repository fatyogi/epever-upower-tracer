#!/usr/bin/python
import sys, getopt
import time
from UPower import *

MaxAttempts = 10

def main(argv):

   status = "none"

   try:
      opts, args = getopt.getopt(argv,"hi:")
   except getopt.GetoptError:
      print(sys.argv[0], ' -i on|off')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(sys.argv[0]," -i on|off")
         print("Switches invertor on and off")
         sys.exit()
      elif opt in ("-i"):
         status = arg
   
   up = UPower()
   if (up.connect() < 0):
      print("Could not connect to the device")
      exit -2
 
   
   newstat = 0
   if (status == "on"): newstat = 1

   for x in range(MaxAttempts):
        instat = up.getIV()
        if (instat == newstat): break
        print("Inverter status", instat)
        print('Setting invertor to', newstat)
        up.switchIV(newstat)
        time.sleep(3)
  

# main call
if __name__ == "__main__":
   main(sys.argv[1:])
