

import os
import click
import fofa
import json
import logging
from tqdm import tqdm

from .helper import XLSWriter, CSVWriter

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


def fofa_count(query):
    """Returns the number of results for a fofa query.
    """
    para = get_user_key()
    api = fofa.Client(**para)

    try:
        r = api.search(query, size=1, fields='ip')
    except fofa.FofaError as e:
        raise click.ClickException(e.message)

    click.echo(r['size'])


def fofa_stats(query, fields='ip,port,protocol', size=5):
    """Returns the number of results for a fofa query.
    """
    para = get_user_key()
    api = fofa.Client(**para)

    try:
        r = api.search_stats(query, size=size, fields=fields)
    except fofa.FofaError as e:
        raise click.ClickException(e.message)

    print_data(r)

def fofa_search_all(client, query, fields, num):
    size = 10000
    page = 1
    result = {
        'size': 0,
        'results': [],
        'consumed_fpoint': 0,
    }
    total = 0
    while True:
        try:
            remain_num = num - total
            if remain_num < size:
                size = remain_num

            r = client.search(query, fields=fields, page=page, size=size)
            data = r['results']
            total += len(data)

            result['results'] += data
            result['size'] += r['size']
            result['consumed_fpoint'] += r['consumed_fpoint']
            result['query'] = r['query']

            if len(data) < size or total >= num:
                break

            page+=1
        except fofa.FofaError as e:
            raise click.ClickException(u'search page {}, error: {}'.format(page, e.message))
    return result

def fofa_paged_search_save(writer, client, query, fields, num):
    """ Perform paged search using the search API and save the results to a writer.

    Args:
        writer: Writer object (e.g., CSVWriter or XLSWriter) for saving the results.
        client: FOFA API client.
        query: FOFA query string.
        fields: Comma-separated string of fields to include in the search results.
        num: Number of results to save.
    """
    size = 10000
    page = 1
    result = {
        'size': 0,
        'writed': 0,
        'consumed_fpoint': 0,
    }
    total = 0
    progress_bar = tqdm(total=num, desc='Downloading Fofa Data', leave=False, unit='item', unit_scale=True)
    try:
        while True:
            remain_num = num - total
            if remain_num < size:
                size = remain_num

            r = client.search(query, fields=fields, page=page, size=size)
            data = r['results']
            total += len(data)

            for d1 in data:
                progress_bar.update(1)
                writer.write_data(d1)

            progress_bar.refresh()
            result['size'] += r['size']
            result['consumed_fpoint'] += r['consumed_fpoint']
            result['query'] = r['query']
            result['writed'] = total

            if len(data) < size or total >= num:
                break

            page+=1
        progress_bar.set_postfix({'completed': True})
    except fofa.FofaError as e:
        raise click.ClickException(u'search page {}, error: {}'.format(page, e.message))

    return result

def fofa_next_search_save(writer, client, query, fields, num):
    """ Perform next search using the search next API and save the results to a writer.

    Args:
        writer: Writer object (e.g., CSVWriter or XLSWriter) for saving the results.
        client: FOFA API client.
        query: FOFA query string.
        fields: Comma-separated string of fields to include in the search results.
        num: Number of results to save.
    """
    size = 10000
    page = 1
    result = {
        'size': 0,
        'writed': 0,
        'consumed_fpoint': 0,
    }
    total = 0
    next = ''
    progress_bar = tqdm(total=num, desc='Downloading Fofa Data', leave=False, unit='item', unit_scale=True)
    try:
        while True:
            remain_num = num - total
            if remain_num < size:
                size = remain_num

            r = client.search_next(query, fields=fields, next=next, size=size)
            data = r['results']
            total += len(data)

            for d1 in data:
                progress_bar.update(1)
                writer.write_data(d1)

            progress_bar.refresh()

            next = r['next']
            result['size'] += r['size']
            result['consumed_fpoint'] += r['consumed_fpoint']
            result['query'] = r['query']
            result['writed'] = total

            if len(data) < size or total >= num:
                break

            page+=1
        progress_bar.set_postfix({'completed': True})
    except fofa.FofaError as e:
        raise click.ClickException(u'search next {}, error: {}'.format(next, e.message))

    return result


