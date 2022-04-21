from flask import Flask, jsonify, request, render_template
import board
from neopixel import NeoPixel
from time import sleep
from threading import Thread

pixels=NeoPixel(board.D18,60,auto_write=False)
fps=60
led_nb=60

class Pixel:
    def __init__(self, color , state = False):
        self.color = color
        self.state = state
    def __repr__(self):
        return str(color)
    def color_shift(self,shift):
        self.color += shift


class Color:
    def __init__(self,r,g,b):
        self.color = [r,g,b]
    def __add__(self,other): 
        if not(isinstance(other,Color)):
            raise TypeError("can't add a color to whatever the fuck you just passed to the function you dumb bitch")
        return Color(self.color[0]+other.color[0],self.color[1]+other.color[1],self.color[2]+other.color[2])


@app.route('/')
def main():
    return(render_template('index.html'))

@app.route('/switch', methods=['GET'])
def switch():
    status = request.args.get('status')

    if(status == "off"):
        l.state=False
        l.lock=False

    elif(status == "on"):
        l.state=True
    
    return(jsonify({"message":"switch"}))

@app.route('/lock', methods=['GET'])
def lock():
    status = request.args.get('status')
    
    if(status == "off"):
        l.lock=False

    elif(status == "on"):
        l.lock=True

    return(jsonify({"message":"lock"}))

@app.route('/color', methods=['GET'])
def color():
    color = request.args.get('color')

    r=int(color[0:2],base=16)
    g=int(color[2:4],base=16)
    b=int(color[4:6],base=16)
    l.color=[r,g,b]
    l.mode="unicolore"

    return(jsonify({"message":"color"}))

@app.route('/script', methods=['GET'])
def script():
    script = request.args.get('script')
    if(script=="stop"):
        l.mode="unicolore"
    l.color=[255,0,0]
    l.mode=script
    
    return(jsonify({"message":"script"}))

th = Thread(target=update)
th.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

