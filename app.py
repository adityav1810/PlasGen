from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import googlemaps
import requests
import json

api_key ='AmcOdmGz9jdNkCj3m5ZcKcl--ujJAKXhhKbEwAvlIxqRAbn6ASA1vhjabbkfqe6e'




app = Flask(__name__)
app.config['SECRET_KEY'] = 'thirdfloor@bennett.edu.in'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False

db=SQLAlchemy(app)

class patientdb(db.Model):
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  p_name=db.Column(db.String(20),nullable=False)
  p_mobile_number = db.Column(db.String(120), nullable=False)
  p_emailid=db.Column(db.String(120), nullable=False)
  p_bloodgroup = db.Column(db.Boolean())
  p_res_address=db.Column(db.String(200), nullable=False)
  p_hospital_name=db.Column(db.String(200), nullable=False)
  p_lat=db.Column(db.Float(),nullable=False)
  p_long=db.Column(db.Float(),nullable=False)
  
  def __init__(self,p_name,p_mobile_number,p_emailid,p_bloodgroup,p_res_address,p_hospital_name,p_lat,p_long):
    
    self.p_name=p_name
    self.p_mobile_number=p_mobile_number
    self.p_emailid=p_emailid
    self.p_bloodgroup=p_bloodgroup
    self.p_res_address=p_res_address
    self.p_hospital_name=p_hospital_name
    self.p_lat=p_lat
    self.p_long=p_long

db.create_all()
  
def get_lat_long(PLACENAME):
  res = requests.get('https://api.opencagedata.com/geocode/v1/json?q='+str(PLACENAME)+'&key=380fff14ffb34ff28ce975610872242f')
  response=res.text
  req_data = json.loads(response) 
  result = req_data['results'][0]['geometry']
  patient_lat=result['lat']
  patient_long=result['lng']

  return patient_lat,patient_long

def add_new_patient(patient_name,patient_mobile_number,patient_emailid,patient_bloodgroup,patient_addr,patient_hospitalname):
  
  patient_lat,patient_long=get_lat_long(patient_addr)
  
  
  
  patient_data=patientdb(patient_name,patient_mobile_number,patient_emailid,patient_bloodgroup,patient_addr,patient_hospitalname,float(patient_lat),float(patient_long))
  db.session.add(patient_data)
  db.session.commit()
  
def get_data():
  data = patientdb.query.all()
  return data


@app.route("/",methods=['GET', 'POST'])
def team():
  # add_new_patient("Adotya","9810368362",'ad@bu.com',0,"E-30, Greater Kailash-3","PSRI")
  print(get_data())
  
  return render_template('home.html') 




@app.route("/find")
def getrouteinfo():
  print(get_lat_long('Greater Kailash 2'))
  
  sourcelat=28.558100
  sourcelong=77.229393
  destlat=28.644680
  destlong=77.303590
  
  res=requests.get('https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins='+str(sourcelat)+','+str(sourcelong)+'&destinations='+str(destlat)+','+str(destlong)+'&travelMode=driving&key='+str(api_key))
  response=res.text
  shortestdist=[]

  req_data = json.loads(response) 
  traveldist=req_data["resourceSets"][0]["resources"][0]["results"][0]["travelDistance"]
  mintime=req_data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"]
  
  print(traveldist,mintime)
  
  return req_data 



  


if __name__ == '__main__':
  app.run(debug=True)

  