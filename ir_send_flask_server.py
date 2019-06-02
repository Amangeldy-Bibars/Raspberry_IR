import pyslinger
from flask import Flask

app = Flask(__name__)
protocol = "NEC"
gpio_pin1 = 22
gpio_pin2 = 27
protocol_config = dict()


@app.route("/on1")
def on_handle1():
    ir = pyslinger.IR(gpio_pin1, protocol, protocol_config)
    ir.send_code("10001000000000001100001011101")
    return "success"
    

@app.route("/off1")
def off_handle1():
    ir = pyslinger.IR(gpio_pin1, protocol, protocol_config)
    ir.send_code("10001000110000000000010100011")
    return "success"


@app.route("/on2")
def on_handle2():
    ir = pyslinger.IR(gpio_pin2, protocol, protocol_config)
    ir.send_code("10001000000000001100001011101")
    return "success"
    

@app.route("/off2")
def off_handle2():
    ir = pyslinger.IR(gpio_pin2, protocol, protocol_config)
    ir.send_code("10001000110000000000010100011")
    return "success"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

    #11000100000000000110000101110 - vkl (27)
    #10001000110000000000010100011 - vykl
