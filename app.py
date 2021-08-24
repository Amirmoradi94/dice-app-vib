
from flask import Flask, jsonify
from flask.globals import request
from filter_ import octavefilter
from threading import Thread

app = Flask(__name__) #intance of our flask application 

@app.route("/api", methods=["POST"])
def function():
    
    request_data = request.get_json()
    dataset = request_data["dataset"]

    x.append(dataset[0])
    y.append(dataset[1])
    z.append(dataset[2])
    

    class GetTitleThread(Thread):  
        def __init__(self, data):
            self.output = 0
            self.dataa = data
            super(GetTitleThread, self).__init__()
            
        def run(self):
            self.output = octavefilter(self.dataa)
            
            
    #xx = octavefilter(x)
    
    thread_x = GetTitleThread(x)
    thread_y = GetTitleThread(y)
    #thread_z = GetTitleThread(z)
    
    thread_x.start()
    thread_y.start()
    #thread_z.start()
    
    thread_x.join()
    thread_y.join()
    #thread_z.join()
    
    
    xx = thread_x.output
    yy = thread_y.output
    #zz = thread_z.output

    #print(np.sqrt(np.square(xx) + np.square(yy) + np.square(zz)))
    
    
    output = {"threshold": str(np.sqrt(np.square(xx) + np.square(yy)))}
    return jsonify(output)
    

if __name__ == "__main__":
        
    
    #host= '192.168.2.23'
    x , y, z = [], [], []
    app.run(threaded=True, use_reloader= False)

    
    
    
    
    
    
