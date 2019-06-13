import createDatabase
import re
import operator
from itertools import islice
import validationFunctions

def parseIterator(cur):
  query = 'SELECT user_ID,hobby1,hobby2,statuses   FROM "user";'
  cur.execute(query)
  user = cur.fetchone()
  conn = createDatabase.connect(False)
  while(user!=None):
    #print(user,user[3])
    hobbies = findHobbyUser(user[0],user[1],user[2],conn)
    user=cur.fetchone()
    #print(hobbies)
  createDatabase.connClose(conn)

def findHobbyUser(userID,hobby1,hobby2,conn):
  query = 'SELECT tweet  FROM "tweet" WHERE user_ID=%s;'
  conn.execute(query,(userID,))
  tweet = conn.fetchone()
  hobbies = {}
  while(tweet!=None):
    #print(tweet)
    parseHashtag(tweet,conn,hobbies)
    tweet=conn.fetchone()
  # maximum value
  if (len(hobbies)>1):
    print(hobbies.values())
    hobby = findMaxFromHashtag(hobbies)
    inserthobbies(hobby,userID,conn)
    print(hobby)
  elif(len(hobbies)==1):
    for key in hobbies.keys():
      hobby = [key,hobbies[key]]
    if(validationFunctions.validateString(hobby[0],32,False)):
      insertonehobby(hobby,userID,conn)
    else:
      return
  else:
    print("PROCESSING HOBBIES")
    return None
  return hobbies

def inserthobbies(hobby,userId,conn):
  query = 'UPDATE "user" SET (hobby1,hobby2) = (%s,%s) WHERE user_ID=%s;'
  conn.execute(query,(hobby[0][0],hobby[1][0],userId))
  print("Inserted hobby in DB")


def insertonehobby(hobby,userId,conn):
  query = 'UPDATE "user" SET  hobby1 = (%s) WHERE user_ID=%s;'
  conn.execute(query,(hobby[0],userId))
  print("Inserted hobby in DB")


def parseHashtag(tweet,cur,hobbies):
  regex = re.compile('#([\w\d]*)')
  result = regex.findall(str(tweet))
  #print(result)
  for i in range(len(result)):
    try: 
      hobbies[result[i]] += 1 

    except:
      #print("Hobby speichern")
      hobbies.update({result[i] : 1})
 
def findMaxFromHashtag(hobbies):
  hobby = [['',0],['',0]]
  print(hobbies)
  for key, value in hobbies.items():
            if ((value > hobby[0][1]) and validationFunctions.validateString(key,32,False)):
              hobby[0][0] = key
              hobby[0][1] = value
            else:
              if((value>hobby[1][1]) and validationFunctions.validateString(key,32,False)):
                hobby[1][0] = key
                hobby[1][1] = value
              else:
                continue
  return hobby
