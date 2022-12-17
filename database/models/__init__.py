from sqlalchemy.orm import declarative_base
Base = declarative_base()

def import_models():
    from .user import User
    from .address import Address

import_models()