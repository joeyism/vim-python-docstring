import vim
import abc

from utils import ObjectType


class Enviroment(abc.ABC):

    @property
    @abc.abstractmethod
    def plugin_root_dir(self):
        """ Return absolute path to directory one level above of directory
            containing python scripts.
        """

    @property
    @abc.abstractmethod
    def python_style(self):
        """ Returns string containing docstring style: google, numpy, etc.
            The style has to have corresponding template of name <style>.txt 
            in folder 'styles'.
        """

    @property
    @abc.abstractmethod
    def python_indent(self):
        """ Returns indentation of python source (tab, 4 spaces, ...) """

    @property
    @abc.abstractmethod
    def current_line_nr(self):
        """ Returns number of the current line, indexed from 0. """

    @property
    @abc.abstractmethod
    def current_line(self):
        """ Returns current line. """

    @abc.abstractmethod
    def append_after_line(self, line_nr, text):
        """ Print to buffer

        Append `text` to buffer on line below `line_nr`.

        Args:
            line_nr: (int)
            text: (str)

        """

    @abc.abstractmethod
    def lines_following_cursor(self):
        """ Generator that iterates lines in buffer, starting from current line. """

    #TODO will this work???
    @abc.abstractmethod
    def lines_till_end(self):
        """ Returns all lines from the current one until the end. """

class VimEnviroment(Enviroment):

    def __init__(self):
        settings = {'g:python_indent': '    ', 'g:python_style': 'google'}
        for k, v in settings.items():
            vim.command("let {} = get(g:,'{}', \"{}\")".format(k, v, v))

    def _get_var(self, name):
        return vim.eval(name)

    @property
    def plugin_root_dir(self):
        return self._get_var('s:plugin_root_dir')

    @property
    def python_style(self):
        return self._get_var('g:python_style')

    @property
    def python_indent(self):
        return self._get_var('g:python_indent')

    @property
    def current_line_nr(self):
        return vim.current.window.cursor[0] - 1

    @property
    def current_line(self):
        return vim.current.line

    def append_after_line(self, line_nr, text):
        line_nr += 1
        for line in reversed(text.split('\n')):
            vim.current.buffer.append(line, line_nr)

    def lines_following_cursor(self):
        import vim
        lines = []
        buffer = vim.current.buffer
        cursor_row = vim.current.window.cursor[0]-1
        current_row = cursor_row
        while True:
            yield current_row, buffer[current_row]
            current_row += 1
