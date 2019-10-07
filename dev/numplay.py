#!usr/bin/env

# homemade module for several useful number checks

def isprime(num):
    prime = True

    if isinstance(num, int) == False:
        raise TypeError('Expected input of type int')

    if (num % 2) == 0 and num != 2:
        prime = False

    elif num == 1:
        prime = False

    elif num == 2 or num == 3:
        prime = True

    else:
        root = int(num ** (1 / 2))

        while prime:
            for i in range(2, root+1):
                if (num % i) == 0:
                    prime = False
            break

    return prime

def allprimes(x):
	primes = []

	for i in range(1,x+1):
		if isprime(i):
			primes.append(i)

	return primes


def factorial(x):

	if isinstance(x, int) == False:
		raise TypeError('Expected input of type int')

	num = 1

	for i in range(2,x+1):
		num *= i

	return num

def factors(x):
	factors = []
	half = int(x/2) + 1

	for i in range(1,half):
		if (x%i) == 0:
			factors.append(i)

	factors.append(x)

	return factors

def primefactors(x):
	facs = factors(x)
	primes = []

	for fac in facs:
		if isprime(fac):
			primes.append(fac)

	return primes

def perfect(x):
	facs = factors(x)
	del facs[-1]

	total = sum(facs)

	if total == x:
		perf = 'Perfect'

	elif total < x:
		perf = 'Deficient'

	else:
		perf = 'Abundant'

	return perf

def fib(x):
	a,b = 0,1
	for i in range(x):
		a,b = b,a+b
	return b
    
# This is a test for Git




