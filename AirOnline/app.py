# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
from dateutil import relativedelta
import random

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='123456',
                       db='Test_Air_Ticket',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def public():
    loggedin = None
    usertype = None
    if session != {}:
        loggedin = True
        usertype = session['usertype']
    return render_template('index.html', loggedin=loggedin, usertype=usertype)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_staff')
def register_staff():
    return render_template('register-staff.html')


@app.route('/register_customer')
def register_customer():
    return render_template('register-customer.html')


@app.route('/login')
def login():
    return render_template('login.html')


# login page, choose staff or customer
@app.route('/login_staff')
def login_staff():
    return render_template('login-staff.html')


@app.route('/login_customer')
def login_customer():
    return render_template('login-customer.html')


# ==========================================================#

# ----------------Authenticates the register----------------#
@app.route("/registerAuth", methods=['GET', 'POST'])
def registerAuth():
    usertype = request.form['usertype']
    if usertype == 'Staff':
        return redirect(url_for('register_staff'))
    elif usertype == 'Customer':
        return redirect(url_for('register_customer'))


@app.route("/registerStaffAuth", methods=['GET', 'POST'])
def registerStaffAuth():
    # grabs information from the forms
    username = request.form['username']
    airline_name = request.form['airline-name']
    password = request.form['password']
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    DOB = request.form['DOB']
    phone_number = request.form.getlist('phone-number')

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airline_staff WHERE user_name = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register-staff.html', error=error)
    else:
        query = '''select airline_name
                    from airline
                    where airline_name = %s'''
        cursor.execute(query, (airline_name))
        data1 = cursor.fetchone()
        if (data1):
            ins = 'INSERT INTO airline_staff VALUES(%s, %s, md5(%s), %s, %s, %s)'
            cursor.execute(ins, (username, airline_name, password,
                                 first_name, last_name, DOB))
            conn.commit()

            for phone in phone_number:
                if phone != "":
                    ins = 'INSERT INTO staff_phone VALUES(%s, %s)'
                    cursor.execute(ins, (username, phone))
                    conn.commit()
            cursor.close()
            return render_template('login-staff.html')
        else:
            error = "This airline dose not exist"
            return render_template('register-staff.html', error=error)


@app.route("/registerCustomerAuth", methods=['GET', 'POST'])
def registerCustomerAuth():
    # grabs information from the forms
    email = request.form['username']
    password = request.form['password']
    name = request.form['name']
    DOB = request.form['DOB']
    phone_number = request.form['phone-number']
    building_number = request.form['building-number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    passport_number = request.form['passport-number']
    passport_expiration = request.form['passport-expiration']
    passport_country = request.form['passport-country']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES' \
              '(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, name, password,
                             building_number, street, city, state,
                             phone_number, passport_number, passport_expiration,
                             passport_country, DOB))
        conn.commit()
        cursor.close()
        return render_template('login-customer.html')


# -----------------Authenticates the login------------------#
@app.route("/loginAuth", methods=['GET', 'POST'])
def loginAuth():
    usertype = request.form['usertype']
    if usertype == 'Staff':
        return redirect(url_for('login_staff'))
    elif usertype == 'Customer':
        return redirect(url_for('login_customer'))


