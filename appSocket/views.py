import json
import threading
import time

import serial  # 导入模块
import serial.tools.list_ports
from django.http import HttpResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket

STRGLO = ""  # 读取的数据
BOOL = True  # 读取标志位
# 设置ser_1 ser_2全局变量，默认值为serial对象
ser_1 = serial.Serial()
ser_2 = serial.Serial()


def websocket_g2(req):
    return render(req, 'webSoketG2.html')


def modify_message(message):
    return message.lower()


# 写数据实现
def WriteData(request, ser1, ser2, data2, data3, *args):
    global BOOL
    try:
        if len(args) > 0:
            start = 0
            BOOL = True
            end = int(str(args).replace("(", '').replace(")", '').replace(",", ''))
            while BOOL:
                start = start+1
                if start > end:
                    BOOL = False
                    break
                print(BOOL)
                print(type(data2))
                print("xie数据", data2, data3)
                data_2 = bytes.fromhex(data2)
                data_3 = bytes.fromhex(data3)
                print(data2)
                result = ser1.write(data_2)  # 写数据
                result2 = ser2.write(data_3)
                print("写总字节数:", result, result2)
                time.sleep(0.3)
        else:
            BOOL = True
            while BOOL:
                print(BOOL)
                print(type(data2))
                print("xie数据",data2,data3)
                data_2 = bytes.fromhex(data2)
                data_3 = bytes.fromhex(data3)
                print(data2)
                result = ser1.write(data_2)  # 写数据
                result2 = ser2.write(data_3)
                print("写总字节数:", result, result2)
                time.sleep(0.3)
    except Exception as e:
        print("异常--", e)


# 读数代码本体实现
def ReadData(request, ser, ser2,):
    global STRGLO,BOOL
    BOOL = True
    # 循环接收数据，此为死循环，可用线程实现
    data = []
    b = 0
    data_message = []
    while BOOL:
        a = 0  # 结束while标志
        if ser.in_waiting and ser2.in_waiting:
            b = b+1
            print('字节数：', ser.in_waiting, ser2.in_waiting)
            if(b==5 or b==6):
                STRGLO = ser.read(2).hex()  # .decode("gbk")
                STRGLO2 = ser2.read(2).hex()
                print('5-6', len(STRGLO),  len(STRGLO2))
            else:
                STRGLO = ser.read(1).hex()  # .decode("gbk")
                STRGLO2 = ser2.read(1).hex()
                print('数据', len(STRGLO), len(STRGLO2))
            FIRST = 0
            end = 0
            for str_glo, str_glo2 in zip(STRGLO, STRGLO2):
                first = FIRST+end
                if b == 5 or b == 6:
                    end = first+4
                    data_message.append(int(STRGLO[first:end], 16))
                    data_message.append(int(STRGLO2[first:end], 16))
                    if b==6:
                        print(data_message)
                        request.websocket.send(json.dumps(data_message))
                else:
                    end = first + 2
                data.append(int(STRGLO[first:end], 16))
                if(len(data) > 1):
                    if(data[len(data)-2]==13 and data[len(data)-1] == 10):
                        a = 1
                        # 初始化变量
                        b = 0
                        data_message.clear()
                        data.clear()
                        print("数据传输结束")
                if end == len(STRGLO):
                    break
        # if (a == 1):
        #    print("结束while")
        #     break
    #request.websocket.send(json.dumps(data))

# 启动收发数据线程
def DOpenPort(request, data2, data3):
    global ser_1
    global ser_2
    # portx 端口  bpx 波特率  timeout超时设置
    try:
        #判断是否打开成功
        if(ser_1.is_open and ser_2.is_open):
            threading.Thread(target=ReadData, args=(request, ser_1, ser_2,)).start()
            threading.Thread(target=WriteData, args=(request, ser_1, ser_2, data2, data3,)).start()
            print("ck", ser_1, ser_2)
        else:
            print("ck", ser_1, ser_2)
            request.websocket.send(json.dumps(0))
    except Exception as e:
        print("---异常---：", e)
    return ser_1, ser_2


# 启动收发数据线程
def DOpenPort2(request, data2, data3, data4):
    global ser_1
    global ser_2
    # portx 端口  bpx 波特率  timeout超时设置
    try:
        #判断是否打开成功
        if(ser_1.is_open and ser_2.is_open):
            threading.Thread(target=ReadData, args=(request, ser_1, ser_2,)).start()
            threading.Thread(target=WriteData, args=(request, ser_1, ser_2, data2, data3, int(data4))).start()
            print("ck", ser_1, ser_2)
        else:
            print("ck", ser_1, ser_2)
            request.websocket.send(json.dumps(0))
    except Exception as e:
        print("---异常---：", e)
    return ser_1, ser_2


# 收发数据
@accept_websocket
def echo_two(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'login.html')
    else:
        for message in request.websocket:
            data2 = message.decode('utf-8')
            data3 = data2.split(',')
            # request.websocket.send(message)#发送消息到客户端
            #data = message.decode('utf-8')
            #print(type(data))
            #print(data)
            if len(data3)>2:
                DOpenPort2(request, data3[0], data3[1], data3[2])
            else:
                DOpenPort(request, data3[0], data3[1])


# 扫描串口
@accept_websocket
def port_number(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'login.html')
    else:
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("没有发现端口!")
        else:
            port = []
            for PLIST in list(plist):
                port.append(PLIST[0])
            request.websocket.send(json.dumps(port))

# 打开通道1
def open_serial_1(req):
    state = {"message": None}
    global ser_1
    try:
        com1 = req.POST.get("COM1")
        if ser_1.is_open:
            # 已经打开
            state["message"] = 0
        else:
            ser_1 = serial.Serial(com1, 115200, timeout=None)
            state["message"] = 1   # 打开成功
    except Exception as e:
        return e
    data = json.dumps(state)
    return HttpResponse(data)


# 关闭通道1
def close_serial_1(req):
    state = {"message": None}
    global ser_1
    try:
        if ser_1.is_open:
            # 已经打开
            ser_1.close()  # 关闭成功
            state["message"] = 0
        else:

            state["message"] = 1   # 串口未打开
    except Exception as e:
        return e
    data = json.dumps(state)
    return HttpResponse(data)


# 打开通道2
def open_serial_2(req):
    state = {"message": None}
    global ser_2
    try:
        com2 = req.POST.get("COM2")
        if ser_2.is_open:
            # 已经打开
            state["message"] = 0
        else:
            ser_2 = serial.Serial(com2, 115200, timeout=None)
            state["message"] = 1   # 打开成功
    except Exception as e:
        return e
    data = json.dumps(state)
    return HttpResponse(data)


# 关闭通道2
def close_serial_2(req):
    state = {"message": None}
    global ser_2
    try:
        if ser_2.is_open:
            # 已经打开
            ser_2.close()  # 关闭成功
            state["message"] = 0
        else:
            state["message"] = 1   # 串口未打开
    except Exception as e:
        return e
    data = json.dumps(state)
    return HttpResponse(data)


# 停止采集
def stop(req):
    state = {"message": None}
    global BOOL
    try:
        if BOOL:
            BOOL = False
            state["message"] = 1
        else:
            state["message"] = 0
    except Exception as e:
        print("stop异常", e)
    data = json.dumps(state)
    return HttpResponse(data)