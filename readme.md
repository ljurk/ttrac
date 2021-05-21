# ttrac

a script to track your working times

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
