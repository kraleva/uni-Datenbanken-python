#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import subprocess
import csv
import validationFunctions
import parseTweet
import parseHashtags


query = 'INSERT into "user" (user_ID, name, screenName , location, url, description, protected, verified, followers, friends, listed, favourites, statuses, createdAt, defaultAcc, hobby1 , hobby2, isBrillenTrager) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
query1 = 'INSERT into "tweet" (tweet_ID, user_ID, createdAt , tweet) VALUES(%s, %s, %s, %s)'
query2 = 'INSERT into "following" (follower_ID, user_ID) VALUES(%s, %s)'

def readUserData(cur):
  with open('data/prj_user.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='`')
    i = 0
    normallength = 0
    for row in spamreader:
      if(len(row)<normallength):
        i+=1
        continue
      elif (i!=0):
        i+=1
        result = validationFunctions.validateRowUser(row)
        if(result):
          data = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],"","",row[7])
          cur.execute('SELECT * FROM "user" WHERE user_ID = %s',(row[0],))
          if(cur.rowcount==0):
            cur.execute(query,data)
            print("Is inserted");
      elif(i==0):
        #print(row)
        i+=1
        normallength=len(row)
    
def readTweetData(cur):
  with open('data/prj_tweet.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='`')
    i = 0
    normallength = 0
    for row in spamreader:
      if(len(row)<normallength):
        i+=1
        continue
      elif (i!=0):
        i+=1
        result = validationFunctions.validateRowTweet(cur,row)
        if(result):
          data = (row[0],row[1],row[2],row[3])
          cur.execute('SELECT * FROM "tweet" WHERE tweet_ID = %s',(row[0],))
          if(cur.rowcount==0):
            cur.execute(query1,data)
            parseTweet.parseTweet(row,cur);
            print("Is inserted");
      elif(i==0):
        i+=1
        normallength=len(row)

def readFollowingData(cur):
  with open('data/prj_following.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='`')
    i = 0
    normallength = 0
    for row in spamreader:
      if(len(row)<normallength):
        i+=1
        continue
      elif (i!=0):
        i+=1
        result = validationFunctions.validateRowFollowing(cur,row)
        if(result):
          #print(len(row))
          data = (row[0],row[1])
          cur.execute('SELECT * FROM "following" WHERE follower_ID = %s AND user_ID=%s',(row[0],row[1]))
          if(cur.rowcount==0):
            cur.execute(query2,data)
            print("Is inserted");
      elif(i==0):
        i+=1
        normallength=len(row)

def connect(start):
    """ Connect to the PostgreSQL database server """
    conn = None
    if(start):
        subprocess.call(['./init'])
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="minifb", user="viki", password="password")
        # create a cursor
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        # display the PostgreSQL database server version
        
        # close the communication with the PostgreSQL
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def connClose(conn):
  if conn is not None:
            conn.close()
            print('Database connection closed.')


def main():
    myconn = connect(True)
    readUserData(myconn)
    readTweetData(myconn)
    readFollowingData(myconn)
    parseHashtags.parseIterator(myconn)
    connClose(myconn)

if __name__ == '__main__':
    main()