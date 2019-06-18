import pyslinger
from flask import Flask

app = Flask(__name__)
protocol = "NEC"
gpio_cond_2_out = 22
gpio_cond_1_out = 27
protocol_config = dict()


commands = dict()
commands["on"] = "10001000000000001100001011101" #27 gradus on
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






@app.route('/cond1/<command>')
def handle_for_cond1(command):
    ir = pyslinger.IR(gpio_cond_1_out, protocol, protocol_config)
    ir.send_code(commands[command])
    return "success"
    

@app.route('/cond2/<command>')
def handle_for_cond2(command):
    ir = pyslinger.IR(gpio_cond_2_out, protocol, protocol_config)
    ir.send_code(commands[command])
    return "success"
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

    #11000100000000000110000101110 - vkl (27)
    #10001000110000000000010100011 - vykl

