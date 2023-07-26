from flask import Flask, request, jsonify
from flask_restful import Resource, Api  
import psycopg2 
app = Flask(__name__) 
api = Api(app)

@app.get('/')
def home():
    return "HELLO"



def create_con():
    conn = psycopg2.connect(
        host='10.197.194.126',
        port='5432',
        database='test',
        user='testuser',
        password='testpassword@1'
    )
    return conn


    # cursor = conn.cursor()

    # # Parse the data received from the Android app
    # data = request.get_json()
    # testval = data['testval']
    # cursor.execute("INSERT INTO test (testval) VALUES (%s)", (testval))
    # conn.commit()
    # cursor.close()
    # conn.close()

    # return 'Data received and stored successfully'



@app.route('/example', methods=['GET'])
def get():
    conn = create_con()
    cur = conn.cursor()
    cur.execute("SELECT * FROM androidconn")
    rows = cur.fetchall()
    cur.close()
    conn.close()


    results = []
    for row in rows:
        result = {'testval': row[0]}
        results.append(result)
    return jsonify(results), 200


@app.route('/example', methods=['POST'])
def post():
    data = request.get_json()
    testval = data.get('testval')
    conn = create_con()
    cur = conn.cursor()
    cur.execute("INSERT INTO androidconn (testval) VALUES (%s)", (testval,))
    conn.commit()
    cur.close()
    conn.close()

    return 'Data inserted successfully', 201


@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if 'number' in data:
        number = data['number']
        # Process the received number
        result = number * 2  # Example processing

        # Return a response
        response = {'result': result}
        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid request data'}), 400



#FOR MAIN TABLE
#
#
#



@app.route('/record', methods=['GET'])
def get_record():
    conn = create_con()
    cur = conn.cursor()
    cur.execute("SELECT * FROM heartbeatrecord")
    rows = cur.fetchall()
    cur.close()
    conn.close()


    results = []
    for row in rows:
        result = {'Uid': row[0], 'StartTimeHeartBeat': row[1], 'EndTimeHeartBeat': row[2], 'HeartBeatSample': row[3]}
        results.append(result)
    return jsonify(results), 200


@app.route('/record', methods=['POST'])
def post_record():
    data = request.get_json()
    Uid = data.get('Uid')
    StartTimeHeartBeat = data.get('StartTimeHeartBeat')
    EndTimeHeartBeat = data.get('EndTimeHeartBeat')
    HeartBeatSample = data.get('HeartBeatSample')
    conn = create_con()
    cur = conn.cursor()
    cur.execute('INSERT INTO heartbeatrecord ("Uid","StartTimeHeartBeat","EndTimeHeartBeat","HeartBeatSample") VALUES (%s, %s, %s, %s)', (Uid, StartTimeHeartBeat, EndTimeHeartBeat, HeartBeatSample,))
    # cur.execute("INSERT INTO androidconn (testval) VALUES (%s)", (Uid,))
    conn.commit()
    cur.close()
    conn.close()

    return 'Data inserted successfully', 201




#
#
#

# FOR TRIGGER CHECK
#
#

@app.route('/trigger', methods=['GET'])
def get_trigger_record():
    conn = create_con()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alertuser")
    rows = cur.fetchall()
    cur.close()
    conn.close()


    results = []
    for row in rows:
        result = {'Uid': row[0], 'StartTimeHeartBeat': row[1], 'EndTimeHeartBeat': row[2], 'HeartBeatSample': row[3], 'TimeStampOxy': row[4], 'OxySaturationValue': row[5]}
        results.append(result)
    return jsonify(results), 200

#
#
#




if '__name__' == '__main__':
    app.run()