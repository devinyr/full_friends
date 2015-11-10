from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector

app = Flask(__name__)

app.secret_key = "thisisasecretkey"

mysql = MySQLConnector('friendsdb')

def find_friend(id):
	friends = mysql.fetch("SELECT * FROM friends")
	for friend in friends:
		print friend['first_name']
		print friend['id']
		if friend['id'] == int(id):
			print id
			return friend
	return False

def delete_friend(id):
	return False

@app.route('/', methods=['GET'])
def index():
	friends = mysql.fetch("SELECT * FROM friends")
	print friends
	return render_template('index.html', friends=friends)

@app.route('/friends', methods=['POST'])
def create():
	print request.form['last_name']
	sqlstr = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES ('{}','{}', '{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['occupation'])
	print sqlstr
	mysql.run_mysql_query(sqlstr)
	return redirect('/')

@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
	print id
	friend = find_friend(id)
	if friend:
		return render_template('edit.html', friend=friend)
	return redirect('/')

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	print "updating"
	print id
	print request.form
	sqlstr = "UPDATE friends SET first_name = '{}', last_name = '{}', occupation = '{}', updated_at = NOW() WHERE id = {}".format(request.form['first_name'], request.form['last_name'], request.form['occupation'] ,id)
	print sqlstr
	mysql.run_mysql_query(sqlstr)
	return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
	print "deleting"
	print id
	sqlstr = "DELETE FROM FRIENDS WHERE id = {}".format(id)
	print sqlstr
	mysql.run_mysql_query(sqlstr)
	return redirect('/')


app.run(debug = True)


