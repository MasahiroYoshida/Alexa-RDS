import sys
import os
import logging
import pymysql 
import pymysql.cursors
import collections
from helper import convert
#rds settings

rds_host  = os.environ['db_host']
name = os.environ['db_username']
password = os.environ['db_password']
db_name = os.environ['db_name']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    logger.info("connect: {}".format(rds_host))
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def getFlight():
    """
    This function fetches content from MySQL RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        sql_select_query = "select count(*) from Flight"
        cur.execute(sql_select_query)
        for row in cur:

            logger.info(row[0])
            item_count = row[0]
            #print(row)
        
        cur.close()

    return "There is total {} flight avaiable".format(item_count)

def getFlightToSpecific(destination, start='Dallas'):
    item_count = 0

    with conn.cursor() as cur:
        #sanitization
        sql_select_query = """SELECT * FROM Flight WHERE Destination=%s and Start=%s"""
        cur.execute(sql_select_query, (destination, start, ))
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
        cur.close()

    return "There is {} flight avaiable from {} to {}".format(item_count, start, destination)

def getFlightToSpecificOnDate(departure, destination, start='Dallas'):
    item_count = 0

    with conn.cursor() as cur:
        #sanitization
        sql_select_query = """SELECT * FROM Flight WHERE Destination=%s and Start=%s and date(Date_of_departure)=%s"""
        cur.execute(sql_select_query, (destination, start, departure))
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
        cur.close()

    return "There is {} flight avaiable from {} to {} on {}".format(item_count, start, destination, departure)

def getRecentTicket(customer_id):
    start = "Dallas"
    destination = "Seattle"
    departure = "2019-05-22 10:12:00"
    item_count = 0
    with conn.cursor() as cur:
        #sanitization
        sql_select_query = """select * from Ticket, Flight where Customer_ID=%s and Ticket.Flight_ID=Flight.Flight_ID order by Date_of_departure desc"""
        cur.execute(sql_select_query, (customer_id,))
        for row in cur:
            row = convert(row)
            item_count += 1
            logger.info(row)
            print("Start: {}, Destination: {}, Date: {}".format(row["Start"], row["Destination"], row["Date_of_departure"]))
            start = row["Start"]
            destination = row["Destination"]
            departure = row["Date_of_departure"]
        cur.close()

    return "You currently have {} ticket. The most recent flight is from {} to {} on {}".format(item_count, start, destination, departure)


