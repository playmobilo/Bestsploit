import secrets
import db

database = db.Db()
database.new_api_key(secrets.token_hex(),'Akos')
