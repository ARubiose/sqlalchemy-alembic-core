# Database connections from config
from database.config import automapped_database, declarative_database

from database.models.user import User
from database.models.address import Address
from database.models.role import Role

# Do something with the database
print(automapped_database.base.classes.keys())
print(declarative_database.base.metadata.tables.keys())

# Insert a user and his address opening a session
with declarative_database.session as session:
    # Add Role
    role:Role = Role(name='admin', description='Administrator')
    session.add(role)
    session.flush() # Flush to get role.id
    # Add user
    user:User = User(name='Alvaro', fullname='Rubios', password='admin', role_id=role.id)
    session.add(user)
    session.flush() # Flush to get user.id
    # # Add address
    address:Address = Address( address='123 Main', user_id=user.id)
    session.add(address)
    # Commit changes
    session.commit()
