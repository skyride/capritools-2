import random, string

def random_key(length):
   return ''.join(random.choice(string.letters + string.digits) for i in range(length))
