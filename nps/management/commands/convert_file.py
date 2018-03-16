from django.core.management.base import BaseCommand
import pandas as pd
import csv


class Command(BaseCommand):
    help = 'Converts a raw csv to utf-8 encoding and prepares it for importing.'

    def add_arguments(self, parser):
        parser.add_argument('input')
        parser.add_argument('output')
        parser.add_argument('file_format')

    def handle(self, *args, **options):
        input_file = options['input']
        output_file = options['output']
        file_format = options['file_format']

        # read in data from file
        df = pd.read_csv(input_file, encoding='latin-1')

        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', 1, inplace=True)
        if 'id' not in df.columns:
            print('adding id column')
            df['id'] = ''

        rename = False
        rename_dict = {}
        if 'db_name' in df.columns:
            rename_dict['db_name'] = 'client'
            rename = True

        if file_format == 'old':
            dup_subset = ['client', 'survey_name', 'user_id', 'response']
            # convert column names
            if 'type' in df.columns:
                rename_dict['type'] = 'question_type'
                rename = True
            if 'db_name' in df.columns:
                rename_dict['db_name'] = 'client'
                rename = True
            if 'user_can_teach' in df.columns:
                rename_dict['user_can_teach'] = 'can_teach'
                rename = True
            if 'can_teach' in df.columns:
                df['can_teach'] = df['can_teach'].astype(int)
        else:
            if 'role_type' in df.columns:
                rename_dict['role_type'] = 'user_type'
                rename = True
            dup_subset = ['client', 'survey_name', 'user_id', 'recommend_response', 'reason_response']

        if rename:
            df.rename(columns=rename_dict, inplace=True)

        df.drop_duplicates(inplace=True, subset=dup_subset)

        print('writing dataframe to file')
        df.to_csv(output_file, encoding='utf-8', index=False, quoting=csv.QUOTE_NONNUMERIC)





