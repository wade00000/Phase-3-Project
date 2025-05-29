from app.database import engine, Base
from app.cli import cli

def main():
    try:
        Base.metadata.create_all(engine)
        print("Database tables created or already exist.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return

    cli()

if __name__ == "__main__":
    main()
