import redis

def main():
    pool = redis.StrictRedis(host='localhost', port=6379, db=0)
    print(pool.get('0'))

main()
