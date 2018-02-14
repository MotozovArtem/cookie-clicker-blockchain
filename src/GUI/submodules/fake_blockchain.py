


def generate_block():
    import random
    import string
    hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    author = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
    comment = ''.join(random.choice(string.ascii_uppercase ) for _ in range(7))
    proof = str(random.randint(10,100))
    create_date = "12:04:54"
    prev_block = "184962b539823eb979a728f9d367e362322c9755"
    return {"hash": hash, "author": author, "comment": comment, "proof": proof, "create_date": create_date,
             "prev_block": prev_block}

def get_blockchain_info(n): #Эмуляция функции, которая должна вернуть информацию о блокчейне
    return [generate_block() for i in range(n)]
