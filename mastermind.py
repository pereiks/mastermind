#!/usr/bin/python

import random
import time
import re 
import sys

TRIES = 12
COLOR_VARIATIONS = 6

def terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

def generate_new_code():
	global the_code
	the_code = str(random.randint(1,COLOR_VARIATIONS))+\
			str(random.randint(1,COLOR_VARIATIONS))+\
			str(random.randint(1,COLOR_VARIATIONS))+\
			str(random.randint(1,COLOR_VARIATIONS))

def check_attempt(guess,code):
	dup=''
	color_peg=0
	white_peg=0
	for pos,char in enumerate(guess):
		if char==code[pos]:
			color_peg+=1
			if not char in dup:
				dup+=char
	for pos,char in enumerate(guess):
		if char in code and char not in dup and char!=code[pos]:
			white_peg+=1
			dup+=char
	return (color_peg,white_peg,guess)

def game(mode,output):
	if output:
		print "Try to guess the combination of 4 digits (1-6)"
	attempt = 0
	guessed = False	
	result = []
	while guessed == False and attempt<=11:
		if mode=='a':
			the_guess=player_game(attempt)
		elif mode=='b':
			the_guess=five_move_algorithm(attempt,result)
		elif mode=='c':
			the_guess=custom_algorithm(attempt,result)
		result.append(check_attempt(the_guess,the_code))
		if result[attempt][0]==4:
			guessed = True
		if output:
			print ' ' * (terminal_size()[0]-1),'\r',
			print '| '  + the_guess+' | [ '+'\033[32m' + '*' * result[attempt][0] + \
				'\033[37m' + '*' * result[attempt][1] + \
				'\033[30m' + '*' * (4-result[attempt][0]-result[attempt][1]) + \
				'\033[37m ]'+' ' * 30 +'\033[40m'+'\033[37m'
		attempt+=1
	if guessed==True:
		return 0
	else:
		return -1


# TBD
def five_move_algorithm(attempt,result):
	global comp_db
	if attempt==0:
		for i in range(1111,6667):
			if re.match('^[123456]{4}$',str(i)):
				comp_db.append(i)
		return '1122'
	else:
		color_peg = result[attempt-1][0]
		white_peg = result[attempt-1][1]
		for item in comp_db:
			new_check = check_attempt(result[attempt-1][2],item)[0:2]
			if (color_peg,white_peg)!=new_check:
				comp_db_tmp.append(item)
		for item in comp_db_tmp:
			comp_db.remove(item)

def custom_algorithm(attempt,result):
	global comp_db
	comp_db_tmp=[]
	if attempt==0:
		for i in range(1111,6667):
			if re.match('^[123456]{4}$',str(i)):
				comp_db.append(str(i))
		return '1111'
	else:
		color_peg = result[attempt-1][0]
		white_peg = result[attempt-1][1]
		for item in comp_db:
			new_check = check_attempt(result[attempt-1][2],item)[0:2]
			if (color_peg,white_peg)!=new_check:
				comp_db_tmp.append(item)
		for item in comp_db_tmp:
			comp_db.remove(item)
		return comp_db[0]


def player_game(attempt):
	the_guess=raw_input("%i attempt: " %(attempt+1))
	while not re.match("^[1-6]{4}$",the_guess):
		print '\033[1A\r',' ' * (terminal_size()[0]-1),'\r',
		the_guess=raw_input("%i attempt: " %(attempt+1))
	print '\033[1A\r',' ' * (terminal_size()[0]-1),'\r',
	return the_guess


while True:
	the_code = ""
	comp_db = []
	print '\033[40m'+'\033[37m',' ' * (terminal_size()[0]-2),'\r',
	print "=== Welcome to MasterMind ==="
	print "Please choose game mode:"
	print "\ta) Player guesses\n\tb) Five-game algorithm\n\tc) custom algorithm\n\tx) Exit"
	mode = raw_input("Your input: ")
	while not re.match("^[abcx]{1}$",mode):
		print '\033[1A\r',' ' * (terminal_size()[0]-1),'\r',
		mode = raw_input("Your input: ")
	if mode=='x':
		print '\033[39m'+'\033[49m'
		sys.exit()
	elif mode!='a':
		repeat = raw_input("How many repeats: ")
		while not re.match("^[1-9][0-9]*$",repeat):
			print '\033[1A\r',' ' * (terminal_size()[0]-1),'\r',
			repeat = raw_input("How many repeats: ")
		repeat=int(repeat)
	else:
		repeat=1
	if mode == 'a' or mode == 'b' or mode== 'c':
		if repeat>1:
			output=False
			success=0
		else:
			output=True
		for i in range(0,repeat):
			generate_new_code()
			result = game(mode,output)
			if repeat==1:
				if result==-1:
					print "Out of tries!"
					print "the code was: %s" %the_code
				elif result==0:
					print "Congratulations!"
			else:
				if result==0:
					success+=1
				print "\r%i win from %i..." %(success,repeat),
				sys.stdout.flush()
			


