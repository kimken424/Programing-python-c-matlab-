import time
from ucl.common import byte_print, decode_version, decode_sn, getVoltage, pretty_print_obj, lib_version
from ucl.highCmd import highCmd
from ucl.highState_b1 import highState
from ucl.unitreeConnection import unitreeConnection, HIGH_WIFI_DEFAULTS, HIGH_WIRED_DEFAULTS
from ucl.enums import MotorModeHigh, GaitType
from ucl.complex import motorCmd


class myunitree:
    def __init__(self):
        self.hstateRPY=[0.0,0.0,0.0]
        


    def connect(self):

        self.conn = unitreeConnection(HIGH_WIFI_DEFAULTS)  # 네트워크 연결
        self.conn.startRecv()

        self.hcmd = highCmd()
        self.hstate = highState()

    def cmdInit(self):
        time.sleep(0.05)
        data = self.conn.getData()
        for paket in data:
            self.hstate.parseData(paket)

            self.highstate_info = f"SN [{byte_print(self.hstate.SN)}]:\t{decode_sn(self.hstate.SN)}\n" \
                             f"Ver [{byte_print(self.hstate.version)}]:\t{decode_version(self.hstate.version)}\n" \
                             f"SOC:\t\t\t{self.hstate.bms.SOC} %\n" \
                             f"Overall Voltage:\t{getVoltage(self.hstate.bms.cell_vol)} mv\n" \
                             f"Current:\t\t{self.hstate.bms.current} mA\n" \
                             f"Cycles:\t\t\t{self.hstate.bms.cycle}\n" \
                             f"Temps BQ:\t\t{self.hstate.bms.BQ_NTC[0]} °C, {self.hstate.bms.BQ_NTC[1]}°C\n" \
                             f"Temps MCU:\t\t{self.hstate.bms.MCU_NTC[0]} °C, {self.hstate.bms.MCU_NTC[1]}°C\n" \
                             f"FootForce:\t\t{self.hstate.footForce}\n" \
                             f"FootForceEst:\t\t{self.hstate.footForceEst}\n"
            self.hstateRPY=[self.hstate.imu.rpy[0],self.hstate.imu.rpy[1],self.hstate.imu.rpy[2]]
            self.motorQ=[]
            for i in range(20):
                self.motorQ.append(self.hstate.motorstate[i].q)

            # print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
            # print(f'SN [{byte_print(self.hstate.SN)}]:\t{decode_sn(self.hstate.SN)}')
            # print(f'Ver [{byte_print(self.hstate.version)}]:\t{decode_version(self.hstate.version)}')
            # print(f'SOC:\t\t\t{self.hstate.bms.SOC} %')
            # print(f'Overall Voltage:\t{getVoltage(self.hstate.bms.cell_vol)} mv')  # something is still wrong here ?!
            # print(f'Current:\t\t{self.hstate.bms.current} mA')
            # print(f'Cycles:\t\t\t{self.hstate.bms.cycle}')
            # print(f'Temps BQ:\t\t{self.hstate.bms.BQ_NTC[0]} °C, {self.hstate.bms.BQ_NTC[1]}°C')
            # print(f'Temps MCU:\t\t{self.hstate.bms.MCU_NTC[0]} °C, {self.hstate.bms.MCU_NTC[1]}°C')
            # print(f'FootForce:\t\t{self.hstate.footForce}')
            # print(f'FootForceEst:\t\t{self.hstate.footForceEst}')
            # print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')

    def sendCmd(self):
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        print(self.hcmd.mode)

        self.cmdInit()

   