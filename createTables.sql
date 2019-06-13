CREATE TABLE "user" ( 
    user_ID BIGSERIAL primary key, 
    name varchar(32) NOT NULL,
    screenName varchar(32) NOT NULL,
    location varchar(50),
    url text,
    description text,
    protected boolean NOT NULL,
    verified boolean NOT NULL,
    followers int NOT NULL,
    friends int NOT NULL,
    listed int NOT NULL,
    favourites int NOT NULL,
    statuses int NOT NULL,
    createdAt TIMESTAMP,
    defaultAcc boolean NOT NULL,
    hobby1 varchar(32),
    hobby2 varchar(32),
    isBrillenTrager boolean NOT NULL);

CREATE TABLE "following" ( 
    follower_ID BIGSERIAL,
    user_ID BIGSERIAL, 
  PRIMARY KEY (Follower_ID,User_ID), 
  FOREIGN KEY (User_ID) REFERENCES "user"(user_ID),
  FOREIGN KEY (Follower_ID) REFERENCES "user"(user_ID));

CREATE TABLE "tweet" ( 
      tweet_ID BIGSERIAL NOT NULL primary key,
      user_ID BIGSERIAL NOT NULL, 
      createdAt date,
      tweet VARCHAR(280),
  FOREIGN KEY(User_ID) REFERENCES "user"(user_ID));
 
CREATE TABLE "relationship" (
  user1_ID BIGSERIAL NOT NULL,
  user2_ID BIGSERIAL NOT NULL,
  user1_retweetTimes INT NOT NULL,
  user2_retweetTimes INT NOT NULL,
  typeOfRelationship varchar(32) NOT NULL,
  PRIMARY KEY(user1_ID,user2_ID),
  FOREIGN KEY(user1_ID) REFERENCES "user"(user_ID),
  FOREIGN KEY(user2_ID) REFERENCES "user"(user_ID));
