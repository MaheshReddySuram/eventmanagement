from django.db import models

# Create your models here.
class event_type:
    type_id:int
    type:str
    


class events:
    e_id:str
    event_name:str
    event_organizer:str
    event_type:str
    venue:str
    age_restriction:str
    description:str
    date:str
    time:str
    capacity:str
    cost:str
    org_email:str

class users:
    email:str
    password:str
    nationality:str
    gender:str
    usertype:str
    dob:str
    State_ID:str
    age:str
    isActive:str

class messages:
    sl_no:str
    email:str
    mobile:str
    city:str
    subject:str
    message:str
    
class payments:
    pay_id:str
    e_id:int
    email:str
    amount:int
    datetime:str



    

