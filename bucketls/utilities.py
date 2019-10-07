import re
from bucketls.definitions import bls_keywords
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


def get_printable_size(byte_size):
    """
    Note: This function has not been implemented anywhere and it remains here
    for future use.
    A bit is the smallest unit, it's either 0 or 1
    1 byte = 1 octet = 8 bits
    1 kB = 1 kilobyte = 1000 bytes = 10^3 bytes
    1 KiB = 1 kibibyte = 1024 bytes = 2^10 bytes
    1 KB = 1 kibibyte OR kilobyte ~= 1024 bytes
        ~= 2^10 bytes (it usually means 1024 bytes but sometimes it's 1000... ask the sysadmin ;) )
    1 kb = 1 kilobits = 1000 bits (this notation should not be used, as it is very confusing)
    1 ko = 1 kilooctet = 1000 octets = 1000 bytes = 1 kB
    Also Kb seems to be a mix of KB and kb, again it depends on context.
    In linux, a byte (B) is composed by a sequence of bits (b). One byte has 256 possible values.
    More info : http://www.linfo.org/byte.html
    """
    BASE_SIZE = 1024.00
    MEASURE = ["B", "KB", "MB", "GB", "TB", "PB"]

    def _fix_size(size, size_index):
        if not size:
            return "0"
        elif size_index == 0:
            return str(size)
        else:
            return "{:.3f}".format(size)

    current_size = byte_size
    size_index = 0

    while current_size >= BASE_SIZE and len(MEASURE) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    size = _fix_size(current_size, size_index)
    measure = MEASURE[size_index]
    return size + measure


def parse_input(input_string):
    if 'cd ' in input_string and input_string not in bls_keywords:
        string_after_cd = [word for word in re.split('[^ ]* (.*)', input_string) if word != ''][0]
        return string_after_cd
    else:
        return input_string


def get_input(objects, prefix_path=None):
    style = Style.from_dict({
        'input': '#FF0000',
    })
    if prefix_path:
        formatted_input = f'(input) {prefix_path} >>> '
        message = [('class:input', formatted_input)]
    else:
        message = [('class:input', '(input) >>> ')]
    completer = WordCompleter(objects, ignore_case=True)
    while 1:
        user_input = prompt(
            message,
            history=FileHistory('history.txt'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            complete_while_typing=True,
            style=style)
        return user_input


def validate(object, objects):
    if object in objects:
        return True
    else:
        return False
