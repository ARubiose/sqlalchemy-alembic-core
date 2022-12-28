# Database connections from config
from database.config import database 

# ORM models
from database.models.user import User
from database.models.address import Address
from database.models.role import Role

def insert_to_database():
    """Insert data to database"""
    print(database.base.metadata.tables.keys())

    with database.session as session:
        # Add Role or get it if exists
        role:Role = Role(name='admin', description='Administrator')
        session.add(role)
        session.flush() # Flush to get role.id
        # Add user
        user:User = User(name='Juanfran', fullname='Rubios', password='admin', role_id=role.id)
        session.add(user)
        session.flush() # Flush to get user.id
        # Add address
        address:Address = Address( address='123 Main', user_id=user.id)
        session.add(address)
        # Commit changes
        session.commit()
        print(f'Role added to database: {role}')
        print(f'User added to database: {user}')
        print(f'Address added to database: {address}')

def change_engine():
    # Change engine
    print(database.engine)
    database.engine = database.generate_engine(name='databaseb')
    print(database.engine.url)
    db_list = database.get_database_names(starts_with='database')
    print(database.get_engines_from_list(db_list))

if __name__ == "__main__":
    # change_engine()
    insert_to_database()
    pass