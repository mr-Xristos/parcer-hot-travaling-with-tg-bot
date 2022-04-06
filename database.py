import psycopg2
import creds

conn = psycopg2.connect(host = creds.host,
                        dbname = creds.database,
                        user = creds.user,
                        password = creds.password)

cur = conn.cursor()

# id
# user_id
# username
# first_name
# last_name
# costables
# countryee
# days

# cur.execute(f"CREATE TABLE users (id SERIAL PRIMARY KEY, user_id TEXT, username text,"
#             f"first_name text, last_name text, costables text, countryee text, days text);")
# conn.commit()

def set_users(user_id, username, first_name, last_name):
    cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    data = cur.fetchone()
    if data is None:
        cur.execute(f"INSERT INTO users (user_id, username, first_name, last_name) "
                f"VALUES ('{user_id}', '{username}', '{first_name}', '{last_name}');")
        conn.commit()