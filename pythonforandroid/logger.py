"""
Moduł logger dla python-for-android
====================================

Ten moduł zawiera konfigurację logowania i funkcje pomocnicze do formatowania
i wyświetlania komunikatów podczas budowania aplikacji Android.
"""

import logging
import os
import re
import sh
from sys import stdout, stderr
from math import log10
from collections import defaultdict
from colorama import Style as Colo_Style, Fore as Colo_Fore


# monkey patch aby wyświetlić pełny output
sh.ErrorReturnCode.truncate_cap = 999999


class LevelDifferentiatingFormatter(logging.Formatter):
    """
    Formatter logów różnicujący poziomy logowania przez kolorowanie.
    
    Formatuje komunikaty w zależności od poziomu (ERROR, WARNING, INFO, DEBUG)
    dodając odpowiednie prefiksy i kolory.
    """
    def format(self, record):
        if record.levelno > 30:
            record.msg = '{}{}[ERROR]{}{}:   '.format(
                Err_Style.BRIGHT, Err_Fore.RED, Err_Fore.RESET,
                Err_Style.RESET_ALL) + record.msg
        elif record.levelno > 20:
            record.msg = '{}{}[WARNING]{}{}: '.format(
                Err_Style.BRIGHT, Err_Fore.RED, Err_Fore.RESET,
                Err_Style.RESET_ALL) + record.msg
        elif record.levelno > 10:
            record.msg = '{}[INFO]{}:    '.format(
                Err_Style.BRIGHT, Err_Style.RESET_ALL) + record.msg
        else:
            record.msg = '{}{}[DEBUG]{}{}:   '.format(
                Err_Style.BRIGHT, Err_Fore.LIGHTBLACK_EX, Err_Fore.RESET,
                Err_Style.RESET_ALL) + record.msg
        return super().format(record)


logger = logging.getLogger('p4a')
# Konieczne, ponieważ importlib przeładowuje to,
# co dodałoby drugi handler i zresetowało poziom
if not hasattr(logger, 'touched'):
    logger.setLevel(logging.INFO)
    logger.touched = True
    ch = logging.StreamHandler(stderr)
    formatter = LevelDifferentiatingFormatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error


class colorama_shim:
    """
    Klasa pośrednia dla colorama umożliwiająca włączanie/wyłączanie kolorowania.
    
    Pozwala kontrolować, czy kolory są włączone czy wyłączone w runtime,
    zwracając puste stringi gdy są wyłączone.
    """

    def __init__(self, real):
        self._dict = defaultdict(str)
        self._real = real
        self._enabled = False

    def __getattr__(self, key):
        return getattr(self._real, key) if self._enabled else self._dict[key]

    def enable(self, enable):
        self._enabled = enable


Out_Style = colorama_shim(Colo_Style)
Out_Fore = colorama_shim(Colo_Fore)
Err_Style = colorama_shim(Colo_Style)
Err_Fore = colorama_shim(Colo_Fore)


def setup_color(color):
    """
    Konfiguruje kolorowanie wyjścia na podstawie preferencji użytkownika.
    
    Args:
        color: 'never' (brak kolorów), 'always' (zawsze kolory), 
               lub 'auto' (kolory jeśli terminal je wspiera)
    """
    enable_out = (False if color == 'never' else
                  True if color == 'always' else
                  stdout.isatty())
    Out_Style.enable(enable_out)
    Out_Fore.enable(enable_out)

    enable_err = (False if color == 'never' else
                  True if color == 'always' else
                  stderr.isatty())
    Err_Style.enable(enable_err)
    Err_Fore.enable(enable_err)


def info_main(*args):
    """Wyświetla główną informację z pogrubieniem i zielonym kolorem."""
    logger.info(''.join([Err_Style.BRIGHT, Err_Fore.GREEN] + list(args) +
                        [Err_Style.RESET_ALL, Err_Fore.RESET]))


def info_notify(s):
    """Wyświetla powiadomienie z jasnoniebieskim kolorem."""
    info('{}{}{}{}'.format(Err_Style.BRIGHT, Err_Fore.LIGHTBLUE_EX, s,
                           Err_Style.RESET_ALL))


def shorten_string(string, max_width):
    """
    Tworzy skrócony string o ograniczonej długości w formie:
    "the string is very lo...(and 15 more)"
    
    Args:
        string: String do skrócenia
        max_width: Maksymalna szerokość wyniku
        
    Returns:
        Skrócony string lub oryginalny, jeśli mieści się w limicie
    """
    string_len = len(string)
    if string_len <= max_width:
        return string
    visible = max_width - 16 - int(log10(string_len))
    # expected suffix len "...(and XXXXX more)"
    if not isinstance(string, str):
        visstring = str(string[:visible], errors='ignore')
    else:
        visstring = string[:visible]
    return u''.join((visstring, u'...(and ',
                     str(string_len - visible), u' more)'))


def get_console_width():
    """
    Pobiera szerokość konsoli w kolumnach.
    
    Próbuje różnych metod wykrycia szerokości konsoli.
    Zwraca 100 jako wartość domyślną jeśli wykrycie się nie powiedzie.
    
    Returns:
        int: Szerokość konsoli w kolumnach (minimum 25)
    """
    try:
        cols = int(os.environ['COLUMNS'])
    except (KeyError, ValueError):
        pass
    else:
        if cols >= 25:
            return cols

    try:
        cols = max(25, int(os.popen('stty size', 'r').read().split()[1]))
    except Exception:
        pass
    else:
        return cols

    return 100


