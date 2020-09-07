from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import QStringListModel
from PyQt5.uic import loadUi
import sys
import pywifi

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
        self.pwdFiles=QFileDialog.getOpenFileNames(self, 'select files', '', 'txt files(*.txt)')
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
