

from flask import Flask, send_from_directory, current_app
from flask import render_template
from flask import request
from azure.storage.file import FileService, ContentSettings

import pyodbc


app = Flask(__name__)

class DBClass:
    constring = 'DRIVER={SQL Server};SERVER=picshareserver.database.windows.net;DATABASE=Picshare;UID=sam1991;PWD=azure2018.'
    account_key = 'etjPn6TajuKFOHofs9FrFFuFFc/hSPA76lj7q3VLkqds/EGibOFIZqepKcRnOVIqMnswBrpaVlpHD/TYGBVZfQ=='


@app.route('/')
def index():

    return render_template('index.html', msg = '')


@app.route('/login', methods=['post','get'])
def login():
    username = request.form['txtUserName']
    if (username==''):
        msg = 'Please Enter Username..'
        return render_template('index.html', msg=msg)
    else:
        chkCreate = request.form.get('chkCreate')
        if(chkCreate):
            return render_template('AddPic.html')

        else:
            cnxn = pyodbc.connect(DBClass.constring)
            cursor = cnxn.cursor()
            query = "SELECT pictitle, createddate, nooflikes, picture, Id, imagepath  FROM picdata where username = '"+username+"'"
            cursor.execute(query)
            data = cursor.fetchall()
            return render_template('index.html', username=username, data = data, msg='')


@app.route('/increaselikes/<dataid>')
def increaselikes(dataid):
    cnxn = pyodbc.connect(DBClass.constring)
    cursor = cnxn.cursor()
    cursor.execute("SELECT nooflikes  FROM picdata where Id = " +dataid)
    data = cursor.fetchone()
    nooflikes = data[0]
    nooflikes = nooflikes + 1
    updatequery = "update picdata set nooflikes ="+ str(nooflikes) +" where Id=" +dataid
    cursor.execute(updatequery)
    cnxn.commit()
    return render_template('index.html', msg='liked..')


@app.route('/addpicture', methods=['post', 'get'])
def addpicture():
    AddUpdatePic('Add', 0)
    msg = 'Picture added successfully..'
    return  render_template('AddPic.html', msg = msg)


def AddUpdatePic(addoredit, dataid):
    file = request.files['filename']
    file.save(file.filename)
    filename = file.filename
    username = request.form['txtusername']

    ####################################################
    file_service = FileService(account_name='picshare', account_key= DBClass.account_key)
    file_service.create_file_from_path('myshare', 'Images', filename, filename)
    imagepath = 'https://picshare.file.core.windows.net/myshare/Images/' + filename + '?sv=2017-04-17&ss=bqtf&srt=sco&sp=rwdlacup&se=2018-02-04T02:15:36Z&sig=%2FcrxJnh9mg4TrXCsVYgGGnBn7Nm2Q9FiRL3VWoyFxcY%3D'
    ####################################################

    pictitle = request.form['txttitle']
    cnxn = pyodbc.connect(DBClass.constring)
    cursor = cnxn.cursor()
    if(addoredit == 'Edit'):
        query = "Update picdata set pictitle = '"+pictitle+"', createddate = getdate(), imagepath = '"+imagepath+"' where Id= " +dataid
    else:
        query="insert into picdata ( Username, pictitle, createddate, nooflikes, imagepath) values ('" + username + "', '" + pictitle + "', getdate(), 1, '" + imagepath + "')"

    cursor.execute(query)
    cnxn.commit()


if __name__ == '__main__':
    app.run()