from datetime import datetime
import json
import click
from terminaltables import AsciiTable

timeformat = "%H:%M:%S"
strptimeformat = "%d-%m-%Y %H:%M:%S"
dayformat = "%d-%m-%Y"
def now():
    return str(datetime.now().strftime(timeformat))

def today():
    return str(datetime.now().strftime(dayformat))

@click.group()
def cli():
    pass

@cli.group(name='break')
def _break():
    pass

@_break.command()
def start(day=today()):
    with open('data.json') as fh:
        data = json.load(fh)
    if 'breaks' not in data[day].keys():
        data[day]['breaks'] = [{'start': now()}]
    else:
        if 'stop' not in data[day]['breaks'][-1].keys():
            print("no break started yet")
            return
        data[day]['breaks'].append({'start': now()})

    with open('data.json', 'w') as fh:
        fh.write(json.dumps(data, indent=4))
    print("ok")

@_break.command()
def stop(day=today()):
    with open('data.json') as fh:
        data = json.load(fh)
    if 'breaks' not in data[day].keys() or 'stop' in data[day]['breaks'][-1].keys():
        print("no break started yet")
        return
    else:
        data[day]['breaks'][-1]['stop'] = now()

    with open('data.json', 'w') as fh:
        fh.write(json.dumps(data, indent=4))
    print("ok")


def printTable(table_data):
    table = AsciiTable(table_data)
    #table.inner_heading_row_border = False
    print(table.table)

@cli.command()
@click.option('-t', '--total', is_flag=True, default=False)
def status(total, day=today()):
    with open('data.json') as fh:
        data = json.load(fh)
    for i in data:
        if i != day and not total:
            continue
        start = datetime.strptime(f"{i} {data[i]['start']}", strptimeformat)
        table_data = [
            ['day', i],
            ['start', data[i]['start']],
            ['duration', abs(start - datetime.now())],
            ['stop', data[i]['stop'] if 'stop' in data[i] else '-']
        ]

        if 'breaks' in data[i].keys():
            #breaks = [["Start", "Stop", "Duration"]]
            table_data.append(["Breaks", ""])
            for num, y in enumerate(data[i]['breaks']):
                if 'stop' in y:
                    print(f"{i} {y['start']}")
                    print("{i} {y['stop']}")
                    delta = abs(datetime.strptime(f"{i} {y['start']}", strptimeformat) - datetime.strptime(f"{i} {y['stop']}", strptimeformat))
                else:
                    delta = abs(datetime.strptime(f"{i} {y['start']}", strptimeformat) - datetime.now())
                delim = '-' * (num + 1)
                table_data = table_data + [[f'{delim} start', y['start']],
                               [f'{delim} stop', y['stop'] if 'stop' in y else '-'],
                               [f'{delim} duration', delta]]
            #printTable(breaks)
        printTable(table_data)


@cli.command()
def start(day=today()):
    with open('data.json') as fh:
        data = json.load(fh)
    if day not in data:
        data[day] = {}
    data[day]['start'] = now()
    with open('data.json', 'w') as fh:
        fh.write(json.dumps(data, indent=4))
    print(data)
    click.echo("OK")


@cli.command()
def stop(day=today()):
    with open('data.json') as fh:
        data = json.load(fh)
    if day not in data and 'start' not in data[day]:
        print("not started yet")
        return
    data[day]['stop'] = now()
    with open('data.json', 'w') as fh:
        fh.write(json.dumps(data, indent=4))
    click.echo("OK")

if __name__ == '__main__':
    cli()
