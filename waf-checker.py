#!/usr/bin/env python

"""Return if a domain is proected by a Web Application Firewall (WAF).

Usage:
  waf-checker inspect (--website-file FILE) [--export-json] [--export-csv] [-vd]
  waf-checker --version
  waf-checker --help

Modes of operation:
  inspect                         Display if site is protected by a WAF.

Options:
  -h, --help                    Show this help message and exit.
  --version                     Display version info and exit.
  -w FILE, --website-file FILE  List of websites / urls to check in JSON format. (../big_data_london_exhibitors.json)
  --export-json                 Exports results to a JSON file.
  --export-csv                  Exports results in CSV format.
  -v, --verbose                 Log to activity to STDOUT at log level INFO.
  -d, --debug                   Increase log level to 'DEBUG'. Implies '--verbose'.

"""
import logging
import docker

from docopt import docopt

def get_logger(args):
    """
    Setup basic logging.
    Return logging.Logger object.
    """
    # log level
    log_level = logging.CRITICAL
    # if args['--verbose'] or args['check']:
    #     log_level = logging.INFO
    # if args['--debug']:
    #     log_level = logging.DEBUG
    #
    # log_format = '%(name)s: %(levelname)-9s%(message)s'
    # if args['--debug']:
    #     log_format = '%(name)s: %(levelname)-9s%(funcName)s():  %(message)s'
    # if (('--export-json' in args and not args['--export-json']) and not args['check']):
    #     log_format = '[dryrun] %s' % log_format

    # logFormatter = logging.Formatter(log_format)
    rootLogger = logging.getLogger()
    rootLogger.setLevel(log_level)

    #add console appened
    consoleHandler = logging.StreamHandler()
    # consoleHandler.setFormatter(logFormatter)

    rootLogger.addHandler(consoleHandler)

    return rootLogger

def main():
    args = docopt(__doc__, version='1.0')
    log = get_logger(args)
    client = docker.from_env()
    env_vars = {'HOST':'https://osodevops.io'}
#     volumes = {host_dir:
#                    {'bind': container_dir, 'mode': 'rw'}},
# environment = {'ETAS_MEM_GB': '14',
#                'ETAS_LAUNCHER': '/run_dir',
#                'ETAS_OUTPUT': '/run_dir/user_output',
#                'ETAS_THREADS': '3'},

    container = client.containers.run(
        'osodevops/wafw00f',
        'https://osodevops.io',
        detach=True,
        auto_remove=True,
        environment=env_vars)
    for line in container.logs(stream=True):
        print(line.decode("utf-8").strip())


if __name__ == "__main__":
    main()

