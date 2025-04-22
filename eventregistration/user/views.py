from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from datetime import datetime
from .models import event_type
from django.core.files.storage import FileSystemStorage

from .models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Create your views here.

# --------------------------------------------------------------------------------
# Main Webpage Views(USER)
# --------------------------------------------------------------------------------
def index(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['email']
        mobile = request.POST['mobile']
        city = request.POST['city']
        subject = request.POST['subject']
        message = request.POST['message']

        mycursor.execute("insert into messages(email,mobile,city,subject,message) values('" +
                         email+"','"+mobile+"','"+city+"','"+subject+"','"+message+"')")
        conn.commit()
        return redirect('index')
    else:
        return render(request, 'index.html')

# --------------------------------------------------------------------------------


def login(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        mycursor = conn.cursor()
        # retrive post details

        uname = request.POST['email']
        pwd = request.POST['password']

        mycursor.execute("select * from user where email='" +
                         uname+"' and password='"+pwd+"' and isActive=1")
        result = mycursor.fetchone()
        if (result != None):
            request.session['username'] = uname
            return redirect('index1')
            # redirect('studenthome')
        else:
            return render(request, 'login.html', {'status': 'Wrong Username or Password!'})
    else:
        return render(request, 'login.html')
# --------------------------------------------------------------------------------


def registration(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['email']
        pwd = request.POST['password']
        nationality = request.POST['nationality']
        gender = request.POST['gender']
        usertype = request.POST['usertype']
        dob = str(request.POST['dob'])
        State_ID = request.POST['State_ID']

        if usertype == 'eventmanager':
            mycursor.execute("insert into user(email,password,nationality,gender,usertype,dob,State_ID,age) values('" +
                             email+"','"+pwd+"','"+nationality+"','"+gender+"','"+usertype+"','"+dob+"','"+State_ID+"',TIMESTAMPDIFF(YEAR,'"+dob+"', CURDATE()))")
        else:
            mycursor.execute("insert into user(email,password,nationality,gender,usertype,dob,State_ID,age,isActive) values('" +
                             email+"','"+pwd+"','"+nationality+"','"+gender+"','"+usertype+"','"+dob+"','"+State_ID+"',TIMESTAMPDIFF(YEAR,'"+dob+"', CURDATE()),1)")
        conn.commit()
        return redirect('login')

    else:
        return render(request, 'registration.html')

# --------------------------------------------------------------------------------


def get_events(request):
    if "username" in request.session:
        # uname = request.session['username']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from event")
        result = mycursor.fetchall()
        e = []
        for row in result:
            obj = events()
            obj.event_name = row[1]
            obj.event_organizer = row[2]
            obj.event_type = row[3]
            obj.venue = row[4]
            obj.age_restriction = row[5]
            obj.description = row[6]
            obj.date = row[7]
            obj.time = row[8]
            obj.capacity = row[9]
            obj.cost = row[10]
            e.append(obj)
        # Get all events
        mycursor = conn.cursor(dictionary=True)

        mycursor.execute("SELECT * FROM event")
        events_list = mycursor.fetchall()
         # Get registered events for this user
        registered_events = []
        mycursor.execute("SELECT e_id FROM event_register WHERE email=%s", (uname,))
        for row in mycursor.fetchall():
            registered_events.append(row['e_id'])
        
        return render(request, 'showevents.html', {
            'events': events_list,
            'username': uname,
            'registered_events': registered_events
        })
    else:
         return render(request, 'login.html')
# --------------------------------------------------------------------------------


def profile(request):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from user where email='"+uname+"'")
        result = mycursor.fetchall()
        p = []
        for row in result:
            obj = users()
            obj.email = row[0]
            obj.password = row[1]
            obj.nationality = row[2]
            obj.gender = row[3]
            obj.usertype = row[4]
            obj.dob = row[5]
            obj.State_ID = row[6]
            obj.age = row[7]
            obj.isActive = row[8]

            p.append(obj)
        # print(e)

        return render(request, 'profile.html', {'profile': p, 'username': uname})
    else:
        return render(request, 'login.html')
# --------------------------------------------------------------------------------


def password_recovery(request):

    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['username']

        mycursor.execute("select password from user where email='"+email+"'")

        result = mycursor.fetchone()
        pwd = str(result)
        if (result != None):
            # SMTP server configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'chanakya2105@gmail.com'
# for App Password enable 2-step verification then u can create app password
            smtp_password = 'wmqq hifm bydv bxid'

# Email content
            subject = 'Password recovery'
            body = 'This is a Password recovery email sent from Eventia.' + \
                'Your password as per registration is: ' + pwd[2:len(pwd)-3]
            sender_email = 'chanakya2105@gmail.com'
            receiver_email = email

# Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email,
                                message.as_string())

            return render(request, 'password_recovery.html', {'status': 'Password sent to given mail ID'})
        else:
            return render(request, 'password_recovery.html', {'status': 'Wrong Username!'})
    else:
        return render(request, 'password_recovery.html')


def logout(request):
    del request.session['username']
    request.session.modified = True
    return render(request, 'login.html')


def a_logout(request):
    del request.session['username']
    request.session.modified = True
    return render(request, 'admin/a_login.html')


def em_logout(request):
    del request.session['username']
    request.session.modified = True
    return render(request, 'eventmanager/em_login.html')


def contact(request):
    if "username" in request.session:
        if request.method == "POST":
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
            )
            mycursor = conn.cursor()
            # retrive post details
            email = request.POST['email']
            mobile = request.POST['mobile']
            city = request.POST['city']
            subject = request.POST['subject']
            message = request.POST['message']

            mycursor.execute("insert into messages(email,mobile,city,subject,message) values('" +
                         email+"','"+mobile+"','"+city+"','"+subject+"','"+message+"')")
            conn.commit()
            return redirect('index1')
        else:
            return render(request, 'contact.html')
    else:
        return render(request, 'login.html')
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Dashboard for event manager Webpage Views(USER)
# --------------------------------------------------------------------------------


def events_reg(request):
    
    if "username" in request.session:
        uname = request.session.get("username")
        if request.method == 'POST':

            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='eventshowcase'
            )
            query1 = conn.cursor()
            e_name = request.POST['event_name']
            e_org = request.POST['event_organizer']
            e_type = request.POST['event_type']
            venue = request.POST['venue']
            age_res = request.POST['age_restriction']
            date = request.POST['date']
            time = request.POST['time']
            capacity = request.POST['capacity']
            cost = request.POST['cost']
            description = request.POST['description']
            org_email = request.session.get('username')
            new_format = datetime.strptime(
                date, "%Y-%m-%d").strftime('%Y-%m-%d')
            query1.execute("insert into event(event_name,event_organizer,event_type,venue,age_restriction,description,date,time,capacity,cost,org_email) values('" +
                           e_name+"','"+e_org+"','"+e_type+"','"+venue+"','"+age_res+"','"+description+"','"+new_format+"','"+time+"','"+capacity+"','"+cost+"','"+org_email+"')")
            conn.commit()
            return redirect(events_reg)
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="eventshowcase"
            )
            mycursor = conn.cursor()
            mycursor.execute("select * from event_type")
            result = mycursor.fetchall()
            types = []
            for x in result:
                obj = event_type()
                obj.type_id = x[0]
                obj.type = x[1]
                types.append(obj)
            return render(request, 'eventmanager/eventsreg.html', {'event_type': types, 'username': uname})
    else:
        return render(request, 'eventmanager/em_login.html')


