import sys

from sliced import slices
from sliced import Grammar, InvalidSliceString, EndPointValueError

if sys.version_info.major < 3:
    input = raw_input

rows = [
    ['alpha-1', 'alpha-2', 'alpha-3', 'alpha-4', 'alpha-5', 'alpha-6'],
    ['beta-1', 'beta-2', 'beta-3', 'beta-4', 'beta-5', 'beta-6'],
    ['gamma-1', 'gamma-2', 'gamma-3', 'gamma-4', 'gamma-5', 'gamma-6'],
]

dialect = True
while dialect:
    Grammar().list_dialects()
    dialect = input('\nEnter dialect? ')
    if dialect and dialect in Grammar().get_dialects():

        columns = True
        while columns:
            print()
            columns = input('\nSelect columns? ')
            if columns:

                try:
                    for row in slices(rows, columns, dialect):
                        print(row)
                except InvalidSliceString as error:
                    print('InvalidSliceString: {}'.format(error))
                except EndPointValueError as error:
                    print('EndPointValueError: {}'.format(error))