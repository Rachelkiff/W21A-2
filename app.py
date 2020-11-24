from flask import Flask, request, Response
import mariadb
import dbcreds
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/api/bloggers", methods =["GET", "POST", "PATCH", "DELETE"])
def bloggers():
    if request.method == "GET":
      conn = None
      cursor = None 
      bloggers = None 
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blogger")
        bloggers = cursor.fetchall()
      except Exception as error:
        print("Something went wrong(This is LAZY!): ")
        print(error)   
      finally:
        if(cursor != None):
         cursor.close()
        if(conn != None):
         conn.rollback()
         conn.close()
        if(bloggers != None):
            return Response(json.dumps(bloggers, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong.", mimetype="text/html", status=500)  
    elif request.method == "POST": 
      conn = None
      cursor = None 
      blogger_username = request.json.get("username")
      blogger_content = request.json.get("content")
      blogger_created_at = request.json.get("created_at")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO blogger(username, content, created_at) VALUES (?, ?, ?)", [blogger_username, blogger_content, blogger_created_at,])
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong(This is LAZY!): ")
        print(error)   
      finally:
       if(cursor != None):
         cursor.close()
       if(conn != None):
         conn.rollback()
         conn.close()
       if(rows == 1):
          return Response("Blog Post has been posted!", mimetype="text/html", status=201)
       else:
          return Response("Something went wrong!", mimetype="text/html", status=500)   
    elif request.method == "PATCH":
      conn = None
      cursor = None 
      blogger_username = request.json.get("username")
      blogger_content = request.json.get("content")
      blogger_created_at = request.json.get("created_at")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        if blogger_username != "" and blogger_username != None:
           cursor.execute("UPDATE blogger SET username=? WHERE id=?", [blogger_username, blogger_id])
        if blogger_content != "" and blogger_content != None:
            cursor.execute("UPDATE blogger SET content=? WHERE id=?", [blogger_content, blogger_id])
        if blogger_created_at != "" and blogger_created_at != None:
            cursor.execute("UPDATE blogger SET created_at=? WHERE id=?", [blogger_created_at, blogger_id])      
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong(This is LAZY!): ")
        print(error)     
      finally:
       if(cursor != None):
         cursor.close()
       if(conn != None): 
         conn.rollback()
         conn.close()
       if(rows == 1):
          return Response("Blog Updated Successfully!", mimetype="text/html", status=204)
       else:
          return Response("Something went wrong!", mimetype="text/html", status=500)  
    elif request.method == "DELETE":
      conn = None
      cursor = None 
      blogger_id = request.json.get("id")
      rows = None
      try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database,)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blogger WHERE id=?", [blogger_id,])   
        conn.commit()
        rows = cursor.rowcount
      except Exception as error:
        print("Something went wrong(This is LAZY!): ")
        print(error)     
      finally:
       if(cursor != None):
         cursor.close()
       if(conn != None):
         conn.rollback()
         conn.close()
       if(rows == 1):
          return Response("Deleted Blog post Successfully!", mimetype="text/html", status=204)
       else:
          return Response("Delete Failed!", mimetype="text/html", status=500)                      