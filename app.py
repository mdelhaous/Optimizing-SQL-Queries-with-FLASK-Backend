from flask import Flask, render_template
from flask import request 
from gevent.pywsgi import WSGIServer
import time
import psycopg2
app = Flask("app")
from flask_cors import cross_origin
from flask import  jsonify


@app.route('/connectDB', methods=['POST'])
@cross_origin()
def connect_to_database():

    dbname = request.args.get('dbname')
    user = request.args.get('user')
    password = request.args.get('password')
    host = request.args.get('host')
    try:
        # Connect to the database
        conn = psycopg2.connect(dbname = dbname, user= user , password= password , host= host)
        if conn.status == 1:
            return jsonify(status = "connected")
        else :
            return jsonify(status = "NOT connected") 
            
    except psycopg2.Error as e:
        return f"An error occurred while connecting to the database: {e}"
    # finally:
    #     # # Close the connection
    #     # conn.close()




@app.route('/optiQuery', methods=['POST'])
@cross_origin()
def optimize_query():
    unoptimized_query = request.args.get('unoptimized_query')
                               # Connect to the database
    conn = psycopg2.connect(dbname="OPDB", user="postgres", password="12345", host="localhost")
    cursor = conn.cursor()
   

                          # Measure the time before running the query
    start_time = time.perf_counter()
 
                            # Execute the unoptimized query
    cursor.execute(unoptimized_query)
    # result = cursor.fetchall()
    if unoptimized_query.split()[0] == "SELECT":
        
        result = cursor.fetchall()
    else:
       
        conn.commit()

                            # Measure the time after running the query
    end_time = time.perf_counter()
    unoptimized_time = end_time - start_time

                              # Get the optimized query plan
    optimized_query="EXPLAIN " + unoptimized_query
    cursor.execute("EXPLAIN " + unoptimized_query)
    
    if unoptimized_query.split()[0] == "SELECT":
        optimized_query_plan = cursor.fetchall()
    else:
        optimized_query_plan=None

                           # Measure the time taken to execute the optimized query
    start_time = time.perf_counter()
    cursor.execute(unoptimized_query)

    if unoptimized_query.split()[0] == "SELECT":
        result = cursor.fetchall()
    else:
        result = None

    #result = cursor.fetchall()
    end_time = time.perf_counter()
    optimized_time = end_time - start_time

            

                                   # Close the cursor and connection
    cursor.close()
    conn.close()


    # return str(unoptimized_time)
    # return str(optimized_query,optimized_time,unoptimized_time)
    return jsonify(
        unoptimized_query = unoptimized_query,
        optimized_time = optimized_time,
        unoptimized_time = unoptimized_time,
        optimized_query = optimized_query,
        result = result
        )
        
if __name__ == '__main__':
    app.run(debug=True)
    