def a_login(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        mycursor = conn.cursor()
        # retrive post details

        uname = request.POST['username']
        pwd = request.POST['password']

        mycursor.execute("select * from admin where username='" +
                         uname+"' and password='"+pwd+"'")
        result = mycursor.fetchone()
        if (result != None):
            request.session['username'] = uname
            return render(request, 'admin/index.html', {"username": uname})
            # redirect('studenthome')
        else:
            return render(request, 'admin/a_login.html', {'status': 'Wrong Username or Password!'})
    else:
        return render(request, 'admin/a_login.html')
# --------------------------------------------------------------------------------


def em_login(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        mycursor = conn.cursor()
        # retrive post details

        uname = request.POST['email']
        pwd = request.POST['password']

        mycursor.execute("select * from user where email='" +
                         uname+"' and password='"+pwd+"' and usertype='eventmanager' and isActive=1")
        result = mycursor.fetchone()
        if (result != None):
            request.session['username'] = uname
            return render(request, 'eventmanager/index.html', {"username": uname})
            # redirect('studenthome')
        else:
            return render(request, 'eventmanager/em_login.html', {'status': 'Wrong Username or Password!'})
    else:
        return render(request, 'eventmanager/em_login.html')


# --------------------------------------------------------------------------------


def index1(request):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="eventshowcase"
        )
        cursor = conn.cursor(dictionary=True)  # Create cursor here

        uname = request.session.get("username")

        cursor.execute("SELECT usertype FROM user WHERE email = %s", (uname,))
        user_data = cursor.fetchone()
        
        # Close database connection
        cursor.close()
        conn.close()
        if user_data:
            user_type = user_data['usertype']  # Assuming 'user_type' is the column name
            return render(request, 'index1.html', {
                "username": uname,
                "user_type": user_type
            })
        else:
            # Handle case where user data wasn't found
            return render(request, 'index1.html', {
                "username": uname,
                "user_type": "attendee"  # Default to attendee
            })
        return render(request, 'index1.html', {"username": uname})
    else:
        return render(request, 'index.html')


# --------------------------------------------------------------------------------
def viewevents(request):
    if "username" in request.session:
        # uname = request.session['username']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from event")
        result = mycursor.fetchall()
        e = []
        for row in result:
            obj = events()
            obj.e_id = row[0]
            obj.event_name = row[1]
            obj.event_organizer = row[2]
            obj.event_type = row[3]
            obj.venue = row[4]
            obj.age_restriction = row[5]
            obj.description = row[6]
            obj.date = row[7]
            obj.time = row[8]
            obj.capacity = row[9]
            obj.cost = row[10]
            obj.org_email = row[11]
            e.append(obj)
        # print(e)

        return render(request, 'admin/index.html', {'events': e, 'username': uname})
    else:
        return render(request, 'admin/a_login.html')


def viewem(request):
    if "username" in request.session:

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from user")
        result = mycursor.fetchall()
        em = []
        for row in result:
            obj = users()
            obj.usertype = row[4]
            if obj.usertype == "eventmanager":

                obj.email = row[0]

                obj.nationality = row[2]
                obj.gender = row[3]

                obj.dob = row[5]
                obj.State_ID = row[6]
                obj.age = row[7]
                obj.isActive = row[8]

                em.append(obj)
            else:
                continue
        # print(e)

        return render(request, 'admin/emdisp.html', {'eventmanagers': em, 'username': uname})
    else:
        return render(request, 'admin/a_login.html')


def viewmessages(request):
    if "username" in request.session:
        # uname = request.session['username']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from messages")
        result = mycursor.fetchall()
        msg = []
        for row in result:
            obj = messages()
            obj.sl_no = row[0]
            obj.email = row[1]
            obj.mobile = row[2]
            obj.city = row[3]
            obj.subject = row[4]
            obj.message = row[5]
            msg.append(obj)

        return render(request, 'admin/messages.html', {'messages': msg, 'username': uname})
    else:
        return render(request, 'admin/a_login.html')


def viewusers(request):
    if "username" in request.session:
        # uname = request.session['username']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from user")
        result = mycursor.fetchall()
        em = []
        for row in result:
            obj = users()
            obj.usertype = row[4]
            if obj.usertype == "attendee":

                obj.email = row[0]

                obj.nationality = row[2]
                obj.gender = row[3]

                obj.dob = row[5]
                obj.State_ID = row[6]
                obj.age = row[8]
                obj.isActive = row[8]

                em.append(obj)
            else:
                continue
        # print(e)

        return render(request, 'admin/users.html', {'attendees': em, 'username': uname})
    else:
        return render(request, 'admin/a_login.html')


def viewpayments(request):
    if "username" in request.session:
        # uname = request.session['username']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from payments")
        result = mycursor.fetchall()
        pay = []
        for row in result:
            obj = payments()
            obj.pay_id = row[0]
            obj.e_id = row[1]
            obj.email = row[2]
            obj.amount = row[3]
            obj.date_time = row[4]
            pay.append(obj)

        return render(request, 'admin/payments.html', {'payments': pay, 'username': uname})
    else:
        return render(request, 'admin/a_login.html')


def viewmyusers(request):
    return render(request, 'eventmanager/regusers.html')


def em_viewevents(request):
    if "username" in request.session:
        # uname = request.session['username']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        uname = request.session.get('username')
        mycursor = conn.cursor()
        mycursor.execute("select * from event where org_email='"+uname+"'")
        result = mycursor.fetchall()
        e = []
        if result != None:
            for row in result:
                obj = events()
                obj.e_id = row[0]
                obj.event_name = row[1]
                obj.event_organizer = row[2]
                obj.event_type = row[3]
                obj.venue = row[4]
                obj.age_restriction = row[5]
                obj.description = row[6]
                obj.date = row[7]
                obj.time = row[8]
                obj.capacity = row[9]
                obj.cost = row[10]
                obj.org_email = row[11]
                e.append(obj)
        else:
            return render(request, 'eventmanager/index.html', {'status': 'No records of your events are present'})

        return render(request, 'eventmanager/index.html', {'events': e, 'username': uname})
    else:
        return render(request, 'eventmanager/em_login.html')


def viewmypayments(request):
    return render(request, 'eventmanager/payments.html')


def a_deleteevent(request, e_id):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        query = conn.cursor()
        query.execute("DELETE FROM event where e_id='"+e_id+"'")
        conn.commit()
        return redirect(viewevents)
    else:
        return render(request, 'admin/a_login.html')


def admituser(request, email):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        query = conn.cursor()
        query.execute("update user set IsActive =1 where email='"+email+"'")
        conn.commit()
        return redirect(viewem)
    else:
        return render(request, 'admin/a_login.html')


def a_deleteuser(request, email):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        query = conn.cursor()
        query.execute("DELETE FROM user where email='"+email+"'")
        conn.commit()
        return redirect(viewusers)
    else:
        return render(request, 'admin/a_login.html')


def a_deleteem(request, email):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        query = conn.cursor()
        query.execute("DELETE FROM user where email='"+email+"'")
        conn.commit()
        return redirect(viewem)
    else:
        return render(request, 'admin/a_login.html')


def a_deletemsg(request, sl_no):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        query = conn.cursor()
        query.execute("DELETE FROM messages where sl_no='"+sl_no+"'")
        conn.commit()
        return redirect(viewmessages)
    else:
        return render(request, 'admin/a_login.html')


def em_deleteevent(request, e_id):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        query = conn.cursor()
        query.execute("DELETE FROM event where e_id='"+e_id+"'")
        conn.commit()
        return redirect(em_viewevents)
    else:
        return render(request, 'eventmanager/em_login.html')


def em_editevent(request, e_id):
    if "username" in request.session:
        uname = request.session.get("username")
        if request.method == "POST":
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='eventshowcase'
            )
            query1 = conn.cursor()
            e_name = request.POST['event_name']
            e_org = request.POST['event_organizer']
            e_type = request.POST['event_type']
            venue = request.POST['venue']
            age_res = request.POST['age_restriction']
            date = request.POST['date']
            time = request.POST['time']
            capacity = request.POST['capacity']
            cost = request.POST['cost']
            description = request.POST['description']
            org_email = uname
            new_format = datetime.strptime(
                date, "%Y-%m-%d").strftime('%Y-%m-%d')
            query1.execute("UPDATE event set event_name='"+e_name+"',event_organizer='"+e_org+"',event_type='"+e_type+"',venue='"+venue+"',age_restriction='"+age_res +
                           "',date='"+new_format+"',time='"+time+"',capacity='"+capacity+"',cost='"+cost+"',description='"+description+"',org_email='"+uname+"' where e_id='"+e_id+"'")
            conn.commit()
            return redirect(em_viewevents)
        else:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='eventshowcase'
            )
            query = conn.cursor()
            query.execute("select * from event where e_id='"+e_id+"'")
            result = query.fetchall()
            ev = []
            for row in result:
                s = events()
                s.e_id = row[0]
                s.event_name = row[1]
                s.event_organizer = row[2]
                s.event_type = row[3]
                s.venue = row[4]
                s.age_restriction = row[5]
                s.description = row[6]
                s.date = row[7]
                s.time = row[8]
                s.capacity = row[9]
                s.cost = row[10]
                ev.append(s)
            mycursor = conn.cursor()
            mycursor.execute("select * from event_type")
            result = mycursor.fetchall()
            types = []
            for x in result:
                obj = event_type()
                obj.type_id = x[0]
                obj.type = x[1]
                types.append(obj)
            return render(request, 'eventmanager/editevent.html', {'event_type': types, "username": uname, "events": ev})
    else:
        return render(request, 'eventmanager/em_login.html')


