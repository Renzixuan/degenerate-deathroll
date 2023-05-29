# db.py
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="deathroll_bets"
)

print(mydb)
mycursor = mydb.cursor()

async def record_bet(user, gold):
    print(f'User {user} has bet {gold} gold.')

async def check_ongoing_session():
    query = 'SELECT COUNT(*) FROM sessions WHERE ended_at IS NULL;'

    await mycursor.execute(query)
    result = await mycursor.fetchone()

    return result

async def create_new_session():
    return await check_ongoing_session()

    if session_ongoing == True:
        raise Exception("There's already a bet ongoing, cannot start a new one.")

    query = 'INSERT INTO sessions() VALUES();'
    await mycursor.execute(query)
    await mydb.commit()
    print(f'created new session, result: {result}')


async def end_session():
    # TODO 
    return
