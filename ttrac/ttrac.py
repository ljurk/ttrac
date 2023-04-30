import sys
import os.path
from datetime import datetime
import json
import click
import csv as csvModule
from terminaltables import AsciiTable

timeformat = "%H:%M"
strptimeformat = f"%d-%m-%Y {timeformat}"
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
@click.option('-t', '--time', type=str, default=now())
def start(__file, time=now(), day=today()):
    """start a break"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        exit(f'cannot parse json from {defaultfile}')
    if 'break' not in data[day].keys():
        data[day]['break'] = {'start': time}
    else:
        data[day]['break']['start'] = time

    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo("OK")

@_break.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
@click.option('-t', '--time', type=str, default=now())
def stop(__file, time=now(), day=today()):
    """stop a break"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        exit(f'cannot parse json from {defaultfile}')
    if 'break' not in data[day].keys():
        data[day]['break'] = {'stop': time}
    else:
        data[day]['break']['stop'] = time

    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo("OK")

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

        if 'break' in data[i].keys():
            table_data.append(["BreakDuration", abs(datetime.strptime(data[i]['break']['stop'], timeformat) - datetime.strptime(data[i]['break']['start'], timeformat))])
        print(AsciiTable(table_data).table)


@cli.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
@click.option('-t', '--time', type=str, default=now())
def start(__file, time, day=today()):
    """start timetracking"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        data = {day: {}}
    if day not in data:
        data[day] = {}
    data[day]['start'] = time
    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo(f"OK, starting at {time}")


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
@click.option('-t', '--time', type=str, default=now())
def stop(__file, time=now(), day=today()):
    """stop timetracking"""
    try:
        data = json.load(__file)
    except json.decoder.JSONDecodeError:
        print(f'cannot parse json from {defaultfile}')
        return
    if day not in data and 'start' not in data[day]:
        print("not started yet")
        return
    data[day]['stop'] = time
    clear(__file)
    __file.write(json.dumps(data, indent=4))
    click.echo(f"OK, stopping at {time}")

@cli.command()
@click.argument('--file', type=click.File('r+'), default=defaultfile)
def csv(__file):
    """export data as csv"""
    data = json.load(__file)
    print('day;start;stop;breakDuration;Sum')
    for day, dayItems in data.items():
        print(day, end=';')
        print(dayItems['start'], end=';')
        print(dayItems['stop'], end=';')
        if 'break' in dayItems:
            breakDuration = abs(datetime.strptime(dayItems['break']['stop'], timeformat) - datetime.strptime(dayItems['break']['start'], timeformat))
            print(breakDuration, end=';')
            print(abs(datetime.strptime(dayItems['stop'], timeformat) - datetime.strptime(dayItems['start'], timeformat)) - breakDuration)
        else:
            print('', end=';')
            print(abs(datetime.strptime(dayItems['stop'], timeformat) - datetime.strptime(dayItems['start'], timeformat)))
    #headers = data[0].keys()

    #writer.writeheader()

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
