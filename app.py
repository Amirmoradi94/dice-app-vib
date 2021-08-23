
from flask import Flask,jsonify
from flask.globals import request
from filter_ import octavefilter
#from test_func import amir
#import numpy as np
#import timeit
from threading import Thread
#import concurrent.futures
#from multiprocessing.pool import ThreadPool


app = Flask(__name__) #intance of our flask application 

#Route '/' to facilitate get request from our flutter app
@app.route("/api", methods=["POST"])
def function():
    
    request_data = request.get_json()
    dataset = request_data["dataset"]
    

    #"""
    x.append(dataset[0])
    y.append(dataset[1])
    z.append(dataset[2])
    
    #"""
    #start = timeit.timeit()
    
    
    """
    pool = ThreadPool(processes=1)
    x_thread = pool.apply_async(octavefilter, x)
    return_val = x_thread.get()
    """
    
    
    class GetTitleThread(Thread):  
        def __init__(self, data):
            self.output = 0
            self.dataa = data
            super(GetTitleThread, self).__init__()
            
        def run(self):
            self.output = octavefilter(self.dataa)
            
    #xx = octavefilter(x)
    
    #x = [10, 20, 30, 40, 50, 60, 70]
    thread_x = GetTitleThread(x)
    #thread_y = GetTitleThread(y)
    #thread_z = GetTitleThread(z)
    
    thread_x.start()
    #thread_y.start()
    #thread_z.start()
    
    thread_x.join()
    #thread_y.join()
    #thread_z.join()
    
    
    xx = thread_x.output
    #yy = thread_y.output
    #zz = thread_z.output
    
        
    
    #x_thread = threading.Thread(target=octavefilter, args=(x, ))
    #y_thread = threading.Thread(target=octavefilter, args=(y, ))
    
    #x_thread.start()
    #y_thread.start()
    
    #x_thread.join()
    #y_thread.join()

    #stop = timeit.timeit()
    #print(stop-start)
    #"""


    #"""
    #print(np.sqrt(np.square(xx) + np.square(yy) + np.square(zz)))
    
    
    output = {"threshold": str(10000)}
    return jsonify(output)
    

if __name__ == "__main__":
        
    x , y, z = [], [], []
    #host= '192.168.2.23'
    
    app.run()

    
    
    
    
    
    
