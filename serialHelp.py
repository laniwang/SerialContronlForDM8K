import serial
import time


class SerialClass():
    def __init__(self, port='COM5', rate=38400):
        self.port=port  #端口号
        self.rate=rate  #波特率
        self.ser = None
##        self.alive = False
##        self.waitEnd = None
##        self.ID = None
        self.cmdString='' #命令行信息串，用于存储发送的单个命令
        self.data = ''
        self.serialConn()
        
    def serialConn(self):
        #COM4 or COM5      
        self.ser=serial.Serial(self.port, self.rate,timeout=5)
        if self.ser.isOpen==False:
            self.ser.open()
        self.ser.timeout=0.5  #读超时设置
        self.ser.writeTimeout=0.5 #写超时设置
        self.data =self.readSerial()
        print('Start serial info: ',self.data)
##        return self.ser,msg

    #读取串口缓冲数据 inWaiting()
    def readSerial_old(self):
        data = ''
        data = data.encode('utf-8')
        for i in range(3):  #执行三次读缓存数据，防止之前的数据未获取完全。
            n = self.ser.inWaiting()
##            print('%d. Read data ,n=  %d' %(i, n))
            if n:
                data=data+self.ser.read(n)
        print(data)
        datalist=data.decode().split('\r\n')
        print('Msg from serial : ' ,datalist)  #data转换string,经常变成多行
        #data=list(data.decode())
        return data
    
    def readSerial(self):
        '''
        读缓冲内存n,
        串口信息
        '''
        data=''
        data=data.encode('utf-8')
        m = self.ser.inWaiting()
        data=data+self.ser.read(m)  
        return data
    
    def writeSerial(self):
        '''
        写入，发送命令
        串口信息
        '''
        if self.ser.isOpen:
            if self.cmdString:
                self.ser.write(self.cmdString.encode())
        else:
            print('串口未打开或者命令信息不正确。')
            
    def serialClose(self):
        self.ser.close()
        
    def start3rd(self):
        self.ser.write(('3rdStart;'+'\r\n').encode('utf-8'))
        msg=self.readSerial()
        return msg

    def exit3rd(self):
        #COM4 or COM5      
        #ser=serial.Serial('COM5',38400,timeout=10)
        print('Exit 3rd function.')
        if self.ser.isOpen==False:
            self.ser=serial.Serial(self.port, self.rate,timeout=5)
            self.ser.open()
        self.ser.write(('exit;'+'\r\n').encode('utf-8'))
        msg=self.readSerial()
        return msg

    # Recived the message from serial port.
    # for recived the message afte Dynamic AGC send set command?
    def serialread_setCmd2(self):
        nullNum=0
        errorSigna=0
        rdMsg=''
        while True:
            rdMsg=self.ser.readline().decode()
            print('rdMsg value %s .' % rdMsg)
            if rdMsg!='' or rdMsg!='\r\n':
                if rdMsg.startswith('@ok'):
                    errorSigna=0
                    return errorSigna,rdMsg
                elif rdMsg.startswith('@er'):
                    print('faile-->'+ rdMsg)
                    errorSigna=1
                    return errorSigna,rdMsg
            nullNum=nullNum+1
            if nullNum>5:
                print('nullNum %d' % nullNum)  
                return errorSigna,rdMsg

    # Recived the message from serial port.
    # for recived the message afte Dynamic AGC send set command?
    def serialread_setCmd(self,module):
        nullNum=0
        errorSigna=0
        rdMsg=''
        while True:
            rdMsg=self.ser.readline().decode()
            if rdMsg!='' or rdMsg!='\r\n':
                if rdMsg.startswith('@ok ' + module):  #ok Dynamic_AGC'
                    print('OK-->'+rdMsg)
                    errorSigna=0
                    serInstance.readall() # pass @ok pitch command 20181206
                    return errorSigna,rdMsg
                elif rdMsg.startswith('@ok pitch'):
                    errorSigna=0
                    #print(rdMsg)
                    return errorSigna,rdMsg
                elif rdMsg.startswith('@er'):
                    print('faile-->'+ rdMsg)
                    errorSigna=1
                    return errorSigna,rdMsg
            nullNum=nullNum+1
            if nullNum>5:
                return errorSigna,rdMsg


    def read_getCmd(self):
        nullNum=0
        errorSigna=0
        rdMsg=''
        while True:
            rdMsg=self.ser.readline().decode()
            if rdMsg!='' or rdMsg!='\r\n':
                if rdMsg.startswith('@ok pitch'):
                    errorSigna=0
                    #print(rdMsg)
                    return errorSigna,rdMsg
                elif rdMsg.startswith('@er'):
                    print('faile-->'+ rdMsg)
                    errorSigna=1
                    return errorSigna,rdMsg
            nullNum=nullNum+1
            if nullNum>5:
                return errorSigna,rdMsg

# Write the log file.

def logWrite(cmdString,errorSign,msgString,moduleType):
    if errorSign==1 and msgString!='':
        with open(moduleType+'Error.txt','a') as f:
            f.write(cmdString)
            f.write(msgString)
    elif errorSign==0 and msgString!='': 
        with open(moduleType+'.txt','a') as f:
            f.write(cmdString)
            f.write(msgString)

def writeTxtFile(msgString,fileName):
    with open(fileName,'a') as f:
        f.write(msgString)
        f.write('\r\n')
    
if __name__ =='__main__':
    serialInstance=SerialClass()
    serialInstance.start3rd()
    serialInstance.exit3rd()
    serialInstance.serialClose()
