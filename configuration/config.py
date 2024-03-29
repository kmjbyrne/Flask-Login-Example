import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"


#######################
###   CRYPTO KEYS   ###
#######################


SECRET_KEY = 'this is the application secret dEvElopmEnt kEy'
SECURITY_PASSWORD_SALT = 'this is the application secret dEvElopmEnt kEy'

#######################
### CONFIG SETTINGS ###
#######################

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = "c00170460@gmail.com"
MAIL_PASSWORD = 'itcarlowpassword'
MAIL_DEFAULT_SENDER = 'c00170460@gmail.com'

ADMINS = ['c00170460@gmail.com']

