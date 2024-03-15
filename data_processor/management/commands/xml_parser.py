import os
from lxml import etree
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError
from inflection import underscore as camel_to_snake
from data_processor.models import *


class Command(BaseCommand):
    help = 'Upload data from xml to database'

    def handle(self, *args, **options):
        try:
            # Parsing the xml files in data directory
            parse_directory('./data')
        except Exception as e:
            raise CommandError(f'Error parsing data: {e}')


def parse_directory(root_dir: str):
    """
    Walk through the directories and parse 'manifest.xml' in each subdirectory.

    :param root_dir: The root directory from which to start the walk.
    """
    for subdir, dirs, files in os.walk(root_dir):
        if 'manifest.xml' in files:
            path = os.path.join(subdir, 'manifest.xml')
            try:
                # Parse the manifest file to extract and save data to the database
                parse_manifest(path)
            except etree.XMLSyntaxError as e:
                print(f'XML syntax error in {path}: {e}')
            except Exception as e:
                print(f'Error parsing {path}: {e}')


def parse_manifest(xml_path: str):
    """
    Parse the XML manifest file,
    create or update database records for the date, exchanges, and instruments.

    :param xml_path: The file path of the manifest XML.
    """
    try:
        tree = etree.parse(xml_path)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        raise

    try:
        date = root.find('Date').text
        manifest_date, created = ManifestDate.objects.get_or_create(date=date)
    except DatabaseError as e:
        raise Exception(f'Database error creating ManifestDate for: {e}')

    for exchange in root.xpath('.//Exchange'):
        try:
            attributes = {camel_to_snake(attr): exchange.get(attr)
                          for attr in ['Name', 'Location']}
            exchange_m, created = Exchange.objects.get_or_create(date=manifest_date, **attributes)
        except DatabaseError as e:
            print(f'Database error processing exchange: {e}')
            continue

        for instrument in exchange.xpath('.//Instrument'):
            try:
                attributes = {camel_to_snake(attr): instrument.get(attr)
                              for attr in ['Name', 'StorageType', 'Levels', 'Iid',
                                           'AvailableIntervalBegin', 'AvailableIntervalEnd']}
                attributes['iid'] = int(attributes['iid'])
                Instrument.objects.get_or_create(exchange=exchange_m, **attributes)
            except DatabaseError as e:
                print(f'Database error processing instrument: {e}')
                continue
