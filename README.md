# Alembic + SQLAlchemy core
Welcome to the Alembic + SQLAlchemy codebase!

This repository contains code and documentation for using Alembic, a database migration tool, in conjunction with SQLAlchemy, a popular Python library for interacting with databases.

Alembic allows you to easily manage and apply changes to your database schema, such as adding or modifying tables and columns. SQLAlchemy is a powerful tool for querying and manipulating data in your database. Together, these two tools provide a solid foundation for building and maintaining a robust database-driven application.

In this repository, you will find examples and instructions for setting up and using Alembic and SQLAlchemy in your own projects. We hope you find this codebase helpful in your development efforts!

## Alembic commands
  * `alembic upgrade head` - Migrate the database to the latest version.
  * `alembic downgrade base` - Migrate the database to the base version.
  * `alembic revision --autogenerate -m "message"` - Generate a new revision file.
  * `alembic revision -m "message"` - Generate a new revision file without modifications.
  * `alembic show` - Show the current revision for each database.
  * `alembic history` - List changeset scripts in chronological order.
  * `alembic current` - Display the current revision for each database.

## Author
- **Name:** Álvaro Rubio Segovia
- **GitHub:** [ARubiose](https://github.com/ARubiose)
- **LinkedIn:** [alvaro-rubio-segovia](https://www.linkedin.com/in/alvaro-rubio-segovia/)
- **Email:** alvaro.rubio.segovia@gmail.com

## License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.