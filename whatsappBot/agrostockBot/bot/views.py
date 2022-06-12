from django.shortcuts import render

# Create your views here.
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView

# Create your views here.
from twilio.twiml.messaging_response import MessagingResponse, Media, Message, Body
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelform_factory
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
import re, mysql.connector, shelve, os.path
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
import datetime as dt

class Index:
    @csrf_exempt
    def index(request):
        resp=MessagingResponse()
        msg=resp.message()
        
        

        if request.method =='POST':
            incoming_message=request.POST['Body'].lower()

            #Regex for placing an order
            text=re.compile(r'b\d*,\d*')
            finder=text.findall(incoming_message)

            phonenumber=request.POST['From']

            phone_number = str(phonenumber)
            print(phone_number)
            print(type(phone_number))

            fon_finder = re.compile(r'\+\w*')
            fon_found = fon_finder.search(phone_number)
            phonenumberx = fon_found.group(0)
            print(phonenumberx)

            db = mysql.connector.connect(
                option_files = r'C:\Users\Tino\Documents\whatsappBot\agrostockBot\server_config.ini', use_pure=True
            )

            cursor = db.cursor()

            sql2 = "SELECT session.users.phonenumber FROM session.users ORDER BY session.users.id"
            cursor.execute(sql2)

            numbers = []

            results = cursor.fetchall()

            for result1 in results:
                for result in result1:
                    if result:
                        numbers.append(result)

            sql6 = "SELECT session.users.username FROM session.users ORDER BY session.users.id"
            cursor.execute(sql6)

            answers = cursor.fetchall()

            users = []

            for answer1 in answers:
                for answer in answer1:
                    if answer:
                        users.append(answer)

            global x

            sql8 = "SELECT session.users.id FROM session.users ORDER BY session.users.id"
            cursor.execute(sql8)
            iDs = cursor.fetchall()

            if phonenumberx not in numbers:
                x=len(numbers)+1
                username = "user{0}".format(x)
                sql1 = "INSERT INTO session.users(phonenumber, username) VALUES (%s, %s)"
                params1 = ('{0}'.format(phonenumberx), '{0}'.format(username))
                cursor.execute(sql1, params1)
                if True:
                    sql3 = """CREATE TABLE session.{0}(id INT AUTO_INCREMENT,
                            message VARCHAR(100),
                            mes_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY(id))""".format(username)
                    cursor.execute(sql3)
            else:
                pass

            list1 = []

            sql6 = "SELECT phonenumber, username FROM session.users ORDER BY id"
            cursor.execute(sql6)
            city = cursor.fetchone()
            while (city):
                x = '\'{0}\':\'{1}\''.format(
                        city[0],
                        city[1]
                )
                list1.append(x)
                city = cursor.fetchone()

            print(list1)

            list2 = []
            list3 = []

            for i in list1:
                ifinder = re.compile(r'\+\w*\'')
                found = ifinder.search(i)
                if found != None:
                    list2.append(found.group(0))

            for n in list1:
                ifinder1 = re.compile(r'\'\w*\'$')
                found1 = ifinder1.search(n)
                if found1 != None:
                    list3.append(found1.group(0))
            
            print(list2)

            list4 = []
            list5 = []

            for x in list2:
                ifinder2 = re.compile(r'\+\w+')
                found2 = ifinder2.search(x)
                if found2 != None:
                    list4.append(found2.group(0))

            for v in list3:
                ifinder3 = re.compile(r'\w+')
                found3 = ifinder3.search(v)
                if found3 != None:
                    list5.append(found3.group(0))


            dict1 = dict(zip(list4,list5))
            print(dict1)

            global name

            for i,n in dict1.items():
                if phonenumberx == i:
                    name = n
                else:
                    pass

            try:
                sql120 = "SELECT mes_date FROM session.{} ORDER BY id".format(name)
                cursor.execute(sql120)
            except:
                response = 'There was an error please standby'
                print(response)
                

            list10 = []
            list11 = []

            city5 = cursor.fetchone()

            global total_time
            if city5 != None:
                while (city5):
                    x = '\'{0}\''.format(
                            city5[0]
                    )
                    list10.append(x)
                    city5 = cursor.fetchone()

                for i in list10:
                    finder = re.compile(r'\d+')
                    found = finder.findall(i)
                    list11.append(found)

                global n1
                for t in list11:
                    n1 = dt.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]))

                x1 = dt.datetime.now()-n1

                global found11
                finder10 = re.compile(r'\s+')
                found10 = finder10.search(str(x1))
                if found10 == None:
                    finder = re.compile(r'\d*\:\d*\.\d*$')
                    found = finder.search(str(x1))
                    finder2 = re.compile(r'\d\d')
                    found11 = finder2.findall(str(found))
                    total_time = (int(found11[1])*60)+int(found11[2])
                else:
                    finder = re.compile(r'\d+')
                    found = finder.findall(str(x1))
                    print(found)
                    print(found[0])
                    print(found[1])
                    if len(found) == 5:
                        b1 = (found[0]*24)+found[1]
                        b2 = ((b1*60)+found[2])*60
                        total_time = b2+found[3]
                        print(total_time)

                if int(total_time)>=120:
                    sql121 = 'TRUNCATE TABLE session.{}'.format(name)
                    cursor.execute(sql121)
                    print('tapfuura neko')
                else:
                    pass
            else:
                total_time = 0
 
            for i,n in dict1.items():
                if phonenumberx == i:
                    sql7 = 'INSERT INTO session.{0}(message) VALUES(\'{1}\')'.format(n,incoming_message)
                    cursor.execute(sql7)
                    db.commit()
                else:
                    pass

            sql15 = 'SELECT id, message FROM session.{0} ORDER BY id'.format(name)
            cursor.execute(sql15)
            mes = cursor.fetchone()

            list6 = []
            while (mes):
                x = '\'{0}\':\'{1}\''.format(
                        mes[0],
                        mes[1]
                )
                list6.append(x)
                mes = cursor.fetchone()



            list7 = []
            list8 = []
            for q in list6:
                ifinder4 = re.compile(r'^\'\d*\'')
                found4 = ifinder4.search(q)
                if found4 != None:
                    list7.append(found4.group(0))

            for w in list6:
                ifinder5 = re.compile(r'\'\d*\'$')
                found5 = ifinder5.search(w)
                if found5 != None:
                    list8.append(found5.group(0))
                else:
                    ifinders = re.compile(r'\'\w*\'$')
                    founds = ifinders.search(w)
                    list8.append(founds.group(0))

            list9 = []
            list10 = []
            print(list7)
            print(list8)

            for e in list7:
                ifinder6 = re.compile(r'\d+')
                found6 = ifinder6.search(e)
                if found6 != None:
                    list9.append(found6.group(0))

            for r in list8:
                ifinder7 = re.compile(r'\d+')
                found7 = ifinder7.search(r)
                if found7 != None:
                    list10.append(found7.group(0))
                else:
                    ifinders1 = re.compile(r'\w+')
                    founds1 = ifinders1.search(r)
                    list10.append(founds1.group(0))


            dict2 = dict(zip(list9,list10))
            print(dict2)

            a = len(dict2)
            a1 = len(dict2)-1
            a2 = len(dict2)-2
            a3 = len(dict2)-3
            a4 = len(dict2)-4

            aTuple = (a, a1, a2, a3, a4)



            #Dictionary of the products
            product_dict={'1':'Maize', '2':'Potatoes', '3':'Wheat', '4':'Rapoko', '5':'Tobacco', '6':'Cotton'}
                    
            #Dictionary of prices
            price_dict={'1': 0.1, '2': 0.7, '3': 1, '4': 2, '5': 3, '6': 3}

            c = r'C:\Users\Tino\Documents\whatsappBot\agrostockBot\\{}.dat'.format('product_cart')
            if total_time>120:
                cart4 = []
                product_cart = shelve.open('product_cart')
                product_cart['{}'.format(name)] = cart4
            else:
                if os.path.exists(c) == False:
                    cart4 = []
                    product_cart = shelve.open('product_cart')
                    product_cart['{}'.format(name)] = cart4
                else:
                    try:
                        product_cart = shelve.open('product_cart')
                        cart4 = product_cart['{}'.format(name)]
                    except:
                        pass

            d = r'C:\Users\Tino\Documents\whatsappBot\agrostockBot\\{}.dat'.format('name_cart')
            if total_time > 120:
                cart5 = []
                name_cart = shelve.open('name_cart')
                name_cart['{}'.format(name)] = cart5
            else:
                if os.path.exists(d) == False:
                    cart5 = []
                    name_cart = shelve.open('name_cart')
                    name_cart['{}'.format(name)] = cart5
                else:
                    try:
                        name_cart = shelve.open('name_cart')
                        cart5 = name_cart['{}'.format(name)]
                    except:
                        pass


            w = r'C:\Users\Tino\Documents\whatsappBot\agrostockBot\\{}.dat'.format('price_cart')
            if total_time>120:
                cart = []
                price_cart = shelve.open('price_cart')
                price_cart['{}'.format(name)] = cart
                if os.path.exists(w) == False:
                    cart = []
                    price_cart = shelve.open('price_cart')
                    price_cart['{}'.format(name)] = cart
                    print('tachiwana')
                else:
                    price_cart = shelve.open('price_cart')
                    cart = price_cart['{}'.format(name)]
                    print(print('tachishaya'))
            else:
                if os.path.exists(w) == False:
                    cart = []
                    price_cart = shelve.open('price_cart')
                    price_cart['{}'.format(name)] = cart
                    print('tachiwana1')
                else:
                    try:
                        price_cart = shelve.open('price_cart')
                        cart = price_cart['{}'.format(name)]
                        print(print('tachishaya1'))
                    except:
                        pass


            text=re.compile(r'b\d*,\d*')
            finder=text.findall(incoming_message)
            global product1 
            
            try:
                
                print('yajumha')
                if dict2[str(a3)] == 'hello':
                    if dict2[str(a2)] == '1':
                        if dict2[str(a1)] == '1':
                            cart2 = '1'
                            product1 = incoming_message
                            if incoming_message != None:
                                try:
                                    x = dict2[str(a1)]
                                    price1 = price_dict[x]*int(incoming_message)
                                    response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                    print(response)
                                except:
                                    print('Please only send numbers no letters or symbols')

                        elif dict2[str(a1)] == '2':
                            cart2 = '2'
                            product1 = incoming_message
                            if incoming_message != None:
                                try:
                                    x = dict2[str(a1)]
                                    price1 = price_dict[x]*int(incoming_message)
                                    response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                    print(response)
                                except:
                                    print('Please only send numbers no letters or symbols')

                        elif dict2[str(a1)] == '3':
                            cart2 = '3'
                            product1 = incoming_message
                            if incoming_message != None:
                                try:
                                    x = dict2[str(a1)]
                                    price1 = price_dict[x]*int(incoming_message)
                                    response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                    print(response)
                                except:
                                    print('Please only send numbers no letters or symbols')

                        elif dict2[str(a1)] == '4':
                            cart2 = '4'
                            product1 = incoming_message
                            if incoming_message != None:
                                try:
                                    x = dict2[str(a1)]
                                    price1 = price_dict[x]*int(incoming_message)
                                    response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                    print(response)
                                except:
                                    print('Please only send numbers no letters or symbols')

                        elif dict2[str(a1)] == '5':
                            cart2 = '5'
                            product1 = incoming_message
                            if incoming_message != None:
                                try:
                                    x = dict2[str(a1)]
                                    price1 = price_dict[x]*int(incoming_message)
                                    response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                    print(response)
                                except:
                                    print('Please only send numbers no letters or symbols')

                        elif dict2[str(a1)] == '6':
                            cart2 = '6'
                            product1 = incoming_message
                            if incoming_message != None:
                                try:
                                    x = dict2[str(a1)]
                                    price1 = price_dict[x]*int(incoming_message)
                                    response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                    print(response)
                                except:
                                    print('Please only send numbers no letters or symbols') 

                elif dict2[str(a2)] == '0':
                    if dict2[str(a1)] == '1':
                        cart2 = '1'
                        product1 = incoming_message
                        if incoming_message != None:
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                print(response)
                            except:
                                print('Please only send numbers no letters or symbols')

                    elif dict2[str(a1)] == '2':
                        cart2 = '2'
                        product1 = incoming_message
                        if incoming_message != None:
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                print(response)
                            except:
                                print('Please only send numbers no letters or symbols')

                    elif dict2[str(a1)] == '3':
                        cart2 = '3'
                        product1 = incoming_message
                        if incoming_message != None:
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                print(response)
                            except:
                                print('Please only send numbers no letters or symbols')

                    elif dict2[str(a1)] == '4':
                        cart2 = '4'
                        product1 = incoming_message
                        if incoming_message != None:
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                print(response)
                            except:
                                print('Please only send numbers no letters or symbols')

                    elif dict2[str(a1)] == '5':
                        cart2 = '5'
                        product1 = incoming_message
                        if incoming_message != None:
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                print(response)
                            except:
                                print('Please only send numbers no letters or symbols')

                    elif dict2[str(a1)] == '6':
                        cart2 = '6'
                        product1 = incoming_message
                        if incoming_message != None:
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                print(response)
                            except:
                                print('Please only send numbers no letters or symbols')  
            except:
                print('yapotsa')

            #The dialogue of the bot
            if dict2[str(a)]=='hello':
                response1='Hi {0} I am Agrostock your number one agricultural produce shop. I buy and sell agricultural produce'.format(phonenumberx)
                response='''How can i help you:

1. Make purchase
2. Request catalogue
3. Customer service
4. Merchant
5. View Cart
                                                
Select an option by typing A then the 
number of the option selected.'''
                msg.body(response1+response)
                return HttpResponse(str(resp))
                

            elif dict2[str(a1)] == 'hello':
                                
                #Place order to see product list
                if dict2[str(a)] == '1':
                    response1 = '''1. Maize at $0.10 per kg
2. Potatoes at $0.70 per kg
3. Sweet Potatoes at $1.00 per kg
4. Wheat at $2.00 per kg
5. Tobacco at $3.00 per kg
6. Cotton at $3.00 per kg'''
                    msg.body(response1)
                    return HttpResponse(str(resp))
                    

            elif dict2[str(a2)] == 'hello':
                if dict2[str(a1)] == '1':
                    if dict2[str(a)] == '1':
                        response = 'How many kgs do you want?'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        
                    elif dict2[str(a)] == '2':
                        response = 'How many kgs do you want?'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        
                    elif dict2[str(a)] == '3':
                        response = 'How many kgs do you want?'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        
                    elif dict2[str(a)] == '4':
                        response = 'How many kgs do you want?'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        
                    elif dict2[str(a)] == '5':
                        response = 'How many kgs do you want?'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        
                    elif dict2[str(a)] == '6':
                        response = 'How many kgs do you want?'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        
                    else:
                        return HttpResponse('Please restart from hello')
                        

            elif dict2[str(a3)] == 'hello':
                if dict2[str(a2)] == '1':
                    if dict2[str(a1)] == '1':
                        cart2 = '1'
                        product1 = incoming_message
                        if incoming_message != None:
                            
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                print('price1')
                                cart.append(price1)
                                price_cart['{}'.format(name)] = cart

                                print('product1')
                                cart4.append(product1)
                                product_cart['{}'.format(name)] = cart4

                                print('name1')
                                cart5.append(cart2)
                                name_cart['{}'.format(name)] = cart5

                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                msg.body(response)
                                return HttpResponse(str(resp))
                                
                            except:
                                price1 = 0
                                return HttpResponse('Please only send numbers no letters or symbols')
                                

                    elif dict2[str(a1)] == '2':
                        cart2 = '2'
                        product1 = incoming_message
                        if incoming_message != None:
                            
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)

                                print('price1')
                                cart.append(price1)
                                price_cart['{}'.format(name)] = cart

                                print('product1')
                                cart4.append(product1)
                                product_cart['{}'.format(name)] = cart4

                                print('name1')
                                cart5.append(cart2)
                                name_cart['{}'.format(name)] = cart5

                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                msg.body(response)
                                return HttpResponse(str(resp))
                                
                            except:
                                price1 = 0
                                response ='Please only send numbers no letters or symbols'
                                msg.body(response)
                                return HttpResponse(str(resp))
                                

                    elif dict2[str(a1)] == '3':
                        cart2 = '3'
                        product1 = incoming_message
                        if incoming_message != None:
                            
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)

                                print('price1')
                                cart.append(price1)
                                price_cart['{}'.format(name)] = cart

                                print('product1')
                                cart4.append(product1)
                                product_cart['{}'.format(name)] = cart4

                                print('name1')
                                cart5.append(cart2)
                                name_cart['{}'.format(name)] = cart5

                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                msg.body(response)
                                return HttpResponse(str(resp))
                                
                            except:
                                price1 = 0
                                response ='Please only send numbers no letters or symbols'
                                msg.body(response)
                                return HttpResponse(str(resp))
                                

                    elif dict2[str(a1)] == '4':
                        cart2 = '4'
                        product1 = incoming_message
                        if incoming_message != None:
                            
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)

                                print('price1')
                                cart.append(price1)
                                price_cart['{}'.format(name)] = cart

                                print('product1')
                                cart4.append(product1)
                                product_cart['{}'.format(name)] = cart4

                                print('name1')
                                cart5.append(cart2)
                                name_cart['{}'.format(name)] = cart5

                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                msg.body(response)
                                return HttpResponse(str(resp))
                                
                            except:
                                price1 = 0
                                response ='Please only send numbers no letters or symbols'
                                msg.body(response)
                                return HttpResponse(str(resp))
                                

                    elif dict2[str(a1)] == '5':
                        cart2 = '5'
                        product1 = incoming_message
                        if incoming_message != None:
                            
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                msg.body(response)
                                return HttpResponse(str(resp))
                                
                            except:
                                price1 = 0
                                response ='Please only send numbers no letters or symbols'
                                msg.body(response)
                                return HttpResponse(str(resp))
                                

                    elif dict2[str(a1)] == '6':
                        cart2 = '6'
                        product1 = incoming_message
                        if incoming_message != None:
                            
                            try:
                                x = dict2[str(a1)]
                                price1 = price_dict[x]*int(incoming_message)
                                response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                                msg.body(response)
                                return HttpResponse(str(resp))
                                
                            except:
                                price1 = 0
                                response ='Please only send numbers no letters or symbols'
                                msg.body(response)
                                return HttpResponse(str(resp)) 
                                  

            elif dict2[str(a)] == '0':
                    response1 = '''1. Maize at $0.10 per kg
2. Potatoes at $0.70 per kg
3. Sweet Potatoes at $1.00 per kg
4. Wheat at $2.00 per kg
5. Tobacco at $3.00 per kg
6. Cotton at $3.00 per kg'''
                    msg.body(response1)
                    return HttpResponse(str(resp))
                    

            elif dict2[str(a1)] == '0':
                if dict2[str(a)] == '1':
                    response = 'How many kgs do you want?'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                elif dict2[str(a)] == '2':
                    response = 'How many kgs do you want?'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                elif dict2[str(a)] == '3':
                    response = 'How many kgs do you want?'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                elif dict2[str(a)] == '4':
                    response = 'How many kgs do you want?'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                elif dict2[str(a)] == '5':
                    response = 'How many kgs do you want?'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                elif dict2[str(a)] == '6':
                    response = 'How many kgs do you want?'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                else:
                    response='Please restart from hello'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    

            elif dict2[str(a2)] == '0':
                if dict2[str(a1)] == '1':
                    cart2 = '1'
                    product1 = incoming_message
                    if incoming_message != None:
                        
                        try:
                            x = dict2[str(a1)]
                            price1 = price_dict[x]*int(incoming_message)

                            print('price1')
                            cart.append(price1)
                            price_cart['{}'.format(name)] = cart

                            print('product1')
                            cart4.append(product1)
                            product_cart['{}'.format(name)] = cart4

                            print('name1')
                            cart5.append(cart2)
                            name_cart['{}'.format(name)] = cart5

                            response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                            msg.body(response)
                            return HttpResponse(str(resp))
                            
                        except:
                            price1 = 0
                            response ='Please only send numbers no letters or symbols'
                            msg.body(response)
                            return HttpResponse(str(resp))
                            

                elif dict2[str(a1)] == '2':
                    cart2 = '2'
                    product1 = incoming_message
                    if incoming_message != None:
                        
                        try:
                            x = dict2[str(a1)]
                            price1 = price_dict[x]*int(incoming_message)

                            print('price1')
                            cart.append(price1)
                            price_cart['{}'.format(name)] = cart

                            print('product1')
                            cart4.append(product1)
                            product_cart['{}'.format(name)] = cart4

                            print('name1')
                            cart5.append(cart2)
                            name_cart['{}'.format(name)] = cart5

                            response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                            msg.body(response)
                            return HttpResponse(str(resp))
                            
                        except:
                            price1 = 0
                            response ='Please only send numbers no letters or symbols'
                            msg.body(response)
                            return HttpResponse(str(resp))
                            

                elif dict2[str(a1)] == '3':
                    cart2 = '3'
                    product1 = incoming_message
                    if incoming_message != None:
                        
                        try:
                            x = dict2[str(a1)]
                            price1 = price_dict[x]*int(incoming_message)

                            print('price1')
                            cart.append(price1)
                            price_cart['{}'.format(name)] = cart

                            print('product1')
                            cart4.append(product1)
                            product_cart['{}'.format(name)] = cart4

                            print('name1')
                            cart5.append(cart2)
                            name_cart['{}'.format(name)] = cart5

                            response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                            msg.body(response)
                            return HttpResponse(str(resp))
                            
                        except:
                            price1 = 0
                            response ='Please only send numbers no letters or symbols'
                            msg.body(response)
                            return HttpResponse(str(resp))
                            

                elif dict2[str(a1)] == '4':
                    cart2 = '4'
                    product1 = incoming_message
                    if incoming_message != None:
                        
                        try:
                            x = dict2[str(a1)]
                            price1 = price_dict[x]*int(incoming_message)

                            print('price1')
                            cart.append(price1)
                            price_cart['{}'.format(name)] = cart

                            print('product1')
                            cart4.append(product1)
                            product_cart['{}'.format(name)] = cart4

                            print('name1')
                            cart5.append(cart2)
                            name_cart['{}'.format(name)] = cart5

                            response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                            msg.body(response)
                            return HttpResponse(str(resp))
                            
                        except:
                            price1 = 0
                            response ='Please only send numbers no letters or symbols'
                            msg.body(response)
                            return HttpResponse(str(resp))
                            

                elif dict2[str(a1)] == '5':
                    cart2 = '5'
                    product1 = incoming_message
                    if incoming_message != None:
                        
                        try:
                            x = dict2[str(a1)]
                            price1 = price_dict[x]*int(incoming_message)

                            print('price1')
                            cart.append(price1)
                            price_cart['{}'.format(name)] = cart

                            print('product1')
                            cart4.append(product1)
                            product_cart['{}'.format(name)] = cart4

                            print('name1')
                            cart5.append(cart2)
                            name_cart['{}'.format(name)] = cart5

                            response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                            msg.body(response)
                            return HttpResponse(str(resp))
                            
                        except:
                            price1 = 0
                            response ='Please only send numbers no letters or symbols'
                            msg.body(response)
                            return HttpResponse(str(resp))
                            

                elif dict2[str(a1)] == '6':
                    cart2 = '6'
                    product1 = incoming_message
                    if incoming_message != None:
                        
                        try:
                            x = dict2[str(a1)]
                            price1 = price_dict[x]*int(incoming_message)

                            print('price1')
                            cart.append(price1)
                            price_cart['{}'.format(name)] = cart

                            print('product1')
                            cart4.append(product1)
                            product_cart['{}'.format(name)] = cart4

                            print('name1')
                            cart5.append(cart2)
                            name_cart['{}'.format(name)] = cart5

                            response = '''It will cost ${0}.
If you would like to order another product send 0.
If you are done or to view cart send cart'''.format(price1)
                            msg.body(response)
                            return HttpResponse(str(resp))
                            
                        except:
                            price1 = 0
                            response ='Please only send numbers no letters or symbols'
                            msg.body(response)
                            return HttpResponse(str(resp)) 
                            


            elif dict2[str(a1)] == 'hello':
                if dict2[str(a)] == '3':
                    response='''Please type the problem code eg "*c1*" at the beginning of your problem statement
1. Ask for help?
2. Report a problem?

Thank you. We will get back to you'''
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
                            
                        #Login Link need more code under there
            elif dict2[str(a1)] == 'hello':
                if dict2[str(a)] == '6':
                    response='http://1d07aa7c6cd9.ngrok.io/home/'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    

            elif dict2[str(a1)] == 'hello':
                if dict2[str(a)] == '2':
                    response='https://wa.me/c/263715202419'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    

            elif dict2[str(a1)] == 'hello':
                if dict2[str(a)] == '5':
                    cart1 = price_cart['{}'.format(name)]
                    p = sum(cart1)
                    
                    try:
                        response7 = ''
                        for i,m in zip(product_cart['{}'.format(name)],name_cart['{}'.format(name)]):
                            response = '{1} {0}kgs \n'.format(i, product_dict['{}'.format(m)])
                            response7 += response
                        response2 = 'Total cost is ${}'.format(p)
                        msg.body(response7+response2)
                        return HttpResponse(str(resp))
                        
                    except:
                        response = 'Im sorry your cart is empty. Please place an order'
                        msg.body(response)
                        return HttpResponse(str(resp))
                        

            elif dict2[str(a)] == 'cart':
                cart1 = price_cart['{}'.format(name)]
                p = sum(cart1)
                
                try:
                    response7 = ''
                    for i,m in zip(product_cart['{}'.format(name)],name_cart['{}'.format(name)]):
                        response = '{1} {0}kgs \n'.format(i, product_dict['{}'.format(m)])
                        response7 += response
                    response2 = 'Total cost is ${}'.format(p)
                    msg.body(response7+response2)
                    return HttpResponse(str(resp))
                    
                except:
                    response = 'Im sorry your cart is empty'
                    msg.body(response)
                    return HttpResponse(str(resp))
                    

            elif dict2[str(a)]=='2':
                response = 'Tikudzifambira nyaya dzacho'

            elif dict2[str(a1)] == '1':
                if dict2[str(a)] == '1':
                    response = '''1. Maize
2. Potatoes
3. Sweet Potatoes
4. Wheat
5. Tobacco
6. Cotton'''
                    msg.body(response)
                    return HttpResponse(str(resp))
                    
            
            elif dict2[str(a1)] == 'hello':
                                
                #Place order to see product list
                if dict2[str(a)] == '2':
                    response1 = '''NDICHAISA URL'''
                    msg.body(response1)
                    return HttpResponse(str(resp))
                    

            else:
                response = 'Wrong input method'
                msg.body(response)
                return HttpResponse(str(resp))
                

            print(list(product_cart.keys()))
            print(list(name_cart.keys()))
            print(list(price_cart.keys()))

            print(list(product_cart.values()))
            print(list(name_cart.values()))
            print(list(price_cart.values()))

            price_cart.close()
            product_cart.close()
            name_cart.close()

            db.commit()
            cursor.close()
            db.close()
