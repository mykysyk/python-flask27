PATH        = '/var/www/flask'

class Config(object):

    DEBUG       = False
    TESTING     = False
    CHARSET     = 'utf-8'

class ConfigSample(Config):

    CHARSET     = 'utf-8'
    SQLITE3     = PATH + '/app_sample/database.sqlite3'
    TEMPLATE_D  = PATH + '/app_sample/templates/'
    #TEMPLATE_C = PATH + '/app_sample/templates/cache'
    TEMPLATE_C  = None

app_sample = ConfigSample
