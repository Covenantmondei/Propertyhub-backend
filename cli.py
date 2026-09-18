import sys
import argparse
from app.database import SessionLocal
from app.seeders.user_seeder import seed_users
from app.seeders.property_seeder import seed_properties
from app.seeders.visit_seeder import seed_visits
from app.seeders.clear_seeder import clear_database

def main():
    parser = argparse.ArgumentParser(
        description="PropertyHub Management CLI for Database Seeding & Maintenance",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available management commands")

    # Command: seed-all
    subparsers.add_parser(
        "seed-all",
        help="Seed entire database (1 Admin, 5 Agents + Profiles, 10 Buyers, Properties, Visits, Reviews)"
    )

    # Command: seed-users
    subparsers.add_parser(
        "seed-users",
        help="Seed 1 Admin, 5 Agents + Agent Profiles, and 10 Buyers (Password: Test1234!)"
    )

    # Command: seed-properties
    subparsers.add_parser(
        "seed-properties",
        help="Seed realistic properties and images assigned to existing agents"
    )

    # Command: seed-visits
    subparsers.add_parser(
        "seed-visits",
        help="Seed visit requests, favorites, property reservations, and agent reviews"
    )

    # Command: clear-db
    subparsers.add_parser(
        "clear-db",
        help="Clear all database tables and records"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    db = SessionLocal()
    try:
        if args.command == "seed-all":
            print("=== Starting Full Database Seeding ===")
            seed_users(db)
            seed_properties(db)
            seed_visits(db)
            print("=== Full Database Seeding Complete! ===")

        elif args.command == "seed-users":
            seed_users(db)

        elif args.command == "seed-properties":
            seed_properties(db)

        elif args.command == "seed-visits":
            seed_visits(db)

        elif args.command == "clear-db":
            clear_database(db)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()