def fofa_download(client, query, fields, num, save_file, filetype='xls'):
    header = fields.split(',')

    if filetype == 'xls':
        writer = XLSWriter(save_file)
    else:
        writer = CSVWriter(save_file)

    writer.write_data(header)
    result = None
    try:
        if client.can_use_next():
            result = fofa_next_search_save(writer, client, query, fields, num)
        else:
            result = fofa_paged_search_save(writer, client, query, fields, num)
    finally:
        writer.close_writer()
        if result:
            click.echo("Query: '{}', saved to file: '{}', total: {:,}, written: {:,}, consumed fpoints: {:,}\n".format(
                result['query'],
                save_file,
                result['size'],
                result['writed'],
                result['consumed_fpoint']
            ))
        else:
            raise click.ClickException('No result')

@main.command()
@click.option('--count', '-c', default=False, flag_value=True, help='Count the number of results.')
@click.option('--stats', default=False, flag_value=True, help='Query statistics information.')
@click.option('--save', metavar='<filename>', help='Save the results to a file, supports csv and xls formats.')
@click.option('--color/--no-color', default=True, help='Enable/disable colorized output.')
@click.option('--fields', '-f', help='List of properties to show in the search results.', default='ip,port,protocol,domain')
@click.option('--size', help='The number of search results that should be returned. Maximum: 10000', default=100, type=int)
@click.option('-v', '--verbose', count=True, help='Increase verbosity level. Use -v for INFO level, -vv for DEBUG level.')
@click.argument('query', metavar='<fofa query>', nargs=-1)
def search(count, stats, save, color, fields, size, verbose, query):
    """ Returns the results for a fofa query.

    If the query contains special characters like && or ||, please enclose it in single quotes ('').

    Example:

    # Show results in the console
    fofa search 'title="fofa" && cert.is_match=true'

    # Count the number of results
    fofa search --count 'title="fofa" && cert.is_match=true'

    # Query statistics information
    fofa search --stats 'title="fofa" && cert.is_match=true'

    # Save the results to a csv file
    fofa search --save results.csv 'title="fofa" && cert.is_match=true'

    # Save the results to an Excel file
    fofa search --save results.xlsx 'title="fofa" && cert.is_match=true'
    """
    query = ' '.join(query).strip()
    if query == '':
        raise click.ClickException('Empty fofa query')

    fields = fields.strip()

    default_log_level = logging.WARN
    # 根据 -v 参数增加 verbosity level
    if verbose == 1:
        default_log_level = logging.INFO
    elif verbose >= 2:
        default_log_level = logging.DEBUG
    logging.basicConfig(level=default_log_level)

    # count mode
    if count:
        fofa_count(query)
        return

    # stat mode
    if stats:
        fofa_stats(query, fields, size)
        return

    para = get_user_key()
    api = fofa.Client(**para)

    # download mode
    if save:
        filetype = ''
        if save.endswith('.csv'):
            filetype = 'csv'
        elif save.endswith('.xls') or save.endswith('.xlsx'):
            filetype = 'xls'
        else:
            raise click.ClickException('save only support .csv or .xls file')
        fofa_download(api, query, fields, size, save, filetype)
        return

    # search mode
    r = fofa_search_all(api, query, fields, size)

    if r['size'] == 0:
        raise click.ClickException('No result')

    flds = fields.split(',')
    out = u''

    # stats line
    stats = "#stat query:'{}' total:{:,} size:{:,} consumed fpoints:{:,}\n".format(
        r['query'],
        r['size'],
        len(r['results']),
        r['consumed_fpoint']
    )
    out += stats

    separator = u'\t'

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
