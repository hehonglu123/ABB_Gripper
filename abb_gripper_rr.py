from relay_lib_seeed import *
import time, os, signal, argparse
import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.DateTimeUtil import DateTimeUtil
from RobotRaconteurCompanion.Util.SensorDataUtil import SensorDataUtil
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil

DEVICE_ADDRESS= 0x20

class create_gripper(object):
    def __init__(self, tool_info):
        self.port=1
        self.device_info = tool_info.device_info
        self.tool_info = tool_info
    def open(self):
        relay_off(self.port)
    def close(self):
        relay_on(self.port)

        
with RR.ServerNodeSetup("abb_gripper",50500) as node_setup:
    parser = argparse.ArgumentParser(description="G2 Gripper Driver for Robot Raconteur")
    parser.add_argument("--tool-info-file", type=argparse.FileType('r'),default=None,required=True,help="Tool info file (required)")
    args, _ = parser.parse_known_args()

    RRC.RegisterStdRobDefServiceTypes(RRN)

    with args.tool_info_file:
        tool_info_text = args.tool_info_file.read()
    info_loader = InfoFileLoader(RRN)
    tool_info, camera_ident_fd = info_loader.LoadInfoFileFromString(tool_info_text, "com.robotraconteur.robotics.tool.ToolInfo", "tool")
    
    attributes_util = AttributesUtil(RRN)
    tool_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(tool_info.device_info)

    gripper_inst=create_gripper(tool_info)
    service_ctx = RRN.RegisterService("tool","com.robotraconteur.robotics.tool.Tool",gripper_inst)
    service_ctx.SetServiceAttributes(tool_attributes)

    print("Press ctrl+c to quit")
    signal.sigwait([signal.SIGTERM,signal.SIGINT])
