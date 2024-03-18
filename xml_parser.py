import os
from lxml import etree
from inflection import underscore as camel_to_snake
from sqlalchemy.exc import SQLAlchemyError
from database.queries import OrmMethods
from database.models import *


async def parse_data():
    try:
        # Parsing the xml files in data directory
        await _parse_directory('./data')
    except Exception as e:
        raise Exception(f'Error parsing data: {e}')


async def _parse_directory(root_dir: str):
    """
    Walk through the directories and parse 'manifest.xml' in each subdirectory.

    :param root_dir: The root directory from which to start the walk.
    """
    for subdir, dirs, files in os.walk(root_dir):
        if 'manifest.xml' in files:
            path = os.path.join(subdir, 'manifest.xml')
            try:
                # Parse the manifest file to extract and save data to the database
                await _parse_manifest(path)
            except etree.XMLSyntaxError as e:
                print(f'XML syntax error in {path}: {e}')
            except Exception as e:
                print(f'Error parsing {path}: {e}')


async def _parse_manifest(xml_path: str):
    """
    Parse the XML manifest file,
    create or update database records for the date, exchanges, and instruments.

    :param xml_path: The file path of the manifest XML.
    """
    try:
        tree = etree.parse(xml_path)
        root = tree.getroot()
    except etree.XMLSyntaxError:
        raise

    try:
        date = root.find('Date').text
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        date_pk = await OrmMethods.add_new_data(DateOrm, {'date': date})
    except SQLAlchemyError as e:
        raise Exception(f'Database error creating ManifestDate for: {e}')

    for exchange in root.xpath('.//Exchange'):
        try:
            attributes = {camel_to_snake(attr): exchange.get(attr)
                          for attr in ['Name', 'Location']}
            attributes['date'] = date_pk
            exchange_pk = await OrmMethods.add_new_data(ExchangeOrm, attributes)
        except SQLAlchemyError as e:
            print(f'Database error processing exchange: {e}')
            continue

        for instrument in exchange.xpath('.//Instrument'):
            try:
                attributes = {camel_to_snake(attr): instrument.get(attr)
                              for attr in ['Name', 'StorageType', 'Levels', 'Iid',
                                           'AvailableIntervalBegin', 'AvailableIntervalEnd']}
                attributes['iid'] = int(attributes['iid'])
                attributes['available_interval_begin'] = datetime.datetime.strptime(attributes['available_interval_begin'], '%H:%M').time()
                attributes['available_interval_end'] = datetime.datetime.strptime(attributes['available_interval_end'],
                                                                                  '%H:%M').time()
                attributes['exchange'] = exchange_pk
                await OrmMethods.add_new_data(InstrumentOrm, attributes)
            except SQLAlchemyError as e:
                print(f'Database error processing instrument: {e}')
                continue
