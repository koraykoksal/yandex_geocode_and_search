
from typing import OrderedDict, Text
from flask import Flask, app,flash,redirect,url_for,session,logging,request,jsonify
from flask.templating import render_template
from flask_mysqldb import MySQL
from requests.api import post
from requests.sessions import Request
from wtforms import Form, StringField, TextAreaField, PasswordField,validators
from passlib.hash import sha256_crypt
import requests
import json

from os import name, write
from typing import Text
from numpy.lib.function_base import append
from numpy.lib.shape_base import split
import math
import numpy as np
from requests.api import get
import functools
import MySQLdb.cursors
import cgi, cgitb


# Kullanıcı kayıt formu
class registerForm(Form):
    name = StringField('Name', validators=[validators.Length(min=4, max=25),validators.data_required()])
    username = StringField('Username', validators=[validators.Length(min=4, max=25),validators.data_required()])
    email = StringField('Email Address', validators=[validators.Length(min=4, max=35),validators.data_required(),validators.email(message='Please enter a valid address !')])
    password = PasswordField('New Password', [
        validators.data_required(message='Please set password !'),
        validators.equal_to(fieldname='confirm', message='Passwords must match !')

    ])
    confirm = PasswordField('Repeat Password')


class searchForm(Form):
    target_location = StringField("Destinaion Location",validators=[validators.Length(min=4, max=25),validators.data_required()])


class loginForm(Form):
    username = StringField('Username', validators=[validators.Length(min=4, max=25),validators.data_required()])
    password = PasswordField('Password', validators=[validators.Length(min=4, max=25),validators.data_required()])

#############################################################################################################################################################


app = Flask(__name__)       
app.secret_key="msg_register_key"

# mysqldb settings
app.config["MYSQL_HOST"] = "local_host" 
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kblog"
app.config["MYSQL_DATABASE_CHARSET"] = "utf-8"
app.config["MYSQL_CURSORCLASS"] = "DisctCursor"


# app and mysql connection also for connection variable object
mySQL = MySQL(app)



# request   # istek yapılan sayfa '/' root kök dizin anlamına gelir
# response  # geri cevap alınacak olan sayfa
@app.route('/') 
def index():    

    return render_template('index.html')

####################################################################################################################################################3

