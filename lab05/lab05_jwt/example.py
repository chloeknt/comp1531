import jwt

SECRET = 'comp1531'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.lBTAPFU1xxDAi2Vrusfo67ypBai0vBr6O7KOt6CJf1s'

print(jwt.decode(TOKEN, SECRET, algorithms=['HS256']))