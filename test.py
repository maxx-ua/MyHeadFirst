from DBcm import UseDatabase

dbconfig = { 'host': '127.0.0.1',
	     'user': 'vs',
	     'password': 'vsearchpasswd',
	     'database': 'vsearchlogDB', }


with UseDatabase(dbconfig) as cursor:
	sql = """insert into log
			(phrase, letters, ip, browser_string, results)
			values
			(%s, %s, %s, %s, %s)"""
	cursor.execute(sql, (req.form['phrase'],
						 req.form['letters'],
						 req. remote_addr,
						 req.user_agent.browser,
						 res, ))
