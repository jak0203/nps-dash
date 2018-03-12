from django.core.management.base import BaseCommand, CommandError
from nps.models import RawResults, AggregatedResults
import pandas as pd


class Command(BaseCommand):
    help = 'Converts a raw csv to utf-8 encoding and prepares it for importing.'

    def add_arguments(self, parser):
        parser.add_argument('input')
        parser.add_argument('output')

    def handle(self, *args, **options):
        input_file = options['input']
        output_file = options['output']
        # read in data from file
        df = pd.read_csv(input_file, encoding='latin-1')
        # add id column
        print('adding id column')
        df.drop('Unnamed: 0', 1, inplace=True)
        df['id'] = ''
        df.drop_duplicates(inplace=True)

        # convert column names
        rename = {
            'type': 'question_type',
            'db_name': 'client',
        }
        df.rename(columns=rename, inplace=True)

        print('writing dataframe to file')
        df.to_csv(output_file, encoding='utf-8', index=False)





