# db.py
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="deathroll_bets"
)

mycursor =  mydb.cursor()

def record_bet(user, gold):
    ongoing_session_id = get_ongoing_session()

    if should_accept_bet(user, gold, ongoing_session_id):
        query = f'INSERT INTO bets(session_id, person_id, bet_amount) VALUES({ongoing_session_id}, \'{user}\', {gold});'
        mycursor.execute(query)
        mydb.commit()
    

def should_accept_bet(user, gold, session_id):
    mycursor.execute(f'SELECT COUNT(*) FROM bets WHERE person_id = \'{user}\' AND session_id = {session_id};')
    existing_bets = int(mycursor.fetchone()[0])

    if existing_bets > 0:
        raise Exception(f'You have already placed bets, cannot place another!')

    mycursor.execute(f'SELECT amount FROM sessions WHERE id = {session_id};')
    cap = int(mycursor.fetchone()[0])
     
    mycursor.execute(f'SELECT SUM(bet_amount) FROM bets WHERE session_id = {session_id};')
    result = mycursor.fetchone()[0]
    current_bet_total = 0
    if result:
        current_bet_total = int(result)

    if int(gold) + current_bet_total > cap:
        raise Exception(f'Bet amount has exceeded cap of {cap}, max bet amount now is {cap - current_bet_total} gold.')

    return True
    
def get_ongoing_session():
    query = 'SELECT id FROM sessions WHERE ended_at IS NULL;'

    mycursor.execute(query)
    result = mycursor.fetchone()
    
    if not result:
        raise Exception("There's no ongoing betting.")

    session_id = result[0]

    return session_id

def check_ongoing_session():
    query = 'SELECT COUNT(*) FROM sessions WHERE ended_at IS NULL;'
    
    mycursor.execute(query)
    sessions_count = mycursor.fetchone()[0]

    return int(sessions_count) > 0

def create_new_session(pool_amount):
    ongoing_session = check_ongoing_session()
    if ongoing_session is True:
        raise Exception("There's already a bet ongoing, cannot start a new one.")

    query = f'INSERT INTO sessions(amount) VALUES({pool_amount});'
    mycursor.execute(query)
    mydb.commit()


def end_session_and_get_results():
    ongoing_session = get_ongoing_session()

    # Update session end time
    mycursor.execute(f'UPDATE sessions SET ended_at = CURRENT_TIMESTAMP WHERE id = {ongoing_session};')
    mydb.commit()

    # Get all participants of the betting session
    mycursor.execute(f'SELECT person_id, bet_amount FROM bets WHERE session_id = {ongoing_session};')
    result = mycursor.fetchall()

    return result

