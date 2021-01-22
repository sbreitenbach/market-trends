import logging

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.DEBUG)
##End Config##

def returns_true():
    return True

if __name__ == '__main__':
    print("Hello World!")
    print(returns_true())
    logging.info("Hello World!")