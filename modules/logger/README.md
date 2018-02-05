# Logger

Python 3 module which provides functions to output formatted logs.

## Setup

Simply add the module to the destination directory.

## Usage

Run `Logger.foo("text")` where `foo` is the log level.

The following log levels are currently supported:
* debug
* info
* success
* error

### Configuration

To disable all logging output, change the value of the variable `print_logs` in `logger.py` to `False`.

Output is formatted like so:
```
[ 2016-12-24 22:44:41 | DEBUG   ] Message sent.
```
