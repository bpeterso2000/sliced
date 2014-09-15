Examples
========

This example is from 'slicing_demo` which is included in the `sliced` package.

.. code-block:: python

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
                        for row in sliced.sliced(rows, columns, dialect):
                            print(row)
                    except sliced.InvalidSliceString as error:
                        print('InvalidSliceString: {}'.format(error))
                    except sliced.EndPointValueError as error:
                        print('EndPointValueError: {}'.format(error))

.. toctree::
   :maxdepth: 2
   :hidden:
