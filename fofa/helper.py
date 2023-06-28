import locale
import sys
import base64

def get_language():
    """ get shell language """
    if hasattr(locale, 'getdefaultlocale'):
        shell_lang, _ = locale.getdefaultlocale()
    else:
        shell_lang = locale.getdefaultlocale()[0]
    return shell_lang


if sys.version_info[0] > 2:
    # Python 3
    def encode_query(query_str):
        encoded_query = query_str.encode()
        encoded_query = base64.b64encode(encoded_query)
        return encoded_query.decode()
else:
    # Python 2
    def encode_query(query_str):
        encoded_query = base64.b64encode(query_str)
        return encoded_query

