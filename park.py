from flask import Flask, jsonify,request
import time
from decouple import config


app = Flask(__name__)

def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


number_of_slots=config('number_of_slots')
if(is_int(number_of_slots)):
    number_of_slots=int(number_of_slots)
else:
    number_of_slots=100     # If invalid integer is passed in env then it will consider 100 as total slots
  

slots=[0]*number_of_slots       # Let there are N slots, so create a list with N Zero's
ip={}





@app.route("/", methods=['GET','POST'])
def index():
    if(request.method=='POST'):
        some_json=request.get_json()
        return jsonify({'you sent':some_json}),201
    else:
        return jsonify({"about":"Home Page"})
        #return jsonify({'ip': request.remote_addr}), 200




@app.route('/check/<num>',methods=['GET'])  # Takes input Car Number and gives output of Car Name parked at that slot
def get_check(num):
    flag=0
    for i in range(100):
        if(str(num)==str(slots[i])):
            flag=1
            return jsonify({'available at slot':i})
    if(flag==0):
        return "This car is not available in the parking"




@app.route('/park/<int:slotnumber>/<carnumber>',methods=['GET'])  # Takes input for slotnumber and carnumber to register 
def get_park(slotnumber,carnumber):
    
    if(slotnumber>=0 and slotnumber<=100):
        slots[slotnumber]=carnumber
        return jsonify({str(slotnumber):carnumber})
    return "PLease enter valid slot"




@app.route('/info/<num>',methods=['GET'])   # Takes input as either Slotnumber or Vehicle Number
def get_info(num):
    if(is_int(num)):      # If user_input is slotnumber
        num=int(num)
        if(slots[num]==0):
            return "No Vehicle Parked at this slot"
        else:
            return jsonify({'Vehicle at slot '+str(num) :slots[num]})
    else:       # If user_input is Vehicle Number
        for i in range(100):
            if(str(num)==str(slots[i])):
                flag=1
                return jsonify({'Available at slot':i})
        if(flag==0):
            return "This car is not available in the parking"      



@app.route('/unpark/<int:slotnum>',methods=['GET'])  # Takes input as slotnumber to free up the slot
def get_unpark(slotnum):
    if(slots[slotnum]==0):
        return "This slot is already free"
    else:
        slots[slotnum]=0
        return "Slot Number "+str(slotnum)+" is now freed"



@app.route('/show',methods=['GET'])  # Returns all slots information
def get_show():
    d={}
    for i in range(100):
        if(slots[i]!=0):
            d[i]=slots[i]           # Converting list to dictionary
    return jsonify(d)   

@app.errorhandler(404)   # Redirects all the invaliud requets
def not_found(e):
  return "Wrong Request"

    

@app.before_request             # Runs the function whenever request is made
def everyrequest():
    address = request.remote_addr       # Fetch the ip address of user
    request_limit = 10   # number of requests
    interval = 10        # per n seconds
    if address not in ip or time.time() > ip[address]['expires']:
        ip[address] = {
            'expires' : time.time() + interval,
            'remaining' : request_limit
        }
    if time.time() <= ip[address]['expires']:
        if ip[address]['remaining'] > 0:
            ip[address]['remaining'] -= 1
        else:
            return "Too many request in 10 seconds"
    
        
            




if __name__=='__main__':
    app.run(debug=True)
