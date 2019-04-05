from flask import Flask,request,render_template
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from werkzeug.datastructures import ImmutableMultiDict
import matplotlib.pyplot as plt



app = Flask(__name__)

@app.route('/we',methods=['GET', 'POST'])
def test():
    data = request.data
    connection = sqlite3.connect("DSS_stats.db")
    cursor = connection.cursor()
    cursor.execute("select distinct host from lpnlog")
    arr_hosts = cursor.fetchall()
    dateFrameArray = []
    print(arr_hosts)
    for ip in arr_hosts:
        connection = sqlite3.connect("DSS_stats.db")
        cursor = connection.cursor()
        print("SELECT * from lpnlog where host = '{}' ".format(ip[0]))
        cursor.execute("SELECT * from lpnlog where host = '{}' order by ts ".format(ip[0]))
        dataChunk = cursor.fetchall()
        res = pd.DataFrame(data=dataChunk,
                           columns=['id', 'host', 'pass_id', 'lpn', 'ts', 'logdt', 'passdt', 'delay', 'recvol'])
        # res.fillna(0)

        values = {'pass_id': 0, 'recvol': 0, 'delay': 0}
        res = res.fillna(value=values)

        # res['id'] = res['id']+1

        res['id'] = res['id'].astype('int64')
        res['host'] = res['host'].astype('object')
        res['pass_id'] = res['pass_id'].astype('int64')
        res['lpn'] = res['lpn'].astype('str')
        res['ts'] = pd.to_datetime(res['ts'])
        res['logdt'] = pd.to_datetime(res['logdt'])
        res['passdt'] = pd.to_datetime(res['passdt'])
        res['delay'] = res['delay'].astype('int64')
        res['recvol'] = res['recvol'].astype('int64')

        print(res.head())

        res = res[res.ts.notnull()]

        dateFrameArray.append(res)
        print(len(dateFrameArray))
    fig = plt.figure(num=None, figsize=(15, 8), dpi=120, facecolor='w', edgecolor='k')
    '''
    x = dateFrameArray[5]['ts']
    y = dateFrameArray[5]['delay']
    plt.plot(x,y)
    '''

    for data in dateFrameArray:
        print(data.head())

        print("=========")

        x = data['ts']
        y = data['delay']
        plt.plot(x, y)

    plt.legend(['y = x', 'y = 2x', 'y = 3x', 'y = 4x'], loc='upper left')
    plt.savefig('foo.png')
    #plt.show()
    

    #return  send_file("foo.png", mimetype='image/gif')


    return render_template("index.html", picture="foo.png")




@app.route('/select_all', methods=['GET', 'POST'])
def select_all():
    connection = sqlite3.connect("DSS_stats.db")
    cursor = connection.cursor()
    cursor.execute("select * from lpnlog")
    #cursor.execute("select distinct host from lpnlog")
    data = cursor.fetchall()
    #data = cursor.fetchall()

    res = pd.DataFrame(data=data,
                       columns=['id', 'host', 'pass_id', 'lpn', 'ts', 'logdt', 'passdt', 'delay', 'recvol'])
    values = {'pass_id': 0, 'recvol': 0, 'delay': 0}
    res = res.fillna(value=values)

    # res['id'] = res['id']+1

    res['id'] = res['id'].astype('int64')
    res['host'] = res['host'].astype('object')
    res['pass_id'] = res['pass_id'].astype('int64')
    res['lpn'] = res['lpn'].astype('str')
    res['ts'] = pd.to_datetime(res['ts'])
    res['logdt'] = pd.to_datetime(res['logdt'])
    res['passdt'] = pd.to_datetime(res['passdt'])
    res['delay'] = res['delay'].astype('int64')
    res['recvol'] = res['recvol'].astype('int64')
    print(res.head().to_string())
    print("========")
    #print(res.to_string())
    #res = res.to_string()


    return render_template('select_all.html', title='select_all', result=list(res.columns.values))


    #return 'qwe'



@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)



@app.route('/part_sql',methods = ['POST', 'GET'])
def part_sql():
    if request.method == 'POST':
        result = request.form
        data = result.getlist('col')
        connection = sqlite3.connect("DSS_stats.db")
        cursor = connection.cursor()
        cursor.execute("select host,{},{} from lpnlog".format(data[0],data[1]))
        for d in data:
            if d == 'ts' or d == 'lpn' or d == 'logdt' or d=='passdt':
                print(d)
        # cursor.execute("select distinct host from lpnlog")
        info = cursor.fetchall()
        print(info)
        x= []
        y = []
        for inf in info:
            x.append(inf[1])
            y.append(inf[2])
        print(x)
        print(y)
        plt.plot(x, y, label='linear')
        plt.show()
    return '23we'



if __name__ == '__main__':
    #app.run(host="192.168.30.83", port=5000)


    app.run(host="127.0.0.1", port=5000)