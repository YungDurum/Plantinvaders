import os
from dotenv import load_dotenv


load_dotenv()

# Flask Mail and app config
class Config(object):
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PASS")
    SESSION_PERMANENT = False
    DATABASE = "sqlite:///moisture.db"

# Other email settings that i am not using currently
# app.config["RAGTIME_ADMIN"] = os.environ.get('RAGTIME_ADMIN')
# app.config["RAGTIME_MAIL_SUBJECT_PREFIX"] = 'Ragtime —'
# app.config["RAGTIME_MAIL_SENDER"] = 'Ragtime Admin <ragtime.flask@gmail.com'