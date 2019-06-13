import re
import createDatabase

def parseTweet(row,cur):
  getOriginalUserID(row,cur)

def getOriginalUserID(row,cur):
  regex = re.compile('^RT .*$')
  tweet = row[3]
  result = regex.search(tweet)
  if result == None:
    #print(result.group(1))
    return
  else:
    regex = re.compile('@([\w\d]*)')
    try:
      result = regex.search(tweet)
      username = result.group(1)
      findOriginalUserId(username,cur,row)
    except:
      print("OOPS,FEHLERHAFTE DATAAA")
  #tweet = result.

def findOriginalUserId(screenName,cur,row):
  result = cur.execute('SELECT * FROM "user" WHERE screenName = %s',(screenName,))
  helper = cur.fetchone()
  print(helper)
  if helper:
    #id of the original tweets,id of the retweeter is row[1]
    result = helper[0]
    query = 'SELECT * FROM "relationship" WHERE user1_ID=%s AND user2_ID=%s OR user1_ID=%s AND user2_ID=%s'
    cur.execute(query,(result,row[1],row[1],result))
    if (cur.rowcount > 0): 
      result1 = cur.fetchone()
      print(result1)
      lookwhatToIncrement(result1,cur,result,row[1])
    else :
      query1 = 'INSERT into "relationship" (user1_ID, user2_ID, user1_retweetTimes,user2_retweetTimes,typeOfRelationship) VALUES(%s, %s, %s, %s, %s) RETURNING user1_ID;'
      data = (row[1],result,1,0,'Single')
      cur.execute(query1,data)
      print("INSERTED RELATIONSHIP")

def lookwhatToIncrement(relationShipEntity,cur,originalUserId,userId):
  userId = int(userId)
  originalUserId = int(originalUserId)
  user1_ID = relationShipEntity[0]
  user2_ID = relationShipEntity[1]
  user1_retweetTimes = int(relationShipEntity[2])
  user2_retweetTimes = int(relationShipEntity[3])
  typeOfRelationship = relationShipEntity[4]
  print(user2_ID==userId,type(user2_ID),type(userId))
  if(userId == user2_ID and int(user1_retweetTimes)==1 and int(user2_retweetTimes)==0):
    query1 = 'UPDATE "relationship" SET (user1_retweetTimes, user2_retweetTimes,typeOfRelationship) = (%s,%s,%s) WHERE user1_ID=%s AND user2_ID=%s;'
    data = (user1_retweetTimes,user2_retweetTimes+1,'Date',user1_ID,user2_ID)
    cur.execute(query1,data)
    print("Fall1 Ready")
  elif(userId ==user1_ID and int(user1_retweetTimes)==1 and int(user2_retweetTimes)==2):
    query1 = 'UPDATE "relationship" SET (user1_retweetTimes,user2_retweetTimes,typeOfRelationship) = (%s,%s,%s) WHERE user1_ID=%s AND user2_ID=%s;'
    data = (user1_retweetTimes+1,user2_retweetTimes,'Married',user1_ID,user2_ID)
    cur.execute(query1,data)
    print('Fall2 Ready')
  elif(userId ==user2_ID and int(user2_retweetTimes)==1 and int(user1_retweetTimes)==2):
    query1 = 'UPDATE "relationship" SET (user1_retweetTimes,user2_retweetTimes,typeOfRelationship) = (%s,%s,%s) WHERE user1_ID=%s AND user2_ID=%s;'
    data = (user1_retweetTimes,user2_retweetTimes+1,'Married',user1_ID,user2_ID)
    cur.execute(query1,data)
    print('Fall3 Ready')
  else:
    if(userId==user2_ID):
      query1 = 'UPDATE "relationship" SET (user1_retweetTimes,user2_retweetTimes,typeOfRelationship) = (%s,%s,%s) WHERE user1_ID=%s AND user2_ID=%s;'
      data = (user1_retweetTimes,user2_retweetTimes+1,typeOfRelationship,user1_ID,user2_ID)
      cur.execute(query1,data)
      print('Fall4.1 Ready')
    else:
      query1 = 'UPDATE "relationship" SET (user1_retweetTimes,user2_retweetTimes,typeOfRelationship) = (%s,%s,%s) WHERE user1_ID=%s AND user2_ID=%s;'
      data = (user1_retweetTimes+1,user2_retweetTimes,typeOfRelationship,user1_ID,user2_ID)
      cur.execute(query1,data)
      print('Fall 4.2 ready')