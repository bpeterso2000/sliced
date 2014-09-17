Sliced demonstration
====================

This example is from 'slicing_demo.py` which is included in the `sliced` package::

    import sys
    import sliced
    if sys.version_info.major < 3:
        input = raw_input

    rows = [
        ['alpha-1', 'alpha-2', 'alpha-3', 'alpha-4', 'alpha-5', 'alpha-6'],
        ['beta-1', 'beta-2', 'beta-3', 'beta-4', 'beta-5', 'beta-6'],
        ['gamma-1', 'gamma-2', 'gamma-3', 'gamma-4', 'gamma-5', 'gamma-6'],
    ]

    dialect = True
    while dialect:
        sliced.Grammar().list_dialects()
        dialect = input('\nEnter dialect? ')
        if dialect and dialect in sliced.Grammar().get_dialects():

            columns = True
            while columns:
                print()
                columns = input('\nSelect columns? ')
                if columns:

                    try:

                        # this is the workhorse function
                        rows = sliced.slices(rows, columns, dialect)

                        for row in rows:
                            print(row)

                    except sliced.InvalidSliceString as error:
                        # error while parsing text against the grammar
                        print('InvalidSliceString: {}'.format(error))

                    except sliced.EndPointValueError as error:
                        # when origin=1, start & stop can't equal zero
                        print('EndPointValueError: {}'.format(error))