@app.route("/loginStaffAuth", methods=['GET', 'POST'])
def loginStaffAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airline_staff WHERE user_name = %s and password = md5(%s)'
    # query = 'SELECT * FROM airline_staff WHERE user_name = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        session['usertype'] = "staff"
        session['airline'] = data['airline_name']
        return redirect(url_for('staff_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login-staff.html', error=error)  # send the error msg to html
    # communicate between python and html


@app.route('/loginCustomerAuth', methods=['GET', 'POST'])
def loginCustomerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        # creates a session for the the user
        # session is a built in dictionary
        session['username'] = username
        session['usertype'] = "customer"
        return redirect(url_for('customer_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login-customer.html', error=error)  # send the error msg to html


# ============== public_index =====================#

# public search
@app.route('/searchPublic', methods=['GET', 'POST'])
def searchPublic():
    # get search info from page and execute in sql db
    source = request.form['source']
    destination = request.form['destination']
    triptype = request.form['triptype']
    departure_date = request.form['departure-date']

    if triptype == "one-way":
        cursor = conn.cursor()
        query = '''select * from flight_price natural join flight_seats_sold
                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                and amount_of_seats > tickets_sold'''
        cursor.execute(query, (source, destination, departure_date))
        data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        cursor.close()
        return render_template('search-one.html', source=source, destination=destination, departure_date=departure_date,
                               flights=data1)

    elif triptype == "round":
        return_date = request.form['return-date']
        cursor = conn.cursor()
        # depart
        query1 = '''select * from flight_price natural join flight_seats_sold
                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                and amount_of_seats > tickets_sold'''
        cursor.execute(query1, (source, destination, departure_date))
        data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        cursor.close()
        # return
        cursor = conn.cursor()
        query2 = '''select * from flight_price natural join flight_seats_sold
                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                and amount_of_seats > tickets_sold'''
        cursor.execute(query2, (destination, source, return_date))
        data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport=%s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        cursor.close()
        return render_template('search-round.html', source=source, destination=destination,
                               departure_date=departure_date,
                               return_date=return_date, departure_flights=data1, return_flights=data2)


@app.route("/searchPublicOneWay", methods=['GET', 'POST'])
def searchPublicOneWay():
    source = request.form['source']
    destination = request.form['destination']
    triptype = request.form['triptype']
    departure_date = request.form['departure-date']

    if triptype == "one-way":
        cursor = conn.cursor()
        query = '''select * from flight_price natural join flight_seats_sold
                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                and amount_of_seats > tickets_sold'''
        cursor.execute(query, (source, destination, departure_date))
        data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        cursor.close()
        return render_template('search-one.html', source=source, destination=destination, departure_date=departure_date,
                               flights=data1)

    elif triptype == "round":
        return_date = request.form['return-date']
        cursor = conn.cursor()
        # depart
        query = 'select * from flight_price ' \
                'where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now() ' \
                'and departure_airport = %s and arrival_airport = %s and departure_date = %s'
        cursor.execute(query, (source, destination, departure_date))
        data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                    natural join flight join airport as A join airport as B
                    where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        # return
        query = 'select * from flight_price ' \
                'where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now() ' \
                'and departure_airport = %s and arrival_airport = %s and departure_date = %s'
        cursor.execute(query, (destination, source, return_date))
        data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport=%s and B.city = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and A.city = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold
                    and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        cursor.close()

        return render_template('search-round.html', source=source, destination=destination,
                               departure_date=departure_date, return_date=return_date, departure_flights=data1,
                               return_flights=data2)


@app.route("/searchPublicRound", methods=['GET', 'POST'])
def searchPublicRound():
    source = request.form['source']
    destination = request.form['destination']
    triptype = request.form['triptype']
    departure_date = request.form['departure-date']

    if triptype == "one-way":
        cursor = conn.cursor()
        query = '''select * from flight_price natural join flight_seats_sold
                    where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold'''
        cursor.execute(query, (source, destination, departure_date))
        data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and A.city = %s and B.city = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and departure_airport = %s and B.city = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and A.city = %s and arrival_airport = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        cursor.close()
        return render_template('search-one.html', source=source, destination=destination, departure_date=departure_date,
                               flights=data1)

    elif triptype == "round":
        return_date = request.form['return-date']
        cursor = conn.cursor()
        # depart
        query = '''select * from flight_price natural join flight_seats_sold
                    where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold'''
        cursor.execute(query, (source, destination, departure_date))
        data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and A.city = %s and B.city = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and departure_airport = %s and B.city = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        if (not data1):
            query = '''select * from flight_price natural join flight_seats_sold
                        natural join flight join airport as A join airport as B
                        where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and A.city = %s and arrival_airport = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query, (source, destination, departure_date))
            data1 = cursor.fetchall()
        cursor.close()
        # return
        cursor = conn.cursor()
        query = '''select * from flight_price natural join flight_seats_sold
                    where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                    and departure_airport = %s and arrival_airport = %s and departure_date = %s
                    and amount_of_seats > tickets_sold'''
        cursor.execute(query, (destination, source, return_date))
        data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and A.city = %s and B.city = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and departure_airport=%s and B.city = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        if (not data2):
            query2 = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                        and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and A.city = %s and arrival_airport = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
            cursor.execute(query2, (destination, source, return_date))
            data2 = cursor.fetchall()
        cursor.close()
        return render_template('search-round.html', source=source, destination=destination,
                               departure_date=departure_date, return_date=return_date, departure_flights=data1,
                               return_flights=data2)


# ------------- public check ------------------
@app.route("/checkIndex", methods=['GET', 'POST'])
def checkIndex():
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    datetype = request.form['datetype']
    date = request.form['date']

    if datetype == "departure_date":
        cursor = conn.cursor()
        query = 'select airline_name, flight_number, departure_date, departure_time, ' \
                'arrival_date, arrival_time, departure_airport, arrival_airport, status ' \
                'from flight ' \
                'where airline_name = %s and flight_number = %s and departure_date = %s' \
                'order by departure_time asc'
        cursor.execute(query, (airline_name, flight_number, date))
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('check.html', statuses=data1, airline_name=airline_name, flight_number=flight_number,
                               date=date, datetype=datetype)

    elif datetype == "arrival_date":
        cursor = conn.cursor()
        query = 'select airline_name, flight_number, departure_date, departure_time, ' \
                'arrival_date, arrival_time, departure_airport, arrival_airport, status ' \
                'from flight ' \
                'where airline_name = %s and flight_number = %s and arrival_date = %s' \
                'order by arrival_time asc'
        cursor.execute(query, (airline_name, flight_number, date))
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('check.html', statuses=data1, airline_name=airline_name, flight_number=flight_number,
                               date=date, datetype=datetype)


@app.route("/checkPublic", methods=['GET', 'POST'])
def checkPublic():
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    datetype = request.form['datetype']
    date = request.form['date']

    if datetype == "departure_date":
        cursor = conn.cursor()
        query = 'select airline_name, flight_number, departure_date, departure_time, ' \
                'arrival_date, arrival_time, departure_airport, arrival_airport, status ' \
                'from flight where airline_name = %s and flight_number = %s and departure_date = %s' \
                'order by departure_time asc'
        cursor.execute(query, (airline_name, flight_number, date))
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('check.html', statuses=data1, airline_name=airline_name, flight_number=flight_number,
                               date=date, datetype=datetype)

    elif datetype == "arrival_date":
        cursor = conn.cursor()
        query = 'select airline_name, flight_number, departure_date, departure_time, ' \
                'arrival_date, arrival_time, departure_airport, arrival_airport, status ' \
                'from flight where airline_name = %s and flight_number = %s and arrival_date = %s' \
                'order by arrival_time asc'
        cursor.execute(query, (airline_name, flight_number, date))
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('check.html', statuses=data1, airline_name=airline_name, flight_number=flight_number,
                               date=date, datetype=datetype)


# ==============================================================================
# ==============================================================================
# ================ Customer Use Cases ===================

# -------------------------------customer home----------------------------------
@app.route('/customer_home', methods=['GET', 'POST'])
def customer_home():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            username = session['username']
            today = datetime.date.today()
            to_date = today
            from_date = datetime.date(today.year - 1, today.month, today.day)
            session['flight_info1'] = {}
            session['flight_info2'] = {}

            cursor = conn.cursor()
            query = '''select name from customer where email = %s'''
            cursor.execute(query, (username))
            name = cursor.fetchone()
            cursor.close()
            name = name['name']

            # view
            cursor = conn.cursor()
            query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
            from (flight natural join ticket) join purchase using (ticket_id)
            where email = %s and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
            cursor.execute(query, (username, today))
            data1 = cursor.fetchall()
            cursor.close()
            # rate
            cursor = conn.cursor()
            query = 'select airline_name, flight_number, departure_date, departure_time, departure_airport, arrival_airport ' \
                    'from (flight natural join ticket) join purchase using (ticket_id)' \
                    'where timestamp(cast(arrival_date as datetime)+cast(arrival_time as time)) < now() ' \
                    'and email = %s and ' \
                    'ticket_id not in ' \
                    '(select ticket_id ' \
                    'from (flight natural join ticket) join purchase using (ticket_id) join rates using (email, airline_name, flight_number, departure_date, departure_time))'
            cursor.execute(query, (username))
            data2 = cursor.fetchall()
            cursor.close()

            # Track-total
            cursor = conn.cursor()
            query = '''select sum(sold_price) from purchase where email = %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
            cursor.execute(query, (username, from_date, to_date))
            total_spending = cursor.fetchall()
            if total_spending[0]['sum(sold_price)'] == None:
                total_spending[0]['sum(sold_price)'] = 0
            cursor.close()
            # Track-monthly
            cursor = conn.cursor()
            monthly_spending = []
            months = []
            date1 = datetime.datetime.strptime(str(from_date), '%Y-%m-%d')
            date2 = datetime.datetime.strptime(str(to_date), '%Y-%m-%d')
            # r = relativedelta.relativedelta(date2, date1)
            # month_number = r.months + r.years*12
            month_number = (date2.year - date1.year) * 12 + date2.month - date1.month
            if from_date.day != 1:
                month_number += 1
            for i in range(month_number):
                query = '''select sum(sold_price) from purchase where email = %s
                and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
                and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
                if from_date.month + i <= 12:
                    from_d_year = from_date.year
                    from_d_month = from_date.month + i
                else:
                    from_d_year = from_date.year + 1
                    from_d_month = from_date.month + i - 12
                if from_date.month + i + 1 <= 12:
                    to_d_year = from_date.year
                    to_d_month = from_date.month + i + 1
                else:
                    to_d_year = from_date.year + 1
                    to_d_month = from_date.month + i - 11
                if i == 0:
                    from_d_day = from_date.day
                else:
                    from_d_day = 1
                if i == month_number - 1:
                    to_d_month = to_date.month
                    to_d_day = to_date.day
                else:
                    to_d_day = 1
                from_d = datetime.date(from_d_year, from_d_month, from_d_day)
                to_d = datetime.date(to_d_year, to_d_month, to_d_day)
                cursor.execute(query, (username, from_d, to_d))
                monthly = cursor.fetchall()
                if monthly[0]['sum(sold_price)'] == None:
                    monthly[0]['sum(sold_price)'] = 0
                months.append(str(from_d_year) + "-" + str(from_d_month))
                monthly_spending.append(monthly)
            cursor.close()

            return render_template('customer-home.html', flights=data1, unrated=data2,
                                   total=total_spending[0]['sum(sold_price)'],
                                   monthly_spending=monthly_spending, from_date=to_date, from_date_track=from_date,
                                   to_date_track=to_date,
                                   display_number=6, months=months, name=name)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ---------!customer! search flights-------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            # display the search result
            usertype = session['usertype']
            source = request.form['source']
            destination = request.form['destination']
            triptype = request.form['triptype']
            depart_date = request.form['depart-date']
            session['searchCustomer'] = {'source': source, 'destination': destination, 'triptype': triptype,
                                         'depart_date': depart_date, 'return_date': None}
            session['flight_info1'] = {}
            session['flight_info2'] = {}

            if triptype == "one-way":
                cursor = conn.cursor()
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                        where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and departure_airport = %s and arrival_airport = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                cursor.close()
                # return render_template('search-customer-one.html', source=source, flights=data1)
                return render_template('search-customer-one.html', source=source, destination=destination,
                                       depart_date=depart_date, flights=data1)

            elif triptype == "round":
                return_date = request.form['return-date']
                session['searchCustomer']['return_date'] = return_date
                cursor = conn.cursor()
                # depart
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                # return
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (destination, source, return_date))
                data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport=%s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-round.html', source=source, destination=destination,
                                       depart_date=depart_date, return_date=return_date, departure_flights=data1,
                                       return_flights=data2)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/searchCustomerOneWay', methods=['GET', 'POST'])
def searchCustomerOneWay():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            source = request.form['source']
            destination = request.form['destination']
            triptype = request.form['triptype']
            depart_date = request.form['depart-date']
            session['searchCustomer']['source'] = source
            session['searchCustomer']['destination'] = destination
            session['searchCustomer']['triptype'] = triptype
            session['searchCustomer']['depart_date'] = depart_date
            session['flight_info1'] = {}
            session['flight_info2'] = {}

            if triptype == "one-way":
                session['searchCustomer']['return_date'] = None
                cursor = conn.cursor()
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-one.html', source=source, destination=destination,
                                       depart_date=depart_date, flights=data1)

            elif triptype == "round":
                return_date = request.form['return-date']
                session['searchCustomer']['return_date'] = return_date
                cursor = conn.cursor()
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                        where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and departure_airport = %s and arrival_airport = %s and departure_date = %s
                        and amount_of_seats > tickets_sold
                        and status != "cancelled"'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                # return
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (destination, source, return_date))
                data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport=%s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-round.html', source=source, destination=destination,
                                       depart_date=depart_date, return_date=return_date, departure_flights=data1,
                                       return_flights=data2)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/searchCustomerRound", methods=['GET', 'POST'])
def searchCustomerRound():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            source = request.form['source']
            destination = request.form['destination']
            triptype = request.form['triptype']
            depart_date = request.form['depart-date']
            session['searchCustomer']['source'] = source
            session['searchCustomer']['destination'] = destination
            session['searchCustomer']['triptype'] = triptype
            session['searchCustomer']['depart_date'] = depart_date
            session['flight_info1'] = {}
            session['flight_info2'] = {}

            if triptype == "one-way":
                session['searchCustomer']['return_date'] = None
                cursor = conn.cursor()
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-one.html', source=source, destination=destination,
                                       depart_date=depart_date, flights=data1)

            elif triptype == "round":
                return_date = request.form['return-date']
                session['searchCustomer']['return_date'] = return_date
                cursor = conn.cursor()
                # depart
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                # return
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (destination, source, return_date))
                data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport=%s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-round.html', source=source, destination=destination,
                                       depart_date=depart_date, return_date=return_date, departure_flights=data1,
                                       return_flights=data2)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ---------!customer! purchase flights-------------
@app.route("/purchaseCustomerOneWay", methods=['POST'])
def purchaseCustomerOneWay():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            airline_name = request.form['airline-name']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']
            arrival_date = request.form['arrival-date']
            arrival_time = request.form['arrival-time']
            source = request.form['source']
            destination = request.form['destination']
            price = request.form['price']
            # get ticket info
            cursor = conn.cursor()
            query = '''select ticket_id
                        from ticket
                        where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s
                        and ticket_id not in (select ticket_id from purchase)'''
            cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
            ticket_id = cursor.fetchone()
            cursor.close()
            # store flight info in session
            flight_info1 = {"airline_name": airline_name, "flight_number": flight_number,
                            "departure_date": departure_date, "departure_time": departure_time,
                            "arrival_date": arrival_date, "arrival_time": arrival_time, "departure_airport": source,
                            "arrival_airport": destination, "price": price, "ticket_id": ticket_id["ticket_id"]}
            session['flight_info1'] = flight_info1
            return redirect(url_for('purchase_customer'))
            # return render_template("purchase-customer.html", flights=[flight_info1], total=flight_info1["price"])
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/purchaseCustomerRoundDeparture", methods=['GET', 'POST'])
def purchaseCustomerRoundDeparture():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            source = session['searchCustomer']['source']
            destination = session['searchCustomer']['destination']
            triptype = session['searchCustomer']['triptype']
            depart_date = session['searchCustomer']['depart_date']
            return_date = session['searchCustomer']['return_date']
            departure = True
            airline_name = request.form['airline-name']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']
            arrival_date = request.form['arrival-date']
            arrival_time = request.form['arrival-time']
            departure_airport = request.form['departure-airport']
            arrival_airport = request.form['arrival-airport']
            price = request.form['price']
            if session['flight_info2'] != {}:
                prev_flight = session['flight_info2']
                back = True
                cursor = conn.cursor()
                query = '''select ticket_id
                        from ticket
                        where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s
                        and ticket_id not in (select ticket_id from purchase)'''
                cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
                ticket_id = cursor.fetchone()
                cursor.close()
                # store flight info in session
                flight_info1 = {"airline_name": airline_name, "flight_number": flight_number,
                                "departure_date": departure_date, "departure_time": departure_time,
                                "arrival_date": arrival_date, "arrival_time": arrival_time,
                                "departure_airport": departure_airport, "arrival_airport": arrival_airport,
                                "price": price, "ticket_id": ticket_id["ticket_id"]}
                session['flight_info1'] = flight_info1
                return render_template('search-customer-round.html', departure=departure, back=back, source=source,
                                       destination=destination, triptype=triptype, depart_date=depart_date,
                                       return_date=return_date, airline_name_d=airline_name,
                                       flight_number_d=flight_number, departure_date_d=departure_date,
                                       departure_time_d=departure_time, arrival_date_d=arrival_date,
                                       arrival_time_d=arrival_time, departure_airport_d=departure_airport,
                                       arrival_airport_d=arrival_airport, price_d=price,
                                       airline_name_r=prev_flight['airline_name'],
                                       flight_number_r=prev_flight['flight_number'],
                                       departure_date_r=prev_flight['departure_date'],
                                       departure_time_r=prev_flight['departure_time'],
                                       arrival_date_r=prev_flight['arrival_date'],
                                       arrival_time_r=prev_flight['arrival_time'],
                                       departure_airport_r=prev_flight['departure_airport'],
                                       arrival_airport_r=prev_flight['arrival_airport'], price_r=prev_flight['price'])
            else:
                back = None
                cursor = conn.cursor()
                query = '''select ticket_id
                        from ticket
                        where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s
                        and ticket_id not in (select ticket_id from purchase)'''
                cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
                ticket_id = cursor.fetchone()
                cursor.close()
                # store flight info in session
                flight_info1 = {"airline_name": airline_name, "flight_number": flight_number,
                                "departure_date": departure_date,
                                "departure_time": departure_time, "arrival_date": arrival_date,
                                "arrival_time": arrival_time,
                                "departure_airport": departure_airport, "arrival_airport": arrival_airport,
                                "price": price,
                                "ticket_id": ticket_id["ticket_id"]}
                session['flight_info1'] = flight_info1

                # return flight query
                cursor = conn.cursor()
                query = '''select * from flight_price natural join flight_seats_sold natural join flight
                                where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                                and departure_airport = %s and arrival_airport = %s and departure_date = %s
                                and amount_of_seats > tickets_sold
                                and status != "cancelled"'''
                cursor.execute(query, (destination, source, return_date))
                data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport=%s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                if (not data2):
                    query2 = '''select * from flight_price natural join flight_seats_sold
                                natural join flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query2, (destination, source, return_date))
                    data2 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-round.html', departure=departure, back=back, source=source,
                                       destination=destination, triptype=triptype, depart_date=depart_date,
                                       return_date=return_date, airline_name_d=airline_name,
                                       flight_number_d=flight_number, departure_date_d=departure_date,
                                       departure_time_d=departure_time, arrival_date_d=arrival_date,
                                       arrival_time_d=arrival_time, departure_airport_d=departure_airport,
                                       arrival_airport_d=arrival_airport, price_d=price, return_flights=data2)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/purchaseCustomerRoundReturn", methods=['GET', 'POST'])
