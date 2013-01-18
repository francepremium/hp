import codecs
import os, os.path
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from appstore.models import Environment
from appstore.contrib.form_designer_appeditor.models import AppForm
from form_designer.models import Form
from formapp.models import Record


# from http://docs.python.org/2/library/csv.html
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class Command(BaseCommand):
    args = '<env id>'
    option_list = BaseCommand.option_list + (
        make_option('--artworks',
            action='store',
            dest='artworks',
            default=None,
            help='Path to artworks CSV - artists must be imported'),
        make_option('--artists',
            action='store',
            default=None,
            dest='artists',
            help='Path to artists CSV'),
        make_option('--delimiter',
            action='store',
            dest='delimiter',
            default=';',
            help='Specify a custom delimiter to parse PB csv files.'),
        )

    def handle(self, *args, **options):
        self.environment = Environment.objects.get(pk=args[0])
        self.delimiter = options['delimiter']

        if options['artists'] is not None:
            self.import_artists(options['artists'])

        if options['artworks'] is not None:
            self.import_artworks(options['artworks'])

    def _get_artists_form(self):
        return Form.objects.get(appform__app__deployed=True,
            appform__app__provides__name='PB Auteur',
            appform__app__environment=self.environment)

    def import_artists(self, path):
        source = codecs.open(path, 'r', 'utf-8')
        reader = unicode_csv_reader(source, skipinitialspace=True,
                delimiter=str(self.delimiter))

        form = self._get_artists_form()

        for row in reader:
            name, last_name, first_name = row

            record = Record(form=form, environment=self.environment,
                    data = {'nom': last_name, 'prenom': first_name})
            record.save()
