#!usr/bin/env

from numplay import *

test = 'Unit test failed'

if isprime(2) and isprime(3) and isprime(7):
	if not isprime(1) and not isprime(4):
		if factors(factorial(5)) == [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120]:
			if primefactors(factorial(5)) == [2,3,5]:
				if perfect(28) == 'Perfect' and perfect(24) == 'Abundant':
					if fib(10) == 89:
						test = 'Unit test passed'

print(test)




