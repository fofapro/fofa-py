

import os
import click
import fofa
import json
import logging
from tqdm import tqdm

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


import xlwt
def write_to_excel(data, filename):
    # 创建一个Workbook对象
    workbook = xlwt.Workbook()

    # 创建一个Sheet对象
    sheet = workbook.add_sheet('Sheet1')

    # 写入数据
    for row_num, row_data in enumerate(data):
        for col_num, value in enumerate(row_data):
            sheet.write(row_num, col_num, value)

    # 保存Excel文件
    workbook.save(filename)

import csv
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def fofa_download(client, query, fields, num, save_file):
    size = 10000
    page = 1
    result = {
        'size': 0,
        'consumed_fpoint': 0,
    }
    total = 0
    header = fields.split(',')
    datas =[header]

    progress_bar = tqdm(total=num, desc='Downloading Fofa Data', leave=False, unit='item', unit_scale=True)
    try:
        while True:
            remain_num = num - total
            if remain_num < size:
                size = remain_num

            r = client.search(query, fields=fields, page=page, size=size)
            data = r['results']
            total += len(data)

            progress_bar.update(len(data))

            datas += data
            result['size'] += r['size']
            result['consumed_fpoint'] += r['consumed_fpoint']
            result['query'] = r['query']

            if len(data) < size or total >= num:
                break

            page+=1
    except fofa.FofaError as e:
        raise click.ClickException(u'search page {}, error: {}'.format(page, e.message))
    finally:
        if len(datas) > 0:
            if save_file.endswith(".xls"):
                write_to_excel(datas, save_file)
            else:
                write_to_csv(datas, save_file)
            click.echo("save query:'{}' to file {}, total:{:,} size:{:,} consumed fpoints:{:,}\n".format(
                result['query'],
                save_file,
                result['size'],
                total,
                result['consumed_fpoint']
            ))


@main.command()
@click.option('--count', default=False, flag_value=True, help='Count the number of results.')
@click.option('--stats', default=False, flag_value=True, help='Query statistics information.')
@click.option('--save', metavar='<filename>', help='Save the results to a file.')
@click.option('--color/--no-color', default=True, help='Enable/disable colorized output.')
@click.option('--fields', help='List of properties to show in the search results.', default='ip,port,protocol,domain')
@click.option('--size', help='The number of search results that should be returned. Maximum: 10000', default=100, type=int)
@click.option('--separator', help='The separator between the properties of the search results.', default='\t')
@click.option('-v', '--verbose', count=True, help='Increase verbosity level. Use -v for INFO level, -vv for DEBUG level.')
@click.argument('query', metavar='<fofa query>', nargs=-1)
def search(count, stats, save, color, fields, size, separator, verbose, query):
    """ Returns the results for a fofa query.

    If the query contains special characters like && or ||, please enclose it in single quotes ('').

    Example:

    # Show results in the console
    fofa search 'title="fofa" && cert.is_match=true'

    # Count the number of results
    fofa search --count 'title="fofa" && cert.is_match=true'

    # Query statistics information
    fofa search --stats 'title="fofa" && cert.is_match=true'

    # Save the results to a file
    fofa search --save results.csv 'title="fofa" && cert.is_match=true'
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
        if not save.endswith('.csv') and not save.endswith('.xls'):
            raise click.ClickException('save only support .csv or .xls file')
        fofa_download(api, query, fields, size, save)
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
