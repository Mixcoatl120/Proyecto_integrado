class Config:
    SECRET_KEY = 'Jvm2OrrMd4QaRNHzvtgqfxyLir8'

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = 'localhost'
    USER = 'postgres'
    PASSWORD = 'Asea2023'
    DB = 'users'
    


config = {
        'development':DevelopmentConfig
    }