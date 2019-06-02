import pyslinger
import random
import mysql.connector
import time
import unicodedata


protocol = "NEC"
gpio_pin_1 = 22
gpio_pin_2 = 27
protocol_config = dict()





Data_to_send = dict()


cnx = mysql.connector.connect(user='netuser', password='987', host='95.161.225.75', database='gitlab')
query = "SELECT * FROM gitlab.fpgaWebApiValues where device = 999 and ttype<11 ORDER BY Id DESC LIMIT 10"
#sql_insert = "INSERT INTO gitlab.airCondTempData (ttime, Cond1, Cond2, temp_1, temp_2, temp_3, temp_4, temp_5, temp_6, temp_7, temp_8, temp_9, temp_10 ) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"



def on_handle_1():
    ir = pyslinger.IR(gpio_pin_1, protocol, protocol_config)
    ir.send_code("10001000000000001100001011101")
    return "success"

def off_handle_1():
    ir = pyslinger.IR(gpio_pin_1, protocol, protocol_config)
    ir.send_code("10001000110000000000010100011")
    return "success"


def on_handle_2():
    ir = pyslinger.IR(gpio_pin_2, protocol, protocol_config)
    ir.send_code("10001000000000001100001011101")
    return "success"

def off_handle_2():
    ir = pyslinger.IR(gpio_pin_2, protocol, protocol_config)
    ir.send_code("10001000110000000000010100011")
    return "success"



def get_temps_sql():
    cursor = cnx.cursor()
    cursor.execute(query)
    A =[]
    for i in cursor:
        A.append(list(i))
    return A


def gen_rand_states():
    Cond1 = random.randint(0,1)
    Cond2 = random.randint(0,1)
    if Cond1 == 0:
        off_handle_1()
    if Cond1 == 1:
        on_handle_1()
    if Cond2 == 0:
        off_handle_2()
    if Cond2 == 1:
        on_handle_2()
    Data_to_send["Cond1"] = Cond1
    Data_to_send["Cond2"] = Cond2


def compact_send_data():
    gen_rand_states()
    Temps = get_temps_sql()
    Data_to_send["ttime"] = Temps[0][1]
    for i in range(10):
        name_of_temp = "temp_"+str(Temps[i][2])
        Data_to_send[name_of_temp] = Temps[i][4]
    for key, val in Data_to_send.items():
        if (key != "Cond1") and (key != "Cond2"):
            Data_to_send[key] = unicodedata.normalize('NFKD', val).encode('ascii','ignore')
    
    
    return Data_to_send

'''
def put_data_to_sql():
    Data = compact_send_data()
    val = (Data["ttime"], Data["Cond1"],Data["Cond2"], Data["temp_1"], Data["temp_2"],  Data["temp_3"],Data["temp_4"], Data["temp_5"], Data["temp_6"],  Data["temp_7"],Data["temp_8"], Data["temp_9"], Data["temp_10"])
    mycursor = cnx.cursor()
    mycursor.execute(sql_insert, val)
'''

if __name__ == '__main__':
    while(1):
        Data = compact_send_data()
        with open('need_data.txt', 'a') as the_file:
            the_file.write(str(Data))
            the_file.write('\n')
        time.sleep(600)