def purchaseCustomerRoundReturn():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            source = session['searchCustomer']['source']
            destination = session['searchCustomer']['destination']
            triptype = session['searchCustomer']['triptype']
            depart_date = session['searchCustomer']['depart_date']
            return_date = session['searchCustomer']['return_date']
            back = True
            airline_name = request.form['airline-name']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']
            arrival_date = request.form['arrival-date']
            arrival_time = request.form['arrival-time']
            departure_airport = request.form['departure-airport']
            arrival_airport = request.form['arrival-airport']
            price = request.form['price']
            if session['flight_info1'] != {}:
                prev_flight = session['flight_info1']
                departure = True
                cursor = conn.cursor()
                query = '''select ticket_id
                        from ticket
                        where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s
                        and ticket_id not in (select ticket_id from purchase)'''
                cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
                ticket_id = cursor.fetchone()
                cursor.close()
                # store flight info in session
                flight_info2 = {"airline_name": airline_name, "flight_number": flight_number,
                                "departure_date": departure_date, "departure_time": departure_time,
                                "arrival_date": arrival_date, "arrival_time": arrival_time,
                                "departure_airport": departure_airport, "arrival_airport": arrival_airport,
                                "price": price, "ticket_id": ticket_id["ticket_id"]}
                session['flight_info2'] = flight_info2
                return render_template('search-customer-round.html', departure=departure, back=back, source=source,
                                       destination=destination, triptype=triptype, depart_date=depart_date,
                                       return_date=return_date, airline_name_r=airline_name,
                                       flight_number_r=flight_number, departure_date_r=departure_date,
                                       departure_time_r=departure_time, arrival_date_r=arrival_date,
                                       arrival_time_r=arrival_time, departure_airport_r=departure_airport,
                                       arrival_airport_r=arrival_airport, price_r=price,
                                       airline_name_d=prev_flight['airline_name'],
                                       flight_number_d=prev_flight['flight_number'],
                                       departure_date_d=prev_flight['departure_date'],
                                       departure_time_d=prev_flight['departure_time'],
                                       arrival_date_d=prev_flight['arrival_date'],
                                       arrival_time_d=prev_flight['arrival_time'],
                                       departure_airport_d=prev_flight['departure_airport'],
                                       arrival_airport_d=prev_flight['arrival_airport'], price_d=prev_flight['price'])
            else:
                departure = None
                cursor = conn.cursor()
                query = '''select ticket_id
                        from ticket
                        where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s
                        and ticket_id not in (select ticket_id from purchase)'''
                cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
                ticket_id = cursor.fetchone()
                cursor.close()
                # store flight info in session
                flight_info2 = {"airline_name": airline_name, "flight_number": flight_number,
                                "departure_date": departure_date, "departure_time": departure_time,
                                "arrival_date": arrival_date, "arrival_time": arrival_time,
                                "departure_airport": departure_airport, "arrival_airport": arrival_airport,
                                "price": price, "ticket_id": ticket_id["ticket_id"]}
                session['flight_info2'] = flight_info2

                # departure flight query
                cursor = conn.cursor()
                query = '''select * from flight_price natural join flight_seats_sold
                        where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                        and departure_airport = %s and arrival_airport = %s and departure_date = %s
                        and amount_of_seats > tickets_sold'''
                cursor.execute(query, (source, destination, depart_date))
                data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and departure_airport = %s and B.city = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                if (not data1):
                    query = '''select * from flight_price natural join flight_seats_sold
                            natural join flight join airport as A join airport as B
                            where departure_airport = A.airport_name and arrival_airport = B.airport_name
                            and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
                            and A.city = %s and arrival_airport = %s and departure_date = %s
                            and amount_of_seats > tickets_sold
                            and status != "cancelled"'''
                    cursor.execute(query, (source, destination, depart_date))
                    data1 = cursor.fetchall()
                cursor.close()
                return render_template('search-customer-round.html', departure=departure, back=back, source=source,
                                       destination=destination, triptype=triptype, depart_date=depart_date,
                                       return_date=return_date, airline_name_r=airline_name,
                                       flight_number_r=flight_number, departure_date_r=departure_date,
                                       departure_time_r=departure_time, arrival_date_r=arrival_date,
                                       arrival_time_r=arrival_time, departure_airport_r=departure_airport,
                                       arrival_airport_r=arrival_airport, price_r=price, departure_flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/purchaseCustomerRound", methods=['GET', 'POST'])
def purchaseCustomerRound():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            return redirect(url_for('purchase_customer'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/purchase_customer", methods=['GET', 'POST'])
def purchase_customer():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            flight_info1 = session['flight_info1']
            flight_info2 = session['flight_info2']
            if flight_info2 == {}:
                flights = [flight_info1]
                total = float(flight_info1['price'])
            else:
                flights = [flight_info1, flight_info2]
                total = float(flight_info1['price']) + float(flight_info2['price'])
            return render_template("purchase-customer.html", flights=flights, total=total)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ------------!customer! make payment-------------
@app.route("/payCustomer", methods=['GET', 'POST'])
def payCustomer():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            username = session['username']
            flight_info1 = session['flight_info1']
            flight_info2 = session['flight_info2']
            card_type = request.form["cardtype"]
            card_number = request.form['card-number']
            name_on_card = request.form['name-on-card']
            card_expiration = request.form['card-expiration']
            cursor = conn.cursor()
            ins = '''insert into purchase
            (ticket_id, email, purchase_date, purchase_time, sold_price, card_type, card_number, name_on_card, expiraton_date)
            values (%s, %s, cast(now() as date), cast(now() as time), %s, %s, %s, %s, %s)
            '''

            cursor.execute(ins, (flight_info1["ticket_id"], username, flight_info1["price"],
                                 card_type, card_number, name_on_card, card_expiration))
            conn.commit()
            cursor.close()
            if flight_info2 != {}:
                cursor = conn.cursor()
                ins = '''insert into purchase
                (ticket_id, email, purchase_date, purchase_time, sold_price, card_type, card_number, name_on_card, expiraton_date)
                values (%s, %s, cast(now() as date), cast(now() as time), %s, %s, %s, %s, %s)
                '''
                cursor.execute(ins, (flight_info2["ticket_id"], username, flight_info2["price"],
                                     card_type, card_number, name_on_card, card_expiration))
                conn.commit()
                cursor.close()
            session.pop('flight_info1')
            session.pop('flight_info2')
            session.pop('searchCustomer')
            return render_template("purchase-customer-confirm.html")
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ------------!customer! rate my flights-------------
@app.route("/rate", methods=['GET', 'POST'])
def rate():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            airline = request.form['airline']
            number = request.form['number']
            date = request.form['date']
            time = request.form['time']
            source = request.form['source']
            destination = request.form['destination']
            return render_template('rate-customer.html', airline_name=airline, flight_number=number,
                                   departure_date=date, departure_time=time, source=source, destination=destination)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/rateCustomer", methods=['GET', 'POST'])
def rateCustomer():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            username = session['username']
            airline_name = request.form['airline-name']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']
            rate = request.form['rate']
            comment = request.form['comment']

            cursor = conn.cursor()
            ins = 'INSERT INTO rates VALUES' \
                  '(%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (username, airline_name, flight_number,
                                 departure_date, departure_time, rate, comment))
            conn.commit()
            cursor.close()
            return redirect(url_for('customer_home'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ------------!customer! view my flights-----------
@app.route('/view', methods=['GET', 'POST'])
def view():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            username = session['username']
            source = request.form['source']
            destination = request.form['destination']
            from_date = request.form['from-date']
            to_date = request.form['to-date']

            if from_date == "":
                from_date = datetime.date.today()
            if to_date == "":
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, from_date))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and arrival_airport = %s
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, destination, from_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where arrival_airport = airport_name and email = %s and city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, destination, from_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and departure_airport = %s
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, from_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where departure_airport = airport_name and email = %s and city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, from_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and departure_airport = %s and arrival_airport = %s
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, destination, from_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and B.city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and departure_airport = %s and B.city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and arrival_airport = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date))
                        data1 = cursor.fetchall()
                    cursor.close()
            else:
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, from_date, to_date))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and arrival_airport = %s
                            and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, destination, from_date, to_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where arrival_airport = airport_name and email = %s and city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and departure_airport = %s
                            and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, from_date, to_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where departure_airport = airport_name and email = %s and city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, from_date, to_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and departure_airport = %s and arrival_airport = %s
                            and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, destination, from_date, to_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and B.city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and departure_airport = %s and B.city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and arrival_airport = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    cursor.close()
            return render_template('view-customer.html', from_date=from_date, to_date=to_date,
                                   source=source, destination=destination, flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/viewCustomer", methods=['GET', 'POST'])
def viewCustomer():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            username = session['username']
            source = request.form['source']
            destination = request.form['destination']
            from_date = request.form['from-date']
            to_date = request.form['to-date']

            if from_date == "":
                from_date = datetime.date.today()
            if to_date == "":
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, from_date))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and arrival_airport = %s
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, destination, from_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where arrival_airport = airport_name and email = %s and city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, destination, from_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and departure_airport = %s
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, from_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where departure_airport = airport_name and email = %s and city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, from_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                    from (flight natural join ticket) join purchase using (ticket_id)
                    where email = %s and departure_airport = %s and arrival_airport = %s
                    and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, destination, from_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and B.city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and departure_airport = %s and B.city = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and arrival_airport = %s
                                and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date))
                        data1 = cursor.fetchall()
                    cursor.close()
            else:
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, from_date, to_date))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and arrival_airport = %s
                            and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, destination, from_date, to_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where arrival_airport = airport_name and email = %s and city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and departure_airport = %s
                            and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, from_date, to_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport
                                where departure_airport = airport_name and email = %s and city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, from_date, to_date))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select airline_name, flight_number, departure_date, departure_time,
                            arrival_date, arrival_time, departure_airport, arrival_airport, status
                            from (flight natural join ticket) join purchase using (ticket_id)
                            where email = %s and departure_airport = %s and arrival_airport = %s
                            and departure_date between %s and %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (username, source, destination, from_date, to_date))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and B.city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and departure_airport = %s and B.city = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, status
                                from (flight natural join ticket) join purchase using (ticket_id)
                                join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and email = %s and A.city = %s and arrival_airport = %s
                                and departure_date between %s and %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (username, source, destination, from_date, to_date))
                        data1 = cursor.fetchall()
                    cursor.close()
            return render_template('view-customer.html', from_date=from_date, to_date=to_date,
                                   source=source, destination=destination, flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ------------!customer! track my spending-----------
@app.route("/track", methods=['GET', 'POST'])
def track():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            # when the user specify from-date and to-date
            username = session['username']
            from_date_track = request.form['from-date']
            to_date_track = request.form['to-date']
            # Track-total
            cursor = conn.cursor()
            query = '''select sum(sold_price) from purchase where email = %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
            cursor.execute(query, (username, from_date_track, to_date_track))
            total_spending = cursor.fetchall()
            if total_spending[0]['sum(sold_price)'] == None:
                total_spending[0]['sum(sold_price)'] = 0
            cursor.close()
            # Track-monthly
            cursor = conn.cursor()
            monthly_spending = []
            months = []
            date1 = datetime.datetime.strptime(from_date_track, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(to_date_track, '%Y-%m-%d')
            # r = relativedelta.relativedelta(date2, date1)
            # month_number = r.months + r.years*12
            year_number = date2.year - date1.year + 1
            for i in range(year_number):
                if i == 0 and year_number > 1:
                    month_number = 13 - date1.month
                    init_month = date1.month
                elif i == year_number - 1 and year_number > 1:
                    if date2.day == 1:
                        month_number = date2.month - 1
                    else:
                        month_number = date2.month
                    init_month = 1
                elif year_number > 1:
                    month_number = 12
                    init_month = 1
                else:
                    if date2.day == 1:
                        month_number = date2.month - date1.month
                    else:
                        month_number = date2.month - date1.month + 1
                    init_month = date1.month
                for j in range(month_number):
                    query = '''select sum(sold_price) from purchase where email = %s
                    and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
                    and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
                    if init_month + j <= 12:
                        from_d_year = date1.year + i
                        from_d_month = init_month + j
                    else:
                        from_d_year = date1.year + 1 + i
                        from_d_month = init_month + j - 12
                    if init_month + j + 1 <= 12:
                        to_d_year = date1.year + i
                        to_d_month = init_month + j + 1
                    else:
                        to_d_year = date1.year + 1 + i
                        to_d_month = init_month + j - 11
                    if j == 0 and i == 0:
                        from_d_day = date1.day
                    else:
                        from_d_day = 1
                    if j == month_number - 1 and i == year_number - 1:
                        to_d_month = date2.month
                        to_d_day = date2.day
                    else:
                        to_d_day = 1
                    from_d = datetime.date(from_d_year, from_d_month, from_d_day)
                    to_d = datetime.date(to_d_year, to_d_month, to_d_day)
                    cursor.execute(query, (username, from_d, to_d))
                    monthly = cursor.fetchall()
                    if monthly[0]['sum(sold_price)'] == None:
                        monthly[0]['sum(sold_price)'] = 0
                    months.append(str(from_d_year) + "-" + str(from_d_month))
                    monthly_spending.append(monthly)
            month_number = (date2.year - date1.year) * 12 + date2.month - date1.month
            if date2.day != 1:
                month_number += 1
            cursor.close()
            return render_template('track-customer.html', total=total_spending[0]['sum(sold_price)'],
                                   monthly_spending=monthly_spending, from_date_track=from_date_track,
                                   to_date_track=to_date_track, month_numnber=month_number, display_number=month_number,
                                   months=months)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route("/trackCustomer", methods=['GET', 'POST'])
def trackCustomer():
    try:
        usertype = session['usertype']
        if usertype == "customer":
            # when the user specify from-date and to-date
            username = session['username']
            from_date_track = request.form['from-date']
            to_date_track = request.form['to-date']
            cursor = conn.cursor()
            query = '''select sum(sold_price) from purchase where email = %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
            cursor.execute(query, (username, from_date_track, to_date_track))
            total_spending = cursor.fetchall()
            if total_spending[0]['sum(sold_price)'] == None:
                total_spending[0]['sum(sold_price)'] = 0
            cursor.close()
            # Track-monthly
            cursor = conn.cursor()
            monthly_spending = []
            months = []
            date1 = datetime.datetime.strptime(from_date_track, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(to_date_track, '%Y-%m-%d')
            # r = relativedelta.relativedelta(date2, date1)
            # month_number = r.months + r.years*12
            year_number = date2.year - date1.year + 1
            for i in range(year_number):
                if i == 0 and year_number > 1:
                    month_number = 13 - date1.month
                    init_month = date1.month
                elif i == year_number - 1 and year_number > 1:
                    if date2.day == 1:
                        month_number = date2.month - 1
                    else:
                        month_number = date2.month
                    init_month = 1
                elif year_number > 1:
                    month_number = 12
                    init_month = 1
                else:
                    if date2.day == 1:
                        month_number = date2.month - date1.month
                    else:
                        month_number = date2.month - date1.month + 1
                    init_month = date1.month
                for j in range(month_number):
                    query = '''select sum(sold_price) from purchase where email = %s
                    and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
                    and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
                    if init_month + j <= 12:
                        from_d_year = date1.year + i
                        from_d_month = init_month + j
                    else:
                        from_d_year = date1.year + 1 + i
                        from_d_month = init_month + j - 12
                    if init_month + j + 1 <= 12:
                        to_d_year = date1.year + i
                        to_d_month = init_month + j + 1
                    else:
                        to_d_year = date1.year + 1 + i
                        to_d_month = init_month + j - 11
                    if j == 0 and i == 0:
                        from_d_day = date1.day
                    else:
                        from_d_day = 1
                    if j == month_number - 1 and i == year_number - 1:
                        to_d_month = date2.month
                        to_d_day = date2.day
                    else:
                        to_d_day = 1
                    from_d = datetime.date(from_d_year, from_d_month, from_d_day)
                    to_d = datetime.date(to_d_year, to_d_month, to_d_day)
                    cursor.execute(query, (username, from_d, to_d))
                    monthly = cursor.fetchall()
                    if monthly[0]['sum(sold_price)'] == None:
                        monthly[0]['sum(sold_price)'] = 0
                    months.append(str(from_d_year) + "-" + str(from_d_month))
                    monthly_spending.append(monthly)
            month_number = (date2.year - date1.year) * 12 + date2.month - date1.month
            if date2.day != 1:
                month_number += 1
            cursor.close()
            return render_template('track-customer.html', total=total_spending[0]['sum(sold_price)'],
                                   monthly_spending=monthly_spending, from_date_track=from_date_track,
                                   to_date_track=to_date_track, month_numnber=month_number, display_number=month_number,
                                   months=months)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ==============================================================================
# ==============================================================================
# ===============Airline Staff use case============
# -------------------------------staff home----------------------------------
@app.route('/staff_home', methods=['GET', 'POST'])
def staff_home():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            username = session['username']
            airline = session['airline']
            from_date = datetime.date.today()
            to_date = datetime.datetime.now() + datetime.timedelta(30)
            to_date = datetime.date(to_date.year, to_date.month, to_date.day)
            cursor = conn.cursor()
            query = '''select * from flight
            where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) between %s and %s
            and airline_name = %s
            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
            cursor.execute(query, (from_date, to_date, airline))
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('staff-home.html', username=username, flights=data1, from_date=from_date,
                                   to_date=to_date)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ------------------view flights -----------------
@app.route('/viewFlights', methods=['GET', 'POST'])
def viewFlights():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            source = request.form['source']
            destination = request.form['destination']
            from_date = request.form['from-date']
            to_date = request.form['to-date']

            if from_date == "":
                from_date = datetime.date.today()
            else:
                from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
                from_date = datetime.date(from_date.year, from_date.month, from_date.day)
            if to_date == "":
                to_date = from_date + datetime.timedelta(30)
                to_date = datetime.date(to_date.year, to_date.month, to_date.day)
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                    from flight
                    where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s and airline_name = %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                        from flight
                        where arrival_airport = %s
                        and departure_date between %s and %s
                        and airline_name = %s
                        order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where arrival_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                        from flight
                        where departure_airport = %s
                        and departure_date between %s and %s
                        and airline_name = %s
                        order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where departure_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                        from flight
                        where departure_airport = %s and arrival_airport = %s
                        and departure_date between %s and %s
                        and airline_name = %s
                        order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and departure_airport = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and arrival_airport = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
            else:
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where arrival_airport = %s
                            and departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where arrival_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where departure_airport = %s
                            and departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where departure_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where departure_airport = %s and arrival_airport = %s
                            and departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and departure_airport = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and arrival_airport = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
            return render_template('view-flights-staff.html', from_date=from_date, to_date=to_date,
                                   source=source, destination=destination, flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/viewFlightsStaff', methods=['GET', 'POST'])
def viewFlightsStaff():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            source = request.form['source']
            destination = request.form['destination']
            from_date = request.form['from-date']
            to_date = request.form['to-date']

            if from_date == "":
                from_date = datetime.date.today()
            else:
                from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
                from_date = datetime.date(from_date.year, from_date.month, from_date.day)
            if to_date == "":
                to_date = from_date + datetime.timedelta(30)
                to_date = datetime.date(to_date.year, to_date.month, to_date.day)
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                    from flight
                    where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= %s and airline_name = %s
                    order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                        from flight
                        where arrival_airport = %s
                        and departure_date between %s and %s
                        and airline_name = %s
                        order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where arrival_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                        from flight
                        where departure_airport = %s
                        and departure_date between %s and %s
                        and airline_name = %s
                        order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where departure_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                        from flight
                        where departure_airport = %s and arrival_airport = %s
                        and departure_date between %s and %s
                        and airline_name = %s
                        order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and departure_airport = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and arrival_airport = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
            else:
                if source == "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    cursor.close()
                elif source == "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where arrival_airport = %s
                            and departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where arrival_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination == "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where departure_airport = %s
                            and departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport
                                where departure_airport = airport_name
                                and city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
                elif source != "" and destination != "":
                    cursor = conn.cursor()
                    query = '''select *
                            from flight
                            where departure_airport = %s and arrival_airport = %s
                            and departure_date between %s and %s
                            and airline_name = %s
                            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                    cursor.execute(query, (source, destination, from_date, to_date, airline))
                    data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and departure_airport = %s and B.city = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    if (not data1):
                        query = '''select *
                                from flight join airport as A join airport as B
                                where departure_airport = A.airport_name and arrival_airport = B.airport_name
                                and A.city = %s and arrival_airport = %s
                                and departure_date between %s and %s
                                and airline_name = %s
                                order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
                        cursor.execute(query, (source, destination, from_date, to_date, airline))
                        data1 = cursor.fetchall()
                    cursor.close()
            return render_template('view-flights-staff.html', from_date=from_date, to_date=to_date,
                                   source=source, destination=destination, flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# -------------------View all customers----------------
@app.route('/viewFlightCustomers', methods=['GET', 'POST'])
def viewFlightCustomers():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']
            cursor = conn.cursor()
            query = '''select email, name
                    from flight natural join ticket natural join purchase natural join customer
                    where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s'''
            cursor.execute(query, (airline, flight_number, departure_date, departure_time))
            data1 = cursor.fetchall()
            cursor.close()

            return render_template('view-flight-customers.html', airline=airline, flight_number=flight_number,
                                   departure_date=departure_date, departure_time=departure_time, customers=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# --------------change flight status --------------
@app.route('/changeStatus', methods=['GET', 'POST'])
def changeStatus():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']

            cursor = conn.cursor()
            query = '''select * from flight
            where airline_name = %s and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
            cursor.execute(query, (airline))
            data = cursor.fetchall()
            cursor.close()

            return render_template('change-status-staff.html', flights=data)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/changeStatusStaff', methods=['GET', 'POST'])
def changeStatusStaff():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            status = request.form['status']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']

            cursor = conn.cursor()
            alter = '''update flight
                    set status = %s
                    where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s'''
            cursor.execute(alter, (status, airline, flight_number, departure_date, departure_time))
            data = cursor.fetchall()
            conn.commit()
            cursor.close()

            cursor = conn.cursor()
            query = '''select * from flight
            where airline_name = %s and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now()
            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
            cursor.execute(query, (airline))
            data = cursor.fetchall()
            cursor.close()

            return render_template('change-status-staff.html', flights=data)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# --------------create flights------------------
@app.route('/createFlight', methods=['GET', 'POST'])
def createFlight():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline_name = session['airline']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']
            arrival_date = request.form['arrival-date']
            arrival_time = request.form['arrival-time']
            departure_airport = request.form['departure-airport']
            arrival_airport = request.form['arrival-airport']
            base_price = request.form['base-price']
            status = request.form['status']
            airplane_id = request.form['airplane-id']

            cursor = conn.cursor()
            query = '''select * from flight
            where airline_name=%s and flight_number=%s and departure_date=%s and departure_time=%s'''
            cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
            data = cursor.fetchall()
            cursor.close()

            # check airport:
            cursor = conn.cursor()
            query = '''select * from airport
                        where airport_name = %s'''
            cursor.execute(query, (departure_airport))
            d_airport = cursor.fetchall()
            cursor.close()

            cursor = conn.cursor()
            query = '''select * from airport where airport_name = %s'''
            cursor.execute(query, (arrival_airport))
            a_airport = cursor.fetchall()
            cursor.close()

            # check airplane
            cursor = conn.cursor()
            query = '''select * from airplane where id = %s'''
            cursor.execute(query, (airplane_id))
            airplane = cursor.fetchall()
            cursor.close()

            # check date
            departure = departure_date + departure_time
            arrival = arrival_date + arrival_time
            if arrival <= departure:
                return render_template('create-flight-confirm.html', exist_flight="Incorrect date or time.")
            if not (d_airport):
                return render_template('create-flight-confirm.html', exist_flight="Departure airport does not exist.")
            if not (a_airport):
                return render_template('create-flight-confirm.html', exist_flight="Arrival airport does not exist.")
            if not (airplane):
                return render_template('create-flight-confirm.html', exist_flight="Airplane does not exist.")

            exist_flight = None
            if (data):
                return render_template('create-flight-confirm.html', exist_flight="This flight already exists.")
            else:

                cursor = conn.cursor()
                ins = 'INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(ins, (
                    airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time,
                    departure_airport,
                    arrival_airport, base_price, status, airplane_id))
                conn.commit()
                cursor.close()

            # -----create tickets for that flight------
            cursor = conn.cursor()
            query = '''select amount_of_seats
            from flight natural join airplane
            where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s'''
            cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
            seat_data = cursor.fetchone()
            cursor.close()

            # -----insert tickets for the flight----
            # generate ticket_id: airline_name abbr. + flight_number + fixed random number + serial order (last 3 digits)
            to_add1 = ''
            for i in airline_name:
                if i.isupper():
                    to_add1 += i
            random_num = random.randint(0, 9999999)
            to_add3 = str(random_num).zfill(7)
            amount_of_seats = seat_data['amount_of_seats']
            cursor = conn.cursor()
            for i in range(amount_of_seats):
                to_add2 = str(i).zfill(4)
                ticket_id = to_add1 + flight_number + to_add3 + to_add2
                query = '''
                insert into ticket (ticket_id, airline_name, flight_number, departure_date, departure_time)
                values (%s, %s, %s, %s, %s)
                '''
                cursor.execute(query, (ticket_id, airline_name, flight_number, departure_date, departure_time))
                conn.commit()
            cursor.close()
            return redirect(url_for('create_flight_confirm'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/create_flight_confirm', methods=['GET', 'POST'])
def create_flight_confirm():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            from_date = datetime.date.today()
            to_date = datetime.datetime.now() + datetime.timedelta(30)
            to_date = datetime.date(to_date.year, to_date.month, to_date.day)

            cursor = conn.cursor()
            query = '''select * from flight
            where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) between %s and %s
            and airline_name = %s
            order by timestamp(cast(departure_date as datetime)+cast(departure_time as time)) asc'''
            cursor.execute(query, (from_date, to_date, airline))
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('create-flight-confirm.html', flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# --------------add airplane------------------
@app.route('/createAirplane', methods=['GET', 'POST'])
def createAirplane():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            airplane_id = request.form['airplane-id']
            seating_capacity = request.form['seating-capacity']

            cursor = conn.cursor()
            query = '''select * from airplane
              where airline_name=%s and id=%s'''
            cursor.execute(query, (airline, airplane_id))
            data = cursor.fetchall()
            cursor.close()

            exist_airplane = None
            if (data):
                return render_template('create-airplane-confirm.html', exist_airplane="This airplane already exists.")
            else:
                cursor = conn.cursor()
                ins = 'INSERT INTO airplane VALUES (%s, %s, %s)'
                cursor.execute(ins, (airline, airplane_id, seating_capacity))
                conn.commit()
                cursor.close()
                return redirect(url_for('create_airplane_confirm'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/create_airplane_confirm', methods=['GET', 'POST'])
def create_airplane_confirm():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']

            cursor = conn.cursor()
            query = '''select id, amount_of_seats from airplane
            where airline_name = %s'''
            cursor.execute(query, (airline))
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('create-airplane-confirm.html', airplanes=data1, airline=airline)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# --------------add airport------------------
@app.route('/createAirport', methods=['GET', 'POST'])
def createAirport():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airport_name = request.form['airport-name']
            city = request.form['city']

            cursor = conn.cursor()
            query = '''select * from airport
              where airport_name=%s and city=%s'''
            cursor.execute(query, (airport_name, city))
            data = cursor.fetchall()
            cursor.close()

            exist_airport = None
            if (data):
                return render_template('create-airport-confirm.html', exist_airport="This airport already exists.")
            else:
                cursor = conn.cursor()
                ins = 'INSERT INTO airport VALUES (%s, %s)'
                cursor.execute(ins, (airport_name, city))
                conn.commit()
                cursor.close()
                return redirect(url_for('create_airport_confirm'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/create_airport_confirm', methods=['GET', 'POST'])
def create_airport_confirm():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            cursor = conn.cursor()
            query = '''select * from airport'''
            cursor.execute(query)
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('create-airport-confirm.html', airports=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# --------------view flight ratings--------------
@app.route('/view_ratings', methods=['GET', 'POST'])
def view_ratings():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            return redirect(url_for('viewRatings'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/viewRatings', methods=['GET', 'POST'])
def viewRatings():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            cursor = conn.cursor()
            query = '''select airline_name, flight_number, departure_date, departure_time, avg(rating) as average_rating
                        from rates
                        where airline_name = %s
                        group by airline_name, flight_number, departure_date, departure_time
                        Order by departure_date desc'''
            cursor.execute(query, (airline))
            data1 = cursor.fetchall()
            cursor.close()

            return render_template('view-ratings.html', flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/viewComments', methods=['GET', 'POST'])
def viewComments():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            flight_number = request.form['flight-number']
            departure_date = request.form['departure-date']
            departure_time = request.form['departure-time']

            cursor = conn.cursor()
            query = '''select email, rating, comments
                        from rates
                        where airline_name=%s and flight_number=%s and departure_date=%s and departure_time=%s'''
            cursor.execute(query, (airline, flight_number, departure_date, departure_time))
            data1 = cursor.fetchall()
            cursor.close()

            return render_template('view-ratings-comments.html', airline_name=airline, flight_number=flight_number,
                                   departure_date=departure_date, departure_time=departure_time, ratings=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# todo:view frequent customer
# 前端未完成
@app.route('/frequentCustomer', methods=['GET', 'POST'])
def frequentCustomer():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']

            cursor = conn.cursor()
            query = '''select distinct email, name, A.num_ticket
            from frequent_customer as A
            where airline_name = %s
            and A.num_ticket = (select max(B.num_ticket) from frequent_customer as B)'''
            cursor.execute(query, (airline))
            data1 = cursor.fetchall()
            cursor.close()

            return render_template('view-frequent-customer.html', customers=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# todo:view flights taken
# 前端未完成
@app.route('/view_all_customers', methods=['GET', 'POST'])
def view_all_customers():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            return redirect(url_for('viewAllCustomers'))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/viewAllCustomers', methods=['GET', 'POST'])
def viewAllCustomers():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']

            cursor = conn.cursor()
            query = '''select distinct email, name
            from ticket natural join purchase natural join customer
            where airline_name = %s'''
            cursor.execute(query, (airline))
            data1 = cursor.fetchall()
            cursor.close()

            return render_template('view-all-customers.html', customers=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/viewFlightsTaken', methods=['GET', 'POST'])
def viewFlightsTaken():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            email = request.form['email']
            name = request.form['name']

            cursor = conn.cursor()
            query = '''select *
            from flight natural join ticket natural join purchase
            where airline_name = %s
            and email = %s'''
            cursor.execute(query, (airline, email))
            data1 = cursor.fetchall()
            cursor.close()

            return render_template('view-flights-taken.html', name=name, flights=data1)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# todo:view ticket sales report
# 前端未完成
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            to_date = datetime.date.today()
            from_date = to_date + relativedelta.relativedelta(years=-1)
            # Total
            cursor = conn.cursor()
            query = '''select count(ticket_id)
            from ticket natural join purchase
            where airline_name = %s and purchase_date between %s and %s'''
            cursor.execute(query, (airline, from_date, to_date))
            total = cursor.fetchall()
            if total[0]['count(ticket_id)'] == None:
                total[0]['count(ticket_id)'] = 0
            cursor.close()
            # Monthly
            cursor = conn.cursor()
            monthly_sales = []
            months = []
            date1 = datetime.datetime.strptime(str(from_date), '%Y-%m-%d')
            date2 = datetime.datetime.strptime(str(to_date), '%Y-%m-%d')
            # r = relativedelta.relativedelta(date2, date1)
            # month_number = r.months + r.years*12
            month_number = (date2.year - date1.year) * 12 + date2.month - date1.month
            if from_date.day != 1:
                month_number += 1
            for i in range(month_number):
                query = '''select count(ticket_id)
                from ticket natural join purchase
                where airline_name = %s
                and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
                and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
                if from_date.month + i <= 12:
                    from_d_year = from_date.year
                    from_d_month = from_date.month + i
                else:
                    from_d_year = from_date.year + 1
                    from_d_month = from_date.month + i - 12
                if from_date.month + i + 1 <= 12:
                    to_d_year = from_date.year
                    to_d_month = from_date.month + i + 1
                else:
                    to_d_year = from_date.year + 1
                    to_d_month = from_date.month + i - 11
                if i == 0:
                    from_d_day = from_date.day
                else:
                    from_d_day = 1
                if i == month_number - 1:
                    to_d_month = to_date.month
                    to_d_day = to_date.day
                else:
                    to_d_day = 1
                from_d = datetime.date(from_d_year, from_d_month, from_d_day)
                to_d = datetime.date(to_d_year, to_d_month, to_d_day)
                cursor.execute(query, (airline, from_d, to_d))
                monthly = cursor.fetchall()
                if monthly[0]['count(ticket_id)'] == None:
                    monthly[0]['count(ticket_id)'] = 0
                months.append(str(from_d_year) + "-" + str(from_d_month))
                monthly_sales.append(monthly)
            cursor.close()

            return render_template('view-ticket-sales.html', from_date=from_date, to_date=to_date,
                                   total=total[0]['count(ticket_id)'], monthly_sales=monthly_sales, months=months,
                                   display_number=month_number)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


