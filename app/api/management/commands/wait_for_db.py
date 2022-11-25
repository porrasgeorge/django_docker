"""
Django commands to wait for the database to start before running app
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import  BaseCommand

class Command(BaseCommand):
    """Django command to wait """
    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write('waiting for database.....')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database offline, waiting for response..')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database ready!'))

