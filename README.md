# trytond-upgrade

Script to automate database migration between Tryton versions.

## Setup

This repository must be placed at the root of your Tryton project:

```
tryton/
├── trytond/
├── trytond-upgrade/
│   ├── upgrade.py
│   ├── before/
│   │   ├── before.yml
│   │   └── *.sql / *.py
│   └── after/
│       ├── after.yml
│       └── *.sql / *.py
└── ...
```

## Usage

```bash
python3 ./trytond-upgrade/upgrade.py -d <database> -c <config_file> <from_version> <to_version>
```

### Arguments

| Argument | Description |
|---|---|
| `-d`, `--database` | Target database name |
| `-c`, `--config` | Tryton configuration file |
| `from_version` | Current version of the database |
| `to_version` | Target version to upgrade to |

### Example

```bash
python3 ./trytond-upgrade/upgrade.py -d mydb -c /etc/trytond.conf 7.2 7.8
```

## How it works

The upgrade process runs in three phases:

1. **Before** — Executes SQL operations defined in `before/before.yml` that must run before `trytond-admin`
2. **trytond-admin** — Runs `trytond-admin --all` to perform the standard Tryton module update
3. **After** — Executes SQL operations defined in `after/after.yml` that must run after `trytond-admin`

Operations are filtered by version range: only operations where `from_version < version <= to_version` are executed. If an operation specifies `modules`, it will only run if all those modules are activated in the database.

## Pending improvements

See the [TODO](TODO) file for known limitations and planned features.
