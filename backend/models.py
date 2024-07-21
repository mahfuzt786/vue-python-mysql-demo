from flask_mysqldb import MySQL
import MySQLdb  # Import MySQLdb for error handling
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()

class User:
    @staticmethod
    def create_user(name, email, password, address=None, contact_number=None, role='user'):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, password, address, contact_number, role) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, email, hashed_password, address, contact_number, role))
            mysql.connection.commit()
            cur.close()
        except MySQLdb.IntegrityError as error:
            if error.args[0] == 1062:  # Duplicate entry error
                return False
            else:
                raise error
        return True

    @staticmethod
    def get_user_by_email(email):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def get_user_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def get_all_users():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return users

    @staticmethod
    def delete_user(user_id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user[3], password)  # user[3] is the password field


class SecurityTransaction:
    @staticmethod
    # def get_combined_transactions(page, per_page, from_date, to_date, portfolio_number, share_symbol, security_currency):
    def get_combined_transactions(from_date, to_date, portfolio_number, share_symbol, security_currency):
        cur = mysql.connection.cursor()
        # offset = (page - 1) * per_page

        query = """
        SELECT 
            st.`TRADE_DATE` AS TRADE_DATE,
            st.`SECURITY_ACCOUNT` AS SECURITY_ACCOUNT,
            sam.`ACCOUNT_NAME` AS SAM_NAME,
            st.`SECURITY_NUMBER` AS SECURITY_NUMBER,
            sm.`SHORT_NAME` AS SECURITY_NAME,
            st.`TRANS_TYPE` AS TRANS_TYPE,
            st.`RECID` AS RECID,
            st.`NO_NOMINAL` AS NO_NOMINAL,
            st.`PRICE` AS PRICE,
            st.`NET_AMT_TRADE` AS NET_AMT_TRADE,
            st.`BROKER_COMMS` AS BROKER_COMMS,
            st.`PROF_LOSS_SEC_CCY` AS PROF_LOSS_SEC_CCY
        FROM 
            SECURITY_TRANSACTIONS st
        LEFT JOIN 
            SEC_ACC_MASTER sam ON st.`SECURITY_ACCOUNT` = sam.`RECID`
        LEFT JOIN 
            SECURITY_MASTER sm ON st.`SECURITY_NUMBER` = sm.`YSM.ID`
        WHERE 
            (%s IS NULL OR st.`TRADE_DATE` >= %s) AND
            (%s IS NULL OR st.`TRADE_DATE` <= %s) AND
            (%s IS NULL OR st.`SECURITY_ACCOUNT` = %s) AND
            (%s IS NULL OR st.`SECURITY_NUMBER` = %s) AND
            (%s IS NULL OR st.`SECURITY_CURRENCY` = %s)
        """
        # LIMIT %s OFFSET %s;
        # """
        
        
        # params = [from_date, from_date, to_date, to_date, portfolio_number, portfolio_number, share_symbol, share_symbol, security_currency, security_currency, per_page, offset]
        params = [from_date, from_date, to_date, to_date, portfolio_number, portfolio_number, share_symbol, share_symbol, security_currency, security_currency]
        
        cur.execute(query, params)
        transactions = cur.fetchall()

        # Get the total count of records for pagination
        count_query = """
        SELECT COUNT(*) 
        FROM SECURITY_TRANSACTIONS st
        LEFT JOIN 
            SEC_ACC_MASTER sam ON st.`SECURITY_ACCOUNT` = sam.`RECID`
        LEFT JOIN 
            SECURITY_MASTER sm ON st.`SECURITY_NUMBER` = sm.`YSM.ID`
        WHERE 
            (%s IS NULL OR st.`TRADE_DATE` >= %s) AND
            (%s IS NULL OR st.`TRADE_DATE` <= %s) AND
            (%s IS NULL OR st.`SECURITY_ACCOUNT` = %s) AND
            (%s IS NULL OR st.`SECURITY_NUMBER` = %s) AND
            (%s IS NULL OR st.`SECURITY_CURRENCY` = %s)
        """

        # cur.execute(count_query, params[:-2])
        cur.execute(count_query, params)
        total = cur.fetchone()[0]
        
        cur.close()

        return transactions, total




