import pyslinger
import random
import mysql.connector
import time
import unicodedata
import datetime


protocol = "NEC"
gpio_cond_2_out = 22
gpio_cond_1_out = 27
protocol_config = dict()





Data_to_send = dict()


cnx = mysql.connector.connect(user='netuser', password='987', host='95.161.225.75', database='gitlab')
query = "SELECT * FROM gitlab.fpgaWebApiValues where device = 999 and ttype<11 ORDER BY Id DESC LIMIT 10"
#sql_insert = "INSERT INTO gitlab.airCondTempData (ttime, Cond1, Cond2, temp_1, temp_2, temp_3, temp_4, temp_5, temp_6, temp_7, temp_8, temp_9, temp_10 ) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

commands = dict()
must = dict()
must["on"] = "10001000000000001100001011101" 
commands["off"] = "10001000110000000000010100011"
commands["on16l"] = "10001000000010000001000010011"
commands["on16m"] = "10001000000010000001001010111"
commands["on16h"] = "10001000000010000001010011011"
commands["on23l"] = "10001000000010001000000000001"
commands["on23m"] = "10001000000010001000001000101"
commands["on23h"] = "10001000000010001000010001001"
commands["on30l"] = "10001000000011001111000010111"
commands["on30m"] = "10001000000011001111001011011"
commands["on30h"] = "10001000000011001111010011111"


def handle_command(command_type, cond_type):
    ir = pyslinger.IR(cond_type, protocol, protocol_config)
    ir.send_code(command_type)
    return "success"



def get_temps_sql():
    cursor = cnx.cursor()
    cursor.execute(query)
    A =[]
    for i in cursor:
        A.append(list(i))
    return A



def compact_send_data():
    Data_to_send["ttime"] = str(datetime.datetime.now())
    try:
        Temps = get_temps_sql()           
        Data_to_send["ttime"] = Temps[0][1]
        for i in range(10):
            name_of_temp = "temp_"+str(Temps[i][2])
            Data_to_send[name_of_temp] = Temps[i][4]
        for key, val in Data_to_send.items():
            if (key != "Cond1") and (key != "Cond2"):
                Data_to_send[key] = unicodedata.normalize('NFKD', val).encode('ascii','ignore') 
    except:
        for i in range(10):
            name_of_temp = "temp_"+str(i+1)
            Data_to_send[name_of_temp] = "no conn with mysql"
    return Data_to_send



if __name__ == '__main__':
    while(1):
        for command in commands:
            handle_command(must["on"],gpio_cond_1_out)
            time.sleep(1)
            handle_command(commands[command],gpio_cond_1_out)
            Data_to_send["Cond1"] = command
            for command in commands:
                handle_command(must["on"],gpio_cond_2_out)
                time.sleep(1)
                handle_command(commands[command], gpio_cond_2_out)
                Data_to_send["Cond2"] = command
                Data = compact_send_data()
                with open('need_data.txt', 'a') as the_file:
                    the_file.write(str(Data))
                    the_file.write('\n')
                time.sleep(1200)


