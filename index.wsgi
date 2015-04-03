import sys

from flask import Flask

sys.path.append('/var/www/flask')

application = Flask(__name__)

application.config['SECRET_KEY'] = 'SECRET_KEY'

#----------------------------------------------------------
# logging
#----------------------------------------------------------
import logging
logging.basicConfig(stream=sys.stderr)

#----------------------------------------------------------
# Sample application
#----------------------------------------------------------
from app_sample import views as views_sample
application.register_blueprint(views_sample.blueprint, url_prefix="/sample")

#----------------------------------------------------------
# for Debug
#----------------------------------------------------------
if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
