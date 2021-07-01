
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
  def handle(self, *args, **options):
    self.stdout.write('Waiting for the database...')
    conn = None

    while not conn:
      try:
        conn = connections['default']
      except OperationalError:
        self.stdout.write('Db unavailable, waituing for 1 second...')
        time.sleep(1)

    self.stdout.write(self.style.SUCCESS('DB available!'))