@app.route('/salesStaff', methods=['GET', 'POST'])
def salesStaff():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            try:
                autoChoice = request.form['autoChoice']
            except:
                autoChoice = None
            if autoChoice == 'View last month':
                TODAY = datetime.date.today()
                from_date = str(TODAY + relativedelta.relativedelta(months=-1, day=1))
                to_date = str(TODAY + relativedelta.relativedelta(day=1))
                to_date = str(to_date)
            elif autoChoice == 'View last year':
                to_date = datetime.date.today()
                from_date = str(to_date + relativedelta.relativedelta(years=-1))
                to_date = str(to_date)
            else:
                from_date = request.form['from-date']
                to_date = request.form['to-date']
            cursor = conn.cursor()
            query = '''select count(ticket_id)
            from ticket natural join purchase
            where airline_name = %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
            and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
            cursor.execute(query, (airline, from_date, to_date))
            total = cursor.fetchall()
            if total[0]['count(ticket_id)'] == None:
                total[0]['count(ticket_id)'] = 0
            cursor.close()
            # Track-monthly
            cursor = conn.cursor()
            monthly_sales = []
            months = []
            date1 = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            # r = relativedelta.relativedelta(date2, date1)
            # month_number = r.months + r.years*12
            year_number = date2.year - date1.year + 1
            for i in range(year_number):
                if i == 0 and year_number > 1:
                    month_number = 13 - date1.month
                    init_month = date1.month
                elif i == year_number - 1 and year_number > 1:
                    if date2.day == 1:
                        month_number = date2.month - 1
                    else:
                        month_number = date2.month
                    init_month = 1
                elif year_number > 1:
                    month_number = 12
                    init_month = 1
                else:
                    if date2.day == 1:
                        month_number = date2.month - date1.month
                    else:
                        month_number = date2.month - date1.month + 1
                    init_month = date1.month
                for j in range(month_number):
                    query = '''select count(ticket_id)
                    from ticket natural join purchase
                    where airline_name = %s
                    and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) >= %s
                    and timestamp(cast(purchase_date as datetime)+cast(purchase_time as time)) < %s'''
                    if init_month + j <= 12:
                        from_d_year = date1.year + i
                        from_d_month = init_month + j
                    else:
                        from_d_year = date1.year + 1 + i
                        from_d_month = init_month + j - 12
                    if init_month + j + 1 <= 12:
                        to_d_year = date1.year + i
                        to_d_month = init_month + j + 1
                    else:
                        to_d_year = date1.year + 1 + i
                        to_d_month = init_month + j - 11
                    if j == 0 and i == 0:
                        from_d_day = date1.day
                    else:
                        from_d_day = 1
                    if j == month_number - 1 and i == year_number - 1:
                        to_d_month = date2.month
                        to_d_day = date2.day
                    else:
                        to_d_day = 1
                    from_d = datetime.date(from_d_year, from_d_month, from_d_day)
                    to_d = datetime.date(to_d_year, to_d_month, to_d_day)
                    cursor.execute(query, (airline, from_d, to_d))
                    monthly = cursor.fetchall()
                    if monthly[0]['count(ticket_id)'] == None:
                        monthly[0]['count(ticket_id)'] = 0
                    months.append(str(from_d_year) + "-" + str(from_d_month))
                    monthly_sales.append(monthly)
            month_number = (date2.year - date1.year) * 12 + date2.month - date1.month
            if date2.day != 1:
                month_number += 1
            cursor.close()

            return render_template('view-ticket-sales.html', from_date=from_date, to_date=to_date,
                                   total=total[0]['count(ticket_id)'], monthly_sales=monthly_sales, months=months,
                                   display_number=month_number)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# todo:quarterly revenue
# 缺前端接口
@app.route('/revenue', methods=['GET', 'POST'])
def revenue():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            year = datetime.date.today().year
            from_date1 = datetime.date(year, 1, 1)
            to_date1 = datetime.date(year, 3, 31)
            from_date2 = datetime.date(year, 4, 1)
            to_date2 = datetime.date(year, 6, 30)
            from_date3 = datetime.date(year, 7, 1)
            to_date3 = datetime.date(year, 9, 30)
            from_date4 = datetime.date(year, 10, 1)
            to_date4 = datetime.date(year, 12, 31)
            dates = [[from_date1, to_date1], [from_date2, to_date2], [from_date3, to_date3], [from_date4, to_date4]]

            revenues = []
            for i in range(4):
                cursor = conn.cursor()
                query = '''select sum(sold_price)
                    from ticket natural join purchase
                    where purchase_date between %s and %s
                    and airline_name = %s'''
                cursor.execute(query, (dates[i][0], dates[i][1], airline))
                quarterly = cursor.fetchall()
                cursor.close()
                if quarterly[0]['sum(sold_price)'] == None:
                    quarterly[0]['sum(sold_price)'] = 0
                revenues.append(quarterly)
            return render_template('revenue-staff.html', revenues=revenues)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# todo:top destinations*3
# 前端未完成
@app.route('/topDestination', methods=['GET', 'POST'])
def topDestination():
    try:
        usertype = session['usertype']
        if usertype == "staff":
            airline = session['airline']
            TODAY = datetime.date.today()
            from_date1 = TODAY + relativedelta.relativedelta(months=-3, day=1)
            to_date1 = TODAY + relativedelta.relativedelta(months=-1, day=31)
            from_date2 = datetime.date(TODAY.year - 1, 1, 1)
            to_date2 = datetime.date(TODAY.year - 1, 12, 31)

            cursor = conn.cursor()
            query = '''select view.arrival_airport, view.city
            from (select airline_name, arrival_airport, city, sum(tickets_sold) as num_ticket
                from flight_seats_sold natural join flight natural join airport
                where arrival_airport = airport_name and airline_name = %s and departure_date between %s and %s
                group by airline_name, arrival_airport, city) as view
            order by view.num_ticket desc
            limit 3'''
            cursor.execute(query, (airline, from_date1, to_date1))
            data1 = cursor.fetchall()
            cursor.close()

            cursor = conn.cursor()
            query = '''select view.arrival_airport, view.city
            from (select airline_name, arrival_airport, city, sum(tickets_sold) as num_ticket
                from flight_seats_sold natural join flight natural join airport
                where arrival_airport = airport_name and airline_name = %s and departure_date between %s and %s
                group by airline_name, arrival_airport, city) as view
            order by view.num_ticket desc
            limit 3'''
            cursor.execute(query, (airline, from_date2, to_date2))
            data2 = cursor.fetchall()
            cursor.close()

            return render_template("top-destinations.html", destinations_month=data1, destinations_year=data2)
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('public'))


# ===============================================================================
# ===============================================================================
# =========================LOGOUT===================
# logout is the same for customer and staff
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    usertype = session['usertype']
    if usertype == "customer":
        if session.get("searchCustomer") is not None:
            session.pop('searchCustomer')
        if session.get("flight_info1") is not None:
            session.pop('flight_info1')
        if session.get("flight_info2") is not None:
            session.pop('flight_info2')
    elif usertype == "staff":
        session.pop('airline')
    session.pop('usertype')
    session.pop('username')
    return render_template("logout.html")


# ========================END============================
# you can set secret_key as random
app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