@app.route('/search', methods = ["GET","POST"])
def search():
    
    
    origin_location = 'moskow kremlin'
    mkad_coordinate = 'MKAD, 29-y kilometr'

    target_location = 'donskoy rayon'

    api_key_geo = 'your_key'
    api_key_sea = 'your_key'

    # location information
    target_location_request_info = requests.get('https://geocode-maps.yandex.ru/1.x/?apikey='+api_key_geo+'&format=json&lang=en-US&geocode='+target_location)
    data1 = json.loads(target_location_request_info.text)

    # location calculate coordinate
    origin_location_request_coordinate = requests.get('https://search-maps.yandex.ru/v1/?text=' + origin_location + '&type=geo&lang=ru_RU&apikey='+ api_key_sea)
    data2 = json.loads(origin_location_request_coordinate.text)

    mkad_location_request_coordinate = requests.get('https://search-maps.yandex.ru/v1/?text=' + mkad_coordinate + '&type=geo&lang=ru_RU&apikey='+ api_key_sea)
    data3 = json.loads(mkad_location_request_coordinate.text)

    target_location_request_coordinate = requests.get('https://search-maps.yandex.ru/v1/?text=' + target_location + '&type=geo&lang=ru_RU&apikey='+ api_key_sea)
    data4 = json.loads(target_location_request_coordinate.text)



    # target location informations
    coordinate_target = data1['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    country_addresline_target = data1['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
    country_namecode_target = data1['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryNameCode']


    # origin location coordinate
    coordinate_origin = data2['features'][0]['geometry']['coordinates'] # moskova kordinatları
    # moskow ring road coordinate
    coordinate_mkad = data3['features'][0]['geometry']['coordinates']   # moskova çevre yolu kordinatları
    # target location coordinate
    coordinate_target = data4['features'][0]['geometry']['coordinates']   # moskova çevre yolu kordinatları


    # origin coodinate convert
    convert_tupe_origin = tuple(coordinate_origin)   # tuple çevirme

    convert_str_origin_index0 = str(convert_tupe_origin[0])  # 0 nolu index değerini str formatına çevirme
    convert_str_origin_index1 = str(convert_tupe_origin[1])  # 1 nolu index değerini str formatına çevirme

    convert_int_origin_index0 = float(convert_tupe_origin[0])   # 0 nolu index değerini float değerine çevirme
    convert_int_origin_index1 = float(convert_tupe_origin[1])   # 1 nolu index değerini float değerine çevirme

    # mkad coordinate convert
    convert_tupe_mkad = tuple(coordinate_mkad)   # tuple çevirme

    convert_str_mkad_index0 = str(convert_tupe_mkad[0])  # 0 nolu index değerini str formatına çevirme
    convert_str_mkad_index1 = str(convert_tupe_mkad[1])  # 1 nolu index değerini str formatına çevirme

    convert_int_mkad_index0 = float(convert_tupe_mkad[0])   # 0 nolu index değerini float değerine çevirme
    convert_int_mkad_index1 = float(convert_tupe_mkad[1])   # 1 nolu index değerini float değerine çevirme


    # target coordinate convert
    convert_tupe_target = tuple(coordinate_target)   # tuple çevirme

    convert_str_target_index0 = str(convert_tupe_target[0])  # 0 nolu index değerini str formatına çevirme
    convert_str_target_index1 = str(convert_tupe_target[1])  # 1 nolu index değerini str formatına çevirme

    convert_int_target_index0 = float(convert_tupe_target[0])   # 0 nolu index değerini float değerine çevirme
    convert_int_target_index1 = float(convert_tupe_target[1])   # 1 nolu index değerini float değerine çevirme


    # Calculation of kilometers between the starting place and the moskow ring road location
    origin_and_mkad_between_km = math.sqrt((convert_int_origin_index1 + convert_int_origin_index0)*2 + (convert_int_mkad_index1 + convert_int_mkad_index0)*2 )

    # Calculation of kilometers between the starting place and the destination location
    origin_and_target_between_km = math.sqrt((convert_int_origin_index1 - convert_int_origin_index0)*2 + (convert_int_target_index1 - convert_int_target_index0)*2 )


    file = open('request_result_log.txt','w')
    #file.write(f"Target location coodinate: {coordinate_target}\nTarget lcoation address: {country_addresline_target}\nTarget location namecode: {country_namecode_target}")


    if origin_and_target_between_km > origin_and_mkad_between_km or origin_and_target_between_km == origin_and_mkad_between_km:
        print('Target Location Coordinate: ',coordinate_target)
        print('Target Location Address: ',country_addresline_target)
        print('Target Location Namecode: ',country_namecode_target)
        if_result = ('*'*5,'Destination location not inside Moskow Ring Road','*'*5)
        print(if_result)
        file.write(f"Target location coodinate: {coordinate_target}\nTarget lcoation address: {country_addresline_target}\nTarget location namecode: {country_namecode_target}\n\n{if_result}")

    else:
        print('Target Location Coordinate: ',coordinate_target)
        print('Target Location Address: ',country_addresline_target)
        print('Target Location Namecode: ',country_namecode_target)
        if_result = ('*'*5,'Destination location inside Moskow Ring Road','*'*5)
        print(if_result)
        file.write(f"Target location coodinate: {coordinate_target}\nTarget lcoation address: {country_addresline_target}\nTarget location namecode: {country_namecode_target}\n\n{if_result}")

    form = searchForm(request.form)
    

    if request.method == "POST":

        return redirect("/search")
    else:

        return render_template('search.html',form = form,coordinate_target=coordinate_target,country_addresline_target=country_addresline_target,country_namecode_target=country_namecode_target,origin_and_target_between_km=origin_and_target_between_km,origin_and_mkad_between_km=origin_and_mkad_between_km)


#############################################################################################################################################

@app.route('/register', methods = ['GET','POST'])    # buradaki url adresine hem get hemde post işlemi uygulayabilirim.
def register():

    form = registerForm(request.form)   # yukarıda oluşturulmuş olan form clası için değişken içine bir form oluşturulur ve request isteğinde bulunur.

    if request.method == 'POST' and form.validate:  # form validate kontorolü sağlansın.

        return redirect(url_for('index'))        # register işlemi yapıldıtan sonra belirtilen adrese response işlemi yap. burada istenirse belirtile url adreside yazılabilir.
    else:
        return render_template('/register.html', form = form)    # get sorgusu döndüğnde form işlemi devreye girsin.



################################################################################################################################################

@app.route('/login', methods = ['GET','POST'])
def login():


    form = loginForm(request.form)

    if request.method == 'POST' and form.validate:

        return redirect(url_for('index'))

    return render_template('/login.html',form = form)

#################################################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)     # if bloğu gerekli şartı karşılar ise app.run özelliği çalışır.






