import os


app_root = os.path.dirname(os.getcwd())

class Config(object):
    DEBUG = False


class LocalConfig(Config):
    DEBUG = True

    RESULT_PATH = "app/result.json"

class DevelopmentConfig(Config):
    DEBUG = True

    RESULT_PATH = "app/result.json"
    #SERVER_NAME = "localhost:5000"
    
class ProductionConfig(Config):
    DEBUG = False

    RESULT_PATH = "app/result.json"
    