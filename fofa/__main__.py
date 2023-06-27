

import os
import click
import fofa
import json

COLORIZE_FIELDS = {
    'ip': 'green',
    'port': 'yellow',
    'domain': 'magenta',
    'as_organization': 'cyan',
}

def escape_data(args):
    # Make sure the string is unicode so the terminal can properly display it
    # We do it using format() so it works across Python 2 and 3
    args = u'{}'.format(args)
    return args.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')


# Define the main entry point for all of our commands
@click.group(context_settings={'help_option_names': ['-h', '--help']})
def main():
    pass

def get_user_key():
    return {
        'email': os.environ['FOFA_EMAIL'],
        'key': os.environ['FOFA_KEY'],
    }

def print_data(data):
    click.echo(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))

@main.command()
def info():
    """Shows general information about your account"""
    para = get_user_key()
    api = fofa.Client(**para)
    try:
        r = api.get_userinfo()
    except fofa.FofaError as e:
        raise click.ClickException(e.message)
    print_data(r)


@main.command()
@click.argument('query', metavar='<fofa query>', nargs=-1)
def count(query):
    """Returns the number of results for a fofa query.

    If the query contains special characters like && or ||, please enclose it in single quotes ('').

    Example:

    fofa count 'title="fofa" && cert.is_match=true'
    """
    query = ' '.join(query).strip()
    if query == '':
        raise click.ClickException('Empty fofa query')

    para = get_user_key()
    api = fofa.Client(**para)

    try:
        r = api.search(query, size=1, fields='ip')
    except fofa.FofaError as e:
        raise click.ClickException(e.message)

    click.echo(r['size'])


@main.command()
@click.option('--detail/--no-detail', '-D', help='show host detail info', default=False, flag_value=True)
@click.argument('host', metavar='<domain or ip>', nargs=-1)
def host(detail, host):
    """Aggregated information for the specified host. """
    para = get_user_key()
    api = fofa.Client(**para)

    try:
        r = api.search_host(host, detail=detail)
    except fofa.FofaError as e:
        raise click.ClickException(e.message)

    print_data(r)


@main.command()
@click.option('--color/--no-color', default=True)
@click.option('--fields', help='List of properties to show in the search results.', default='ip,port,protocol,link')
@click.option('--limit', help='The number of search results that should be returned. Maximum: 10000', default=100, type=int)
@click.option('--separator', help='The separator between the properties of the search results.', default='\t')
@click.argument('query', metavar='<fofa query>', nargs=-1)
def search(color, fields, limit, separator, query):
    """ Returns the results for a fofa query.

    If the query contains special characters like && or ||, please enclose it in single quotes ('').

    Example:

    fofa search 'title="fofa" && cert.is_match=true'
    """
    para = get_user_key()
    api = fofa.Client(**para)

    query = ' '.join(query).strip()
    if query == '':
        raise click.ClickException('Empty fofa query')

    if limit > 10000:
        raise click.ClickException('Too many results requested, maximum is 10,000')

    fields = fields.strip()

    try:
        r = api.search(query, size=limit, fields=fields)
    except fofa.FofaError as e:
        raise click.ClickException(e.message)

    if r['size'] == 0:
        raise click.ClickException('No result')

    flds = fields.split(',')
    out = u''

    # stats line
    stats = u"#stat query:'" + r['query'] + u"'" + separator + u"total:" + u'{}'.format(r['size'])
    out += stats + u'\n'

    # header line
    header = u'#fields '
    for f in flds:
        header += f
        header += separator
    out += header + u'\n'

    for line in r['results']:
        row = u''

        for index, field in enumerate(flds):
            tmp = u''
            value = line[index]
            if value:
                tmp = escape_data(value)
                if color:
                    tmp = click.style(tmp, fg=COLORIZE_FIELDS.get(field, 'white'))

                row += tmp
            row += separator
        out += row + u'\n'
    click.echo_via_pager(out)




if __name__ == "__main__":
    main()
