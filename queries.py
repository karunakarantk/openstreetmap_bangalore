"""
Queries on bengaluru.db
"""

import csv, sqlite3

# Queries as functions to be called at the end. Will be printed to the terminal
# when this script is run.
def number_of_nodes():
	result = cur.execute('SELECT COUNT(*) FROM nodes')
	return result.fetchone()[0]

def number_of_ways():
	result = cur.execute('SELECT COUNT(*) FROM ways')
	return result.fetchone()[0]

def number_of_unique_users():
	result = cur.execute('SELECT COUNT(DISTINCT(allusers.uid)) \
            FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) allusers')
	return result.fetchone()[0]

def common_ammenities():
	for row in cur.execute('SELECT value, COUNT(*) as num \
            FROM nodes_tags \
            WHERE key="amenity" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10'):
		return row

def common_ammenities_2():
	for row in cur.execute('SELECT value, COUNT(*) as num \
            FROM nodes_tags \
            WHERE key="leisure" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10'):
		return row

def top_contributing_users():
	users = []
	for row in cur.execute('SELECT allusers.user, COUNT(*) as num \
            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) allusers \
            GROUP BY allusers.user \
            ORDER BY num DESC \
            LIMIT 10'):
		users.append(row)
	return users

def number_of_users_contributing_once():
	result = cur.execute('SELECT COUNT(*) \
            FROM \
                (SELECT allusers.user, COUNT(*) as num \
                 FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) allusers \
                 GROUP BY allusers.user \
                 HAVING num=1) u')
	return result.fetchone()[0]

if __name__ == '__main__':
	
	con = sqlite3.connect("bengaluru.db")
	cur = con.cursor()
	
	print "Number of nodes: " , number_of_nodes()
	print "Number of ways: " , number_of_ways()
	print "Number of unique users: " , number_of_unique_users()
	print "Top contributing users: " , top_contributing_users()
	print "Number of users contributing once: " , number_of_users_contributing_once()
	print "Common ammenities: " , common_ammenities()
	print "Biggest religion: " , common_ammenities_2()
    