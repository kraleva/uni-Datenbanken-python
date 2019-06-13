from urllib.parse import urlparse


def validateString(word,size,isemptyallowed):
  if(len(word)>size):
    return False
  elif (word=='' and isemptyallowed) :
    return True
  else: 
    return True

def validateUrl(url):
  o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
  if(o.netloc):
    return True
  return False

def validateDate(date):
  mydate = date.rsplit('-')
  if(len(mydate)!=3):
    return False
  year = mydate[0]
  month = int(mydate[1])
  day = int(mydate[2][0:2])
  if(year[0:3]!='200' and year[0:2]!='19' and year[0:3]!='201'):
    return False
  elif(month<0 or month>12):
    return False
  elif(day>31 or day<0):
    return False
  return True

def RepresentsInt(s):
    try: 
        b = int(s)
        return True
    except ValueError:
        return False

def validateBoolean(m):
  if(m=='True'):
    m = True
    return True
  elif(m=='False'):
    m = False
    return True
  return False


def validateRowUser(row):
  ids = RepresentsInt(row[0])
  name = validateString(row[1],32,False)
  screenname = validateString(row[2],32,False)
  location = validateString(row[3],50,True)
  url = validateUrl(row[4])
  protected = validateBoolean(row[6])
  verified = validateBoolean(row[7])
  followers = RepresentsInt(row[8])
  friends = RepresentsInt(row[9])
  listed = RepresentsInt(row[10])
  favourites = RepresentsInt(row[11])
  statuses = RepresentsInt(row[12])
  createdAt = validateDate(row[13])
  defaultAcc = validateBoolean(row[14])
  #print(ids,name,screenname,location,url,protected, createdAt, followers , verified, friends, listed, favourites, statuses, createdAt, defaultAcc)
#print(type(ids),type(name),type(screenname),type(location),type(url),type(protected), type(createdAt), type(followers) , type(verified), type(friends), type(listed), type(favourites), type(statuses), type(createdAt), type(defaultAcc))
  if(ids and name and screenname and location and url and protected and createdAt and verified  and friends and listed and followers and favourites and statuses and createdAt and defaultAcc):
    return True
  return False


def validateUserkey(cur,userkey):
  query = 'SELECT * FROM "user" WHERE user_ID = %s'
  cur.execute(query,(userkey,))
  if(cur.rowcount==0):
    return False
  if RepresentsInt(userkey):
    return True
  return False

def validateRowTweet(cur,row):
  ids = RepresentsInt(row[0])
  ids1 = validateUserkey(cur,row[1]);
  createdAt = validateDate(row[2])
  tweet = validateString(row[3],200,False)
 # print(ids,ids1,createdAt,tweet)
  if(ids and ids1 and createdAt and tweet):
    return True
  return False

def validateRowFollowing(cur,row):
  ids = validateUserkey(cur,row[0])
  ids1 = validateUserkey(cur,row[1]);
 # print(ids,ids1)
  if(ids and ids1):
    return True
  return False