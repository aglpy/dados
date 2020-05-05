import hashlib

def hasher(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def userify(d):
    table = {}
    if d:
        for user in d:
            table[user.get('player')] = user.get('password')
    return table

def get_user(t, p):
    for user in t:
        if user.get('player') == p:
            return user