from RobotRaconteur.Client import *
import time

abb_gripper=RRN.ConnectService('rr+tcp://localhost:11222?service=abb_gripper')
abb_gripper.close()
time.sleep(2)
abb_gripper.open()
