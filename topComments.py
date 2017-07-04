import csv
import praw
import json
import time
import MySQLdb

# Credentials to access the Reddit API
reddit = praw.Reddit(client_id='vgr0He3IMlSqVA',
                     client_secret='h0WAu-6F6cQsx3Ku0DcC9gtld24',
                     user_agent='by /u/ExtractAccount',
                     username='ExtractAccount',
                     password='reddit12345')

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="Luster218!",
                     db="donaldcomments")

cur = db.cursor();
db.set_character_set('utf8mb4')
cur.execute('SET NAMES utf8mb4;')
cur.execute('SET CHARACTER SET utf8mb4;')
cur.execute('SET character_set_connection=utf8mb4;')
print(cur.execute("SELECT * FROM comments"))

# Extract only 25 post from the front page
topPosts = []
for submission in reddit.front.hot(limit=25):
  topPosts.append(submission)

def addDonaldComments(comment):
  int_time = int(comment.created)
  date = time.strftime('%Y-%m-%d', time.localtime(int_time))
  try:
    cur.execute("INSERT INTO comments (id,author,body,created,score) VALUES (NULL, %s, %s, %s, %s)", (comment.author, str(comment.body) , date, str(comment.score)))
  except:
    cur.execute("INSERT INTO comments (id,author,body,created,score) VALUES (NULL, %s, %s, %s, %s)", (comment.author, str(comment.body)[0:1000] , date, str(comment.score)))


# Extract all comments from the front page submissions
for sub in topPosts:
  submission = reddit.submission(id=sub)
  submission.comments.replace_more(limit=0)
  for comment in submission.comments.list():
    if "donald" in comment.body.lower() or "trump" in comment.body.lower():
      addDonaldComments(comment) 


db.commit()
cur.close()
db.close()
