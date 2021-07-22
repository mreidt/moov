import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Comando para o Django pausar a execução até que a base de dados do
    PostgreSQL esteja disponível.

    Esse comando foi ensinado em um curso da Udemy e é muito útil para
    evitar erros de base não disponível durante a execução.
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