def shprint(command, *args, **kwargs):
    """
    Uruchamia komendę (która powinna być instancją sh.Command), 
    jednocześnie logując output.
    
    Args:
        command: Instancja sh.Command do uruchomienia
        *args: Argumenty dla komendy
        **kwargs: Dodatkowe opcje:
            _critical: Jeśli True, kończy program przy błędzie
            _tail: Liczba linii do wyświetlenia z końca outputu przy błędzie
            _filter: Regex filtr do wyświetlania tylko pasujących linii
            _filterout: Regex filtr do pomijania pasujących linii
    
    Returns:
        Output komendy
        
    Raises:
        sh.ErrorReturnCode: Jeśli komenda zawiedzie i _critical nie jest True
    """
    kwargs["_iter"] = True
    kwargs["_out_bufsize"] = 1
    kwargs["_err_to_out"] = True
    kwargs["_bg"] = True
    is_critical = kwargs.pop('_critical', False)
    tail_n = kwargs.pop('_tail', None)
    full_debug = False
    if "P4A_FULL_DEBUG" in os.environ:
        tail_n = 0
        full_debug = True
    filter_in = kwargs.pop('_filter', None)
    filter_out = kwargs.pop('_filterout', None)
    if len(logger.handlers) > 1:
        logger.removeHandler(logger.handlers[1])
    columns = get_console_width()
    command_path = str(command).split('/')
    command_string = command_path[-1]
    string = ' '.join(['{}->{} running'.format(Out_Fore.LIGHTBLACK_EX,
                                               Out_Style.RESET_ALL),
                       command_string] + list(args))

    # If logging is not in DEBUG mode, trim the command if necessary
    if logger.level > logging.DEBUG:
        logger.info('{}{}'.format(shorten_string(string, columns - 12),
                                  Err_Style.RESET_ALL))
    else:
        logger.debug('{}{}'.format(string, Err_Style.RESET_ALL))

    need_closing_newline = False
    try:
        msg_hdr = '           working: '
        msg_width = columns - len(msg_hdr) - 1
        output = command(*args, **kwargs)
        for line in output:
            if isinstance(line, bytes):
                line = line.decode('utf-8', errors='replace')
            if logger.level > logging.DEBUG:
                if full_debug:
                    stdout.write(line)
                    stdout.flush()
                    continue
                msg = line.replace(
                    '\n', ' ').replace(
                        '\t', ' ').replace(
                            '\b', ' ').rstrip()
                if msg:
                    if "CI" not in os.environ:
                        stdout.write(u'{}\r{}{:<{width}}'.format(
                            Err_Style.RESET_ALL, msg_hdr,
                            shorten_string(msg, msg_width), width=msg_width))
                        stdout.flush()
                        need_closing_newline = True
            else:
                logger.debug(''.join(['\t', line.rstrip()]))
        if need_closing_newline:
            stdout.write('{}\r{:>{width}}\r'.format(
                Err_Style.RESET_ALL, ' ', width=(columns - 1)))
            stdout.flush()
    except sh.ErrorReturnCode as err:
        if need_closing_newline:
            stdout.write('{}\r{:>{width}}\r'.format(
                Err_Style.RESET_ALL, ' ', width=(columns - 1)))
            stdout.flush()
        if tail_n is not None or filter_in or filter_out:
            def printtail(out, name, forecolor, tail_n=0,
                          re_filter_in=None, re_filter_out=None):
                lines = out.splitlines()
                if re_filter_in is not None:
                    lines = [line for line in lines if re_filter_in.search(line)]
                if re_filter_out is not None:
                    lines = [line for line in lines if not re_filter_out.search(line)]
                if tail_n == 0 or len(lines) <= tail_n:
                    info('{}:\n{}\t{}{}'.format(
                        name, forecolor, '\t\n'.join(lines), Out_Fore.RESET))
                else:
                    info('{} (last {} lines of {}):\n{}\t{}{}'.format(
                        name, tail_n, len(lines),
                        forecolor, '\t\n'.join([s for s in lines[-tail_n:]]),
                        Out_Fore.RESET))
            printtail(err.stdout.decode('utf-8'), 'STDOUT', Out_Fore.YELLOW, tail_n,
                      re.compile(filter_in) if filter_in else None,
                      re.compile(filter_out) if filter_out else None)
            printtail(err.stderr.decode('utf-8'), 'STDERR', Err_Fore.RED)
        if is_critical or full_debug:
            env = kwargs.get("_env")
            if env is not None:
                info("{}ENV:{}\n{}\n".format(
                    Err_Fore.YELLOW, Err_Fore.RESET, "\n".join(
                        "export {}='{}'".format(n, v) for n, v in env.items())))
            info("{}COMMAND:{}\ncd {} && {} {}\n".format(
                Err_Fore.YELLOW, Err_Fore.RESET, os.getcwd(), command,
                ' '.join(args)))
            warning("{}ERROR: {} failed!{}".format(
                Err_Fore.RED, command, Err_Fore.RESET))
        if is_critical:
            exit(1)
        else:
            raise

    return output
