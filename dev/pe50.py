#!usr/bin/env

# Project Euler #50

from numplay import *

a = 0                        
count = 0
prime_count = 0
goal = 1000

while a < final:
	count += 1

	if isprime(count):
		if a + count >= final:
			break

		a += count
		if isprime(a):
			prime = a

print(prime)
