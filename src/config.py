# configuracion de la credenciales de la base de datos
db_config = {
    'dbname': 'siset',
    'user': 'postgres',
    'password': 'Asea2023',
    'host': 'localhost',
    'port': '5432'
    }

class Config:
    h=""
    
class DevelopmentConfig(Config):
    DEBUG = True
    
config = {
        'development':DevelopmentConfig
    }