import time
import serial  # 导入模块
import threading
STRGLO = ""  # 读取的数据
BOOL = True  # 读取标志位
ser = serial.Serial()


#打开串口
# 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
# 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
# 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
def DOpenPort(portx,bps,timeout):
    ret=False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
        #判断是否打开成功
        if(ser.is_open):
           ret=True
           threading.Thread(target=ReadData, args=(ser,)).start()
    except Exception as e:
        print("---异常---：", e)
    return ser, ret



#关闭串口
def DColsePort(ser):
    global BOOL
    BOOL=False
    ser.close()


#读数代码本体实现
def ReadData(ser):
    global STRGLO,BOOL
    # 循环接收数据，此为死循环，可用线程实现
    time.sleep(0.01)
    data = []
    while BOOL:
        if ser.in_waiting:
            STRGLO = ser.read(ser.in_waiting).hex()  # .decode("gbk")
            FIRST = 0
            end = 0
            for str_glo in STRGLO:
                first = FIRST+end
                end = first+2
                data.append(int(STRGLO[first:end],16))
                if end == len(STRGLO):
                    break
            print(data)



def DReadPort():
    global STRGLO
    str=STRGLO
    STRGLO=""#清空当次读取
    return str


#写数据
def DWritePort(ser,text):
    result = ser.write(text)  # 写数据
    return result


def open_serial_s():
    global ser
    ser = serial.Serial("COM4", 115200)


def test(a,b,c,*args):
    if len(args)>0:
        e = int(str(args).replace("(", '').replace(")", '').replace(",", ''))
        print(e)
    print(a, b, c)

if __name__ == "__main__":
    # ser, ret = DOpenPort("COM4", 115200, None)
    # data = '3A0103A34800020F0D0A'
    # data = bytes.fromhex(data)
    # if(ret==True):#判断串口是否成功打开
         #count=DWritePort(ser, data)
         #print("写入字节数：", count)
         #time.sleep(0)
         #DReadPort() #读串口数据
         #DColsePort(ser)  #关闭串口
    # coding:utf-8
    test(1, 2, 3)