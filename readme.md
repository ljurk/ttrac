# ttrac

a script to track your working times

## installation

```
pip install ttrac
```

## usage

### data file

The data file will be created on your first `ttrac start`. The default path is `~/.config/ttrac/data.json`, but you can use every command with `-f/--file` argument to specify a different file

### commands

```
$ ttrac
Usage: ttrac [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  break    combines subcommand that allows you to take a break
  cat      prints content of the data file
  file     prints path to the data file
  start    start timetracking
  status   show all tracked times of the given day
  stop     stop timetracking
  version  prints the installed ttrac version

```

## example

Here is an example how `ttrac status` output looks like:

```
+------------+------------+
| day        | 19-05-2021 |
+------------+------------+
| start      | 07:04:18   |
| duration   | 7:24:15    |
| stop       | 14:28:33   |
| Breaks     |            |
| - start    | 08:59:41   |
| - stop     | 09:21:11   |
| - duration | 0:21:30    |
+------------+------------+
+------------+------------+
| day        | 20-05-2021 |
+------------+------------+
| start      | 07:04:18   |
| duration   | 7:25:42    |
| stop       | 14:30:00   |
| Breaks     |            |
| - start    | 13:02:02   |
| - stop     | 13:03:59   |
| - duration | 0:01:57    |
+------------+------------+
+----------+----------------+
| day      | 21-05-2021     |
+----------+----------------+
| start    | 09:15:44       |
| duration | 0:23:05.789542 |
| stop     | -              |
+----------+----------------+
```

The corresponding data file looks like this(`ttrac cat`):

```
{
    "19-05-2021": {
        "start": "07:04:18",
        "breaks": [
            {
                "start": "08:59:41",
                "stop": "09:21:11"
            }
        ],
        "stop": "14:28:33"
    },
    "20-05-2021": {
        "start": "07:04:18",
        "stop": "14:30:00",
        "breaks": [
            {
                "start": "13:02:02",
                "stop": "13:03:59"
            }
        ]
    },
    "21-05-2021": {
        "start": "09:15:44"
    }
}
```

