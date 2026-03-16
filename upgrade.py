#!/usr/bin/env python3
import argparse
import importlib
import os
import pathlib
import subprocess

import psycopg2
from trytond.config import config as CONFIG, parse_uri


def parse_args():
    parser = argparse.ArgumentParser(description="Tryton Upgrade")
    parser.add_argument(
        "database", nargs=1, help="Database to upgrade")
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
    ops = []
    valid_ops = []
    path = pathlib.Path(__file__).parent / phase
    from_version = args.from_version[0]
    to_version = args.to_version[0]

    for file in sorted(path.glob('*.py')):
        spec = importlib.util.spec_from_file_location(file.stem, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "OPERATIONS"):
            ops.extend(module.OPERATIONS)

        for op in ops:
            version = op.get("version")
            if version > from_version and version <= to_version:
                valid_ops.append(op)

    return valid_ops


def run_sql(cursor, op):
    modules = op.get("modules")
    sql = op.get("sql")

    if not modules or all(module_activated(cursor, m) for m in modules):
        print(f"RUNNING: {op.get('version'), op.get('name')}")
        cursor.execute(sql)


def run_script(cursor, op):
    pass # TODO: Support scripts


def run_operations(connection, phase, args):
    print(f"Executting {phase.upper()} operations")
    ops = load_operations(phase, args)

    with connection:
        with connection.cursor() as cursor:
            for op in ops:
                if op.get("sql"):
                    run_sql(cursor, op)
                elif op.get("script"):
                    run_script(cursor, op)


def run_trytond_admin(dbname, config_file):
    print("RUNNING trytond-admin")
    subprocess.run(
        ['trytond-admin', '-d', dbname, '-c', config_file, '--all', '-v'],
        check=True
        )


def main():
    args = parse_args()
    if args.config:
        config_file = args.config
    else:
        raise FileNotFoundError("Missing configuration file.")
    dbname = args.database[0]
    print("Connecting to database...")
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
    print("Upgrade completed.")


if __name__ == "__main__":
    main()
