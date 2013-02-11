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
            appform__app__provides__name='Auteurs',
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

    def _get_artworks_form(self):
        return Form.objects.get(appform__app__deployed=True,
            appform__app__provides__name='Livres',
            appform__app__environment=self.environment)

    def _get_artist_id_by_name(self, name):
        if ',' in name:
            nom, prenom = name.split(',')
        else:
            nom = prenom = name

        form = self._get_artists_form()

        records = Record.objects.filter(
                form__appform__app__provides=form.appform.app.provides,
                environment=self.environment,
                text_data__icontains=nom.strip())
        return records.get(text_data__icontains=prenom.strip()).pk

    def _get_support_form(self):
        return Form.objects.get(appform__app__deployed=True,
            appform__app__provides__name='Supports',
            appform__app__environment=self.environment)

    def _get_support_id_by_name(self, name):
        form = self._get_support_form()

        if getattr(self, '_supports', None) is None:
            self._supports = list(Record.objects.filter(
                form__appform__app__provides=form.appform.app.provides,
                environment=self.environment))

        for support in self._supports:
            if support.data['support'] == name:
                return support.pk

        support = Record(environment=self.environment, form=form)
        support.data = {'support': name}
        support.save()

        self._supports.append(support)

        return support.pk


    def import_artworks(self, path):
        source = codecs.open(path, 'r', 'utf-8')
        reader = unicode_csv_reader(source, skipinitialspace=True,
                delimiter=str(self.delimiter))

        form = self._get_artworks_form()
        books = Record.objects.filter(environment=self.environment,
            form__appform__app__provides=form.appform.app.provides)

        for row in reader:
            i, inv, author, support, kind, title, editor, lieu, \
            edit_year, volumes, description, comments = row

            data = {
                'n_douvrage': inv,
                'auteur': [self._get_artist_id_by_name(author)],
                'titre': title,
                'editeur': editor,
                'lieu_dedition': lieu,
                'date_dedition': edit_year,
                'support': [self._get_support_id_by_name(support)],
                'commentaire': comments,
                'n_dinventaire': i,
                'nombre_de_volumes': volumes,
                'commentaire__': description
            }

            found = None
            for book in books:
                if book.data.get('identifiant_unique', None) == i:
                    found = book
                    break

            if found is None:
                book = Record(form=form, environment=self.environment)

            book.data = data
            book.save()

            #record = Record(form=form, environment=self.environment,
            #        data = {'nom': last_name, 'prenom': first_name})
            #record.save()
