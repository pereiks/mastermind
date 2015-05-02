#!/usr/bin/python

import random

the_number = random.randint(1,1000000)
the_guess = 0
print "Try guessing a number from 1 to 1 million in 20 moves!"
print "I will help ypu a bit: when you guess, I will tell you if my number is greater or smaller than your guess!"
moves=20
guessed=False
while guessed=False or moves==0:
	moves-=1
	try: 
	#	the_guess = int(raw_input('Give me the number: '))
	except ValueError:
		print "Not a Number"
		the_guess = 0
		continue
	if the_guess<the_number:
		print "My number is GREATER than yours!"
	elif the_guess>the_number:
		print "My number is SMALLER than yours!"
	elif the_guess==the_number:
		print "YES! You are right!" 
		guessed=True
