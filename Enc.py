import random

key = [chr(i + ord('A')) for i in range(26)]
random.shuffle(key)

plain = input('')
plain = ''.join(plain.split(' '))
cipher=[]
for c in plain:
    cipher.append(key[ord(c)-ord('a')])

print((''.join(cipher)).upper())