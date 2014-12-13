# -*- coding: utf-8 -*-
import pyparsing as pp
from pyparsing import Literal, Optional, ZeroOrMore, Regex, \
    Combine, Suppress, ParseException

from .exceptions import InvalidSliceString, OptionNotFound


class Grammar(object):

    digit = Regex(r'\d')
    nonzerodigit = Regex(r'[1-9]')
    positiveinteger = Combine(nonzerodigit + ZeroOrMore(digit))
    negativeinteger = Combine('-' + positiveinteger)
    nonzerointeger = positiveinteger ^ negativeinteger
    unsignedinteger = '0' ^ positiveinteger
    integer = '0' ^ nonzerointeger
    sep = Regex(r'[^a-zA-Z_]+$')

    dialect_method_prefix = '_dialect__'

    def __init__(self, dialect=None):
        if dialect is None:
            dialect = 'slice_list'
        self.dialect = dialect

    @property
    def dialect(self):
        return self._dialect

    @dialect.setter
    def dialect(self, name):
        if name:
            name = name.lower().replace(' ', '_').replace('-', '_')
        try:
            getattr(self, self.__class__.dialect_method_prefix + name)()
            self._dialect = name
            self._grammar_update = True
        except AttributeError:
            self._dialect = None
            error = dict(mesg='Unknown dialect', selected_option=name,
                         available_options=self.get_dialects())
            raise OptionNotFound(error)

    @property
    def allow_relative_indices(self):
        return self.endpoint == self.__class__.integer

    @allow_relative_indices.setter
    def allow_relative_indices(self, enabled):
        self._grammar_update = True
        endpoint = 'integer' if enabled else 'unsignedinteger'
        self.endpoint = getattr(self.__class__, endpoint)

    @property
    def allow_reverse_strides(self):
        return self.stride == self.__class__.nonzerointeger

    @allow_reverse_strides.setter
    def allow_reverse_strides(self, enabled):
        self._grammar_update = True
        stride = 'nonzerointeger' if enabled else 'positiveinteger'
        self.stride = getattr(self.__class__, stride)

    @property
    def allow_slice_list(self):
        return self._allow_slice_list

    @allow_slice_list.setter
    def allow_slice_list(self, enabled):
        self._grammar_update = True
        self._allow_slice_list = enabled

    @property
    def allow_stepped_intervals(self):
        return self._allow_stepped_intervals

    @allow_stepped_intervals.setter
    def allow_stepped_intervals(self, enabled):
        self._grammar_update = True
        self._allow_stepped_intervals = enabled

    @staticmethod
    def _to_int(tok):
        return int(tok[0])

    def get_dialects(self):
        prefix = self.__class__.dialect_method_prefix
        prefix_length = len(prefix)
        return [i[prefix_length:] for i in dir(self) if i.startswith(prefix)]

    def list_dialects(self, indent='    '):
        return 'Dialects:\n' + ('\n'.join([indent + dialect
                                for dialect in self.get_dialects()]))

    def _dialect__slice_list(self):
        self.list_sep = ','
        self.range_sep = ':'
        self.step_sep = ':'
        self.allow_relative_indices = True
        self.allow_stepped_intervals = True
        self.allow_reverse_strides = True
        self.allow_slice_list = True
        self.interval = {':': 'closed'}

    def _dialect__python_slice(self):
        self._dialect__slice_list()
        self.allow_slice_list = False

    def _dialect__dot_notation(self):
        self._dialect__slice_list()
        range_sep = Combine(Optional('.') + ':' + Optional('.'))
        self.range_sep = range_sep ^ '..'
        self.interval = {':': 'closed', '.:': 'left-open', ':.': 'right-open',
                         '.:.': 'open', '..': 'open'}

    def _dialect__double_dot(self):
        self._dialect__slice_list()
        self.range_sep = Combine('..' + Optional('.'))
        self.allow_stepped_interval = False
        self.interval = {'..': 'closed', '...': 'right-open'}

    def _dialect__unix_cut(self):
        self._dialect__slice_list()
        self.range_sep = '-'
        self.allow_relative_indices = False
        self.allow_stepped_interval = False

    def validate_separators(self):
        """
        Sepaarators can not be alphanumeric when headers are enabled, because
        of potential ambiguity.
        """
        for type_ in ['range', 'step', 'list']:
            try:
                sep = getattr(self, type_ + '_sep')
                if isinstance(sep, str):
                    self.sep.parseString(getattr(self, type_ + '_sep'))
                    setattr(self, type_ + '_sep', Literal(sep))
            except ParseException:
                mesg = ('{} separator can\'t contain alphanumeric or '
                        'underscore characters when headers are enabled.')
                raise ValueError(mesg.format(sep.title()))
        return True

    def _get_slice_item(self):
        index = endpoint = self.endpoint
        short_slice = Optional(endpoint) + self.range_sep + Optional(endpoint)
        if not self.allow_stepped_intervals:
            return Combine(index ^ short_slice)
        long_slice = short_slice + self.step_sep + Optional(self.stride)
        return Combine(index ^ short_slice ^ long_slice)

    def _get_slice_list(self):
        sep = Suppress(self.list_sep)
        slice_item = self._get_slice_item()
        return slice_item + ZeroOrMore(sep + slice_item) + Optional(sep)

    def _build_slice_grammar(self):
        to_int = self.__class__._to_int
        endpoint = self.endpoint.setResultsName
        range_sep = self.range_sep.setResultsName('range_sep')
        lower_bound = Optional(endpoint('start').setParseAction(to_int))
        upper_bound = Optional(endpoint('stop').setParseAction(to_int))
        stride = self.stride.setResultsName('step').setParseAction(to_int)
        short_slice = lower_bound + range_sep + upper_bound
        long_slice = short_slice + self.step_sep + Optional(stride)
        index = lower_bound
        if self.allow_stepped_intervals:
            return index ^ short_slice ^ long_slice
        return index ^ short_slice

    def _build_grammar(self):
        self.validate_separators()
        self._slice_grammar = self._build_slice_grammar() + pp.stringEnd
        self._text_grammar = (self._get_slice_list() if self.allow_slice_list
                              else self._get_slice_item()) + pp.stringEnd

    def parse_text(self, text):
        if self._grammar_update:
            self._build_grammar()
            self._grammar_update = False
        try:
            slices = self._text_grammar.parseString(text)
        except ParseException as error:
            info = {'text': text, 'column': error.column}
            raise InvalidSliceString(error.msg, info)
        return (dict(self._slice_grammar.parseString(i)) for i in slices)

    def parse(self, text):
        result = (self._get_interval_args(i) for i in self.parse_text(text))
        return result if self.allow_slice_list else next(result)

    def _get_interval_args(self, slice_):
        range_sep = slice_.get('range_sep')
        if range_sep:
            del slice_['range_sep']
            slice_['type_'] = self.interval.get(range_sep, 'closed')
        else:
            slice_['type_'] = 'closed'
            slice_['stop'] = slice_['start']
        return slice_
