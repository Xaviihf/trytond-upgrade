#!/usr/bin/env python3
import argparse
import logging
import os
import pathlib
import subprocess

import yaml

logger = logging.getLogger(__name__)

import psycopg2
from trytond.config import config as CONFIG, parse_uri


def parse_args():
    parser = argparse.ArgumentParser(description="Tryton Upgrade")
    parser.add_argument(
        "-d", "--database", required=True, help="Database to upgrade")
    parser.add_argument(
        "from_version", nargs=1, help="Actual version of the database")
    parser.add_argument(
        "to_version", nargs=1, help="Target version to upgrade")
    parser.add_argument(
        "-c", "--config", default=None, help="Config file")
    return parser.parse_args()


def get_url(config_file=None):
    if config_file:
        CONFIG.update_etc(config_file)
        url = parse_uri(CONFIG.get("database", "uri"))
    else:
        url = parse_uri(os.environ.get('TRYTOND_DATABASE__URI', ''))
    return url


def module_activated(cursor, module_name):
    cursor.execute("""
        SELECT state FROM ir_module WHERE name = %s
        """, (module_name,))
    result = cursor.fetchone()
    return bool(result and result[0] == 'activated')


def load_operations(phase, args):
    valid_ops = []
    path = pathlib.Path(__file__).parent / phase
    from_version = args.from_version[0]
    to_version = args.to_version[0]

    yml_file = path / f"{phase}.yml"
    with open(yml_file, 'r') as f:
        data = yaml.safe_load(f)

    for op in data.get('operations', []):
        sql_file = op.get('sql')
        if sql_file:
            sql_path = path / sql_file
            with open(sql_path, 'r') as f:
                op['sql'] = f.read()

        version = op.get('version')
        if version > from_version and version <= to_version:
            valid_ops.append(op)

    return valid_ops


def run_sql(cursor, op):
    modules = op.get("modules")
    sql = op.get("sql")

    if not modules or all(module_activated(cursor, m) for m in modules):
        logger.info("RUNNING: %s, %s", op.get('version'), op.get('name'))
        cursor.execute(sql)


def run_script(cursor, op):
    pass # TODO: Support scripts


def run_operations(connection, phase, args):
    logger.info("Executing %s operations", phase.upper())
    ops = load_operations(phase, args)

    with connection:
        with connection.cursor() as cursor:
            for op in ops:
                if op.get("sql"):
                    run_sql(cursor, op)
                elif op.get("script"):
                    run_script(cursor, op)


def run_trytond_admin(dbname, config_file):
    logger.info("Running trytond-admin")
    subprocess.run(
        ['trytond-admin', '-d', dbname, '-c', config_file, '--all', '-v'],
        check=True
        )


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='trytond-upgrade %(levelname)s %(message)s',
        )
    args = parse_args()
    if args.config:
        config_file = args.config
    else:
        raise FileNotFoundError("Missing configuration file.")
    dbname = args.database
    logger.info("Connecting to database")
    url = get_url(config_file)
    if url.username:
        connection = psycopg2.connect(
            dbname=dbname,
            host=url.hostname,
            port=url.port, user=url.username,
            password=url.password)
    else:
        connection = psycopg2.connect(dbname=dbname)

    run_operations(connection, 'before', args)
    connection.commit()
    run_trytond_admin(dbname, config_file)

    run_operations(connection, 'after', args)
    connection.commit()
    run_trytond_admin(dbname, config_file)

    connection.close()
    logger.info("Upgrade completed.")


if __name__ == "__main__":
    main()
