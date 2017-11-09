# Author: Punkenhofer Mathias
# Mail: code.mpunkenhofer@gmail.com
# Date: 25.10.2017

from MorasConverter import MorasConverter
from MorasConverter import ConversionError
from pathlib import Path
import sqlite3
import json
import time
import sys
import argparse

errors_enabled = False


def file_exists(file_name):
    if Path(file_name).is_file():
        return True
    else:
        return False


def create_db(connection):
    c = connection.cursor()

    # Tables
    c.execute(
        '''CREATE TABLE [items] ( [id] INTEGER PRIMARY KEY ON CONFLICT ABORT AUTOINCREMENT, [name] VARCHAR2(150) NOT NULL ON CONFLICT ABORT, [nameoriginal] VARCHAR2(150), [origin] BLOB, [description] BLOB, [onlineurl] VARCHAR2(250), [extension] VARCHAR2(10), [provider] VARCHAR2(100), [classrestrictions] VARCHAR2(250), [effects] VARCHAR2(250), [realm] INT NOT NULL ON CONFLICT ABORT, [position] INT NOT NULL ON CONFLICT ABORT, [type] INT NOT NULL ON CONFLICT ABORT, [level] INT, [quality] INT, [bonus] INT, [class] INT, [subclass] INT, [material] INT, [af] INT, [dps] INT, [speed] INT, [maxlevel] INT, [damagetype] INT, [lastupdate] INT)''')
    c.execute('''CREATE TABLE [morasversion] ( [dbversion] INT NOT NULL ON CONFLICT ABORT)''')

    # Indices
    c.execute('''CREATE INDEX [idxExtension] ON [items] ([extension])''')
    c.execute('''CREATE INDEX [idxName] ON [items] ([name])''')
    c.execute('''CREATE INDEX [idxPosition] ON [items] ([position])''')
    c.execute('''CREATE INDEX [idxProvider] ON [items] ([provider])''')
    c.execute('''CREATE INDEX [idxRealm] ON [items] ([realm])''')

    # Moras Version
    c.execute("Insert INTO morasversion VALUES ('3')")

    # Save
    connection.commit()


# source: https://stackoverflow.com/questions/6169217/replace-console-output-in-python
def progress_bar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def convert(db, json, converter):
    c = db.cursor()
    items = json["items"]

    print('Converting... there are %d items to convert.' % len(items))

    timestamp = str(int(time.time()))
    errors = []
    converted_items = 0

    for i, item in enumerate(items):
        try:
            db_item = (   # id
                          i + 1,
                          # name
                          converter.name(item),
                          # orig name (never used)
                          '',
                          # origin
                          converter.origin(item),
                          # description.
                          converter.description(item),
                          # url
                          'https://github.com/mpunkenhofer/MorasDBConverter',
                          # patch (do not use - causes moras to crash)
                          '',
                          # provider
                          'Neca',
                          # class restrictions
                          converter.class_restriction(item),
                          # effects / stats
                          converter.bonuses(item),
                          # realm
                          converter.realm(item),
                          # position
                          converter.slot(item),
                          # type
                          converter.type(item),
                          # level
                          converter.level(item),
                          # quality
                          converter.quality(item),
                          # bonus
                          converter.bonus(item),
                          # class
                          converter.item_class(item),
                          # subclass
                          converter.subclass(item),
                          # material
                          converter.material(item),
                          # armor factor
                          converter.armor_factor(item),
                          # dps
                          converter.dps(item),
                          # speed
                          converter.speed(item),
                          # max level
                          converter.max_level(item),
                          # damage type
                          converter.damage_type(item),
                          # last update
                          timestamp
                      )

        except NotImplementedError as e:
            errors.append('Not Implemented Error: ' + e)
        except ConversionError as e:
            errors.append('Conversion Error: ' + e)
        except KeyError as e:
            errors.append('Error: ' + e)
        else:
            c.execute("Insert INTO items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", db_item)
            converted_items += 1

        # only update progress bar once every 100 items
        if i % 100 == 0:
            progress_bar(i, len(items))

    # done
    progress_bar(len(items), len(items))

    if errors_enabled:
        print('\nError Report: %d errors\n' % len(errors))
        for e in errors:
            print(e)
        print()

    print('\nConverted %d of %d items' % (converted_items, len(items)))


def main():
    parser = argparse.ArgumentParser(description='Converts a .json daoc db to moras db format.')

    parser.add_argument('database', type=str, help='daoc item database file (.json)')
    parser.add_argument('metadata', type=str, help='daoc item database metadata file (.json)')
    parser.add_argument('-o', '--output', type=str, default='items.db3', help='output file name (moras database)')
    parser.add_argument('-e', '--errors', help='display conversion errors', action='store_true')
    parser.add_argument('-i', '--ignore', metavar='ID', nargs='+', type=int, help='ignore item(s) with a matching ID')

    args = parser.parse_args()

    if not file_exists(args.database):
        print("Error: database file '%s' does not exists." % args.database)
        return 1

    if not file_exists(args.metadata):
        print("Error: metadata file '%s' does not exists." % args.metadata)
        return 1

    if file_exists(args.output):
        print("Error: output file '%s' already exists." % args.output)
        return 1

    print("Creating database '%s' ..." % args.output)
    connection = sqlite3.connect(args.output)
    create_db(connection)

    with open(args.database) as json_file:
        print("Loading '%s' ..." % args.database)
        data = json.load(json_file)
        print("Done loading '%s' ..." % args.database)

        convert(connection, data, MorasConverter(args.metadata))

    # Close
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