def updateprofile(request):
    if "username" in request.session:
        uname = request.session.get("username")
        if request.method == "POST":
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='eventshowcase'
            )
            query1 = conn.cursor()
            email = request.POST['email']
            nationality = request.POST['nationality']
            gender = request.POST['gender']
            dob = request.POST['dateofbirth']
            new_format = datetime.strptime(
                dob, "%Y-%m-%d").strftime('%Y-%m-%d')
            State_ID = request.POST['State_ID']

            query1.execute("UPDATE user set nationality='"+nationality+"',gender='" +
                           gender+"',dob='"+new_format+"',State_ID='"+State_ID+"' where email='"+email+"'")
            conn.commit()
            return redirect(profile)
        else:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='eventshowcase'
            )
            query = conn.cursor()
            query.execute("select * from user where email='"+uname+"'")
            result = query.fetchall()
            p = []
            for row in result:
                obj = users()
                obj.email = row[0]
                obj.password = row[1]
                obj.nationality = row[2]
                obj.gender = row[3]
                obj.usertype = row[4]
                obj.dob = row[5]
                obj.State_ID = row[6]
                obj.age = row[7]
                obj.isActive = row[8]

                p.append(obj)

            return render(request, 'updateprofile.html', {"username": uname, "pro": p})
    else:
        return render(request, 'login.html')


def deleteprofile(request):
    if "username" in request.session:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eventshowcase'
        )
        email=request.session.get('username')
        query = conn.cursor()
        query.execute("DELETE FROM user where email='"+email+"'")
        conn.commit()
        return redirect(index)
    else:
        return render(request, 'login.html')
    

