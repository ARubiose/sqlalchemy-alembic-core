# Database connections from config
from database.config import automapped_database, declarative_database

from database.models.user import User
from database.models.address import Address

# Do something with the database
print(automapped_database.base.classes.keys())
print(declarative_database.base.metadata.tables.keys())

# Insert a user and his address opening a session
with declarative_database.session as session:
    # Add user
    user:User = User(name='John', fullname='John Doe', password='password')
    session.add(user)
    session.flush() # Flush to get user.id
    # Add address
    address:Address = Address( address='123 Main', user_id=user.id)
    session.add(address)
    # Commit changes
    session.commit()
