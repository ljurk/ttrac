import os.path
from datetime import datetime
import json
import click
from terminaltables import AsciiTable

timeformat = "%H:%M:%S"
strptimeformat = "%d-%m-%Y %H:%M:%S"
dayformat = "%d-%m-%Y"
defaultfile=os.path.expanduser('~/.config/ttrac/data.json')

def now():
    return str(datetime.now().strftime(timeformat))

def today():
    return str(datetime.now().strftime(dayformat))

def clear(filehandle):
    filehandle.seek(0)
    filehandle.truncate()

@click.group()
def cli():
    pass

@cli.group(name='break')
def _break():
    """combines subcommand that allows you to take a break"""
    pass

@_break.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
def start(__file, day=today()):
    """start a break"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        exit(f'cannot parse json from {defaultfile}')
    if 'breaks' not in data[day].keys():
        data[day]['breaks'] = [{'start': now()}]
    else:
        if 'stop' not in data[day]['breaks'][-1].keys():
            exit("previous break hasnt stopped yet")
        data[day]['breaks'].append({'start': now()})

    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo("OK")

@_break.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
def stop(__file, day=today()):
    """stop a break"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        exit(f'cannot parse json from {defaultfile}')
    if 'breaks' not in data[day].keys() or 'stop' in data[day]['breaks'][-1].keys():
        exit("no break started yet")
    else:
        data[day]['breaks'][-1]['stop'] = now()

    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo("OK")


def printTable(table_data):
    table = AsciiTable(table_data)
    print(table.table)

@cli.command()
@click.option('-t', '--total', is_flag=True, default=False)
@click.argument('--file', type=click.File('r'), default=defaultfile)
def status(total, __file, day=today()):
    """show all tracked times of the given day"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        exit(f'cannot parse json from {defaultfile}')
    for i in data:
        if i != day and not total:
            continue
        start = datetime.strptime(f"{i} {data[i]['start']}", strptimeformat)
        stop = datetime.strptime(f"{i} {data[i]['stop']}", strptimeformat) if 'stop' in data[i] else datetime.now()
        table_data = [
            ['day', i],
            ['start', data[i]['start']],
            ['duration', abs(start - stop)],
            ['stop', data[i]['stop'] if 'stop' in data[i] else '-']
        ]

        if 'breaks' in data[i].keys():
            table_data.append(["Breaks", ""])
            for num, y in enumerate(data[i]['breaks']):
                if 'stop' in y:
                    delta = abs(datetime.strptime(f"{i} {y['start']}", strptimeformat) - datetime.strptime(f"{i} {y['stop']}", strptimeformat))
                else:
                    delta = abs(datetime.strptime(f"{i} {y['start']}", strptimeformat) - datetime.now())
                delim = '-' * (num + 1)
                table_data = table_data + [[f'{delim} start', y['start']],
                               [f'{delim} stop', y['stop'] if 'stop' in y else '-'],
                               [f'{delim} duration', delta]]
        printTable(table_data)


@cli.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
def start(__file, day=today()):
    """start timetracking"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        data = {day: {}}
    if day not in data:
        data[day] = {}
    data[day]['start'] = now()
    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo("OK")


@cli.command()
def file():
    """prints path to the data file """
    print(defaultfile)

@cli.command()
@click.argument('--file', type=click.File('r'), default=defaultfile)
def cat(__file):
    """prints content of the data file """
    print(__file.read())

@cli.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
def stop(__file, day=today()):
    """stop timetracking"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        print(f'cannot parse json from {defaultfile}')
        return
    if day not in data and 'start' not in data[day]:
        print("not started yet")
        return
    data[day]['stop'] = now()
    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo("OK")

@cli.command()
def version():
    """prints the installed ttrac version"""
    import pkg_resources  # part of setuptools
    print(pkg_resources.require("ttrac")[0].version)

if __name__ == '__main__':
    if not os.path.isfile(defaultfile):
        os.makedirs(os.path.dirname(defaultfile), exist_ok=True)
        open(defaultfile, 'a').close()

    cli()
