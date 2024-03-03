import sqlite3
import csv
import re
import requests as req
from steam import Steam
from decouple import config
import time
from bs4 import BeautifulSoup
from timeit import default_timer as timer
import datetime
import shutil
import os

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

DB_PATH = "data/steam_games.db"


def create_snapshot_file(file_name, backup_name):
    if os.path.isfile(backup_name):
        os.remove(backup_name)

    shutil.copy2(file_name, backup_name)


def remove_html_tags(input):
    soup = BeautifulSoup(input, 'html.parser')
    return soup.get_text()


def check_missing_values(db_cur, table):
    """ Outputs the missing values for each column of a table

    Args:
        db_cur: database cursor
        table: table to be checked

    Returns:
        columns with missing values
    """
    missing_values = {}

    query = f"select name from pragma_table_info('{table}');"
    db_cur.execute(query)
    result = db_cur.fetchall()
    attributes = [x[0] for x in result]

    for column_name in attributes:
        query_total = f"SELECT COUNT(*) FROM {table};"
        query_null = f"SELECT COUNT(*) FROM {table} WHERE {column_name} IS NULL;"

        db_cur.execute(query_total)
        total_rows = db_cur.fetchone()[0]

        db_cur.execute(query_null)
        null_rows = db_cur.fetchone()[0]

        percentage_null = (null_rows / total_rows) * 100 if total_rows > 0 else 0

        missing_values[column_name] = {
            'total_rows': total_rows,
            'null_rows': null_rows,
            'percentage_null': percentage_null
        }

    print("----- Null Values Summary ----- ")
    for column, info in missing_values.items():
        total_rows = info['total_rows']
        null_rows = info['null_rows']
        percentage_null = info['percentage_null']

        print(f"Column '{column}' has {null_rows} null values - {percentage_null:.2f}%.")
    print()

    return [column for column, info in missing_values.items() if info['null_rows'] > 0]


def populate_from_csv(db_cur, csv_path, table):
    """Reads from CSV File and inserts it into an SQLite3 Table

    Args:
        db_cur: database cursor
        csv_path: file path
        table: table name
    """
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    attributes = data[0]
    data = data[1:]

    query_aux = "("
    for attr in attributes:
        query_aux += attr + ", "

    query_aux = query_aux[:-2] + ")"

    values_aux = "("
    for attr in attributes:
        values_aux += "?, "

    values_aux = values_aux[:-2] + ")"

    for row in data:
        db_cur.execute(f"INSERT INTO {table} {query_aux} values {values_aux}", row)


def standardize_nulls(conn, db_cur):
    """Parse all columns so null values have the same representation
    Args:
        conn: database connection
        db_cur: database cursor
    """

    query = f"select name from pragma_table_info('Game');"
    db_cur.execute(query)
    result = db_cur.fetchall()
    result = [x[0] for x in result]

    for column in result:
        update_query = f'''
                        UPDATE Game
                        SET {column} = null
                        WHERE {column} = '' or {column} = '-';
                        '''
        db_cur.execute(update_query)
    conn.commit()


def create_raw_db(conn, db_cur):
    """Creates SQLite3 Database

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Creating raw sqlite database...")

    query_cont = '''
            CREATE TABLE IF NOT EXISTS GameContentWOPk (
                url TEXT,
                desc TEXT,
                full_desc TEXT,
                requirements TEXT,
                popu_tags TEXT
            )
        '''

    query_data = '''
            CREATE TABLE IF NOT EXISTS GameDataWOPk (
                url TEXT,
                name TEXT,
                categories TEXT,
                img_url TEXT,
                user_reviews TEXT,
                all_reviews TEXT,
                date TEXT,
                developer TEXT,
                publisher TEXT,
                price TEXT,
                pegi TEXT,
                pegi_url TEXT
            )
        '''

    db_cur.execute(query_cont)
    db_cur.execute(query_data)

    populate_from_csv(db_cur, 'data/text_content.csv', "GameContentWOPk")
    populate_from_csv(db_cur, 'data/steam_data.csv', "GameDataWOPk")
    conn.commit()

    # create_snapshot_file(DB_PATH, 'data/steam_games_raw.db')


def remove_duplicates_url(conn, db_cur):
    """Removes Duplicates based on URL

    Args:
        conn: database cursor
        db_cur: database connection
    """

    print("Removing duplicates...")

    if SHOW_DETAILED_INFO:
        initial_gamecontent_count = db_cur.execute('SELECT COUNT(*) FROM GameContentWOPk').fetchone()[0]

    query_cont = '''
            DELETE FROM GameContentWOPk
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM GameContentWOPk
                GROUP BY url
            );

            CREATE TABLE IF NOT EXISTS GameContent (
                url TEXT,
                desc TEXT,
                full_desc TEXT,
                requirements TEXT,
                popu_tags TEXT,
                PRIMARY KEY (url)
            );

            INSERT INTO GameContent SELECT * FROM GameContentWOPk;

            DROP TABLE GameContentWOPk;
            '''

    db_cur.executescript(query_cont)

    if SHOW_DETAILED_INFO:
        final_gamecontent_count = db_cur.execute('SELECT COUNT(*) FROM GameContent').fetchone()[0]
        initial_gamedata_count = db_cur.execute('SELECT COUNT(*) FROM GameDataWOPk').fetchone()[0]

    query_data = '''
            DELETE FROM GameDataWOPk
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM GameDataWOPk
                GROUP BY url
            );

            CREATE TABLE IF NOT EXISTS GameData(
                url TEXT,
                name TEXT,
                categories TEXT,
                img_url TEXT,
                user_reviews TEXT,
                all_reviews TEXT,
                date TEXT,
                developer TEXT,
                publisher TEXT,
                price TEXT,
                pegi TEXT,
                pegi_url TEXT,
                FOREIGN KEY(url) REFERENCES GameContent(url)
            );

            INSERT INTO GameData SELECT * FROM GameDataWOPk;

            DROP TABLE GameDataWOPk;
            '''

    db_cur.executescript(query_data)

    if SHOW_DETAILED_INFO:
        final_gamedata_count = db_cur.execute('SELECT COUNT(*) FROM GameData').fetchone()[0]
        print("----- Deduplication Summary ----- ")
        print(f"Initial GameContent entry count: {initial_gamecontent_count}")
        print(f"Final GameContent entry count: {final_gamecontent_count}")
        print(f"Initial GameData entry count: {initial_gamedata_count}")
        print(f"Final GameData entry count: {final_gamedata_count} \n")

    conn.commit()

    # create_snapshot_file(DB_PATH, 'data/steam_games_raw_deduplicated.db')


def merge_raw(conn, db_cur):
    """Merges Two Tables into a single Game Table. (Joins on URL)

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Merging raw database tables...")

    query = '''
    

          CREATE TABLE IF NOT EXISTS Game(
                url TEXT,
                name TEXT,
                categories TEXT,
                img_url TEXT,
                user_reviews TEXT,
                all_reviews TEXT,
                date TEXT,
                developer TEXT,
                publisher TEXT,
                price TEXT,
                pegi TEXT,
                pegi_url TEXT,
                desc TEXT,
                full_desc TEXT,
                requirements TEXT,
                popu_tags TEXT,
                PRIMARY KEY (url)
          );
          
          INSERT INTO Game SELECT * FROM GameData NATURAL JOIN GameContent;
          
          DROP TABLE GameContent;
          
          DROP TABLE GameData;
    '''

    db_cur.executescript(query)
    conn.commit()

    # create_snapshot_file(DB_PATH, 'data/steam_games_raw_merged.db')


def drop_columns(conn, db_cur, useless_columns):
    """Drops useless columns from the database

    Args:
        conn: database cursor
        db_cur: database connection
        useless_columns: list containing string names of the columns to drop
    """
    print(f"Dropping column(s) {', '.join(useless_columns)}...")

    for column in useless_columns:
        query = f"ALTER TABLE Game DROP {column};"
        db_cur.executescript(query)

    conn.commit()


def remove_useless_information(conn, db_cur):
    """Removes most of the game entries that are related to extra content, like DLCs, OSTs, Packs, Editions, Cosmetic packs

    Args:
        conn: database cursor
        db_cur: database connection
    """

    print("Removing extra content (DLCs, OSTs, Packs, Editions, Cosmetic packs, etc) entries...")

    if SHOW_DETAILED_INFO:
        initial_game_count = db_cur.execute('SELECT COUNT(*) FROM Game').fetchone()[0]

    query = '''
            --Delete games with same url but diff snr data
            DELETE FROM Game
            WHERE url NOT IN (
                SELECT MIN(url)
                FROM Game
                GROUP BY REPLACE(url, SUBSTR(url, INSTR(url, '?')), '')
            );
            -- Delete games with same name but different urls -> most likely dlcs, soundtracks or pack
            DELETE FROM Game
            WHERE url NOT IN (
                SELECT url
                FROM (
                    SELECT url, ROW_NUMBER() OVER (PARTITION BY name ORDER BY url) AS row_num
                    FROM Game
                ) t
                WHERE t.row_num = 1
            );

            DELETE FROM Game
            WHERE name LIKE '%DLC%' OR 
            name LIKE '%Soundtrack%' OR 
            name LIKE "% OST %" OR
            name LIKE '%Original Sound Track%' OR
            name LIKE '%pack%' OR 
            name LIKE '%edition%' OR 
            name LIKE '%expansion%' OR
            name LIKE '%pdf%' OR
            name LIKE "%wallpaper%" OR
            name LIKE "%artbook%" OR
            name LIKE "%bundle%" OR
            name LIKE "%demo" OR 
            name LIKE "%accessory set%" OR
            name LIKE "%cosmetic%" OR
            name LIKE "%pass";
            '''
    db_cur.executescript(query)

    if SHOW_DETAILED_INFO:
        final_game_count = db_cur.execute('SELECT COUNT(*) FROM Game').fetchone()[0]
        print("----- Information deletion Summary ----- ")
        print(f"Initial Game entry count: {initial_game_count}")
        print(f"Final Game entry count: {final_game_count}\n")

    conn.commit()
    # create_snapshot_file(DB_PATH, 'data/steam_games_useless.db')


def remove_null_values(conn, db_cur, minimum):
    """Removes entries with more than <minimum> null entries

    Args:
        conn: database cursor
        db_cur: database connection
        minimum: minimum number of null values
    """

    print(f"Removing rows with {minimum} or more null values...")

    # attrs_with_nulls = check_missing_values(db_cur,"Game")

    query = f'''
            DELETE FROM Game
            WHERE (
                (url IS NULL) +
                (name IS NULL) +
                (categories IS NULL) +
                (all_reviews IS NULL) +
                (date IS NULL) +
                (developer IS NULL) +
                (price IS NULL) +
                (desc IS NULL) +
                (full_desc IS NULL) +
                (requirements IS NULL)
            ) >= {minimum};
    '''

    db_cur.execute(query)
    conn.commit()
    # create_snapshot_file(DB_PATH, 'data/steam_games_some_nulls.db')


def fill_null_values_from_steam_api(conn, db_cur):
    """Fetches missing data from STEAM API and fills the database with the respective information

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Fetching missing information...")
    # https://store.steampowered.com/appreviews/{game_id}?json=1&language=all

    sql_to_api_filter_map = {
        "name": "basic,",
        "categories": "categories,",
        "date": "release_date,",
        "developer": "developers,",
        "price": "price_overview,",
        "desc": "basic,",
        "full_desc": "basic,",
        "requirements": "basic,",
    }

    sql_to_api_response_map = {
        "name": "name",
        "categories": "categories",
        "date": "release_date,date",
        "developer": "developers",
        "price": "price_overview,initial",
        "desc": "short_description",
        "full_desc": "detailed_description",
        "requirements": "pc_requirements,minimum",
    }

    query = f'''SELECT url, GROUP_CONCAT(column_name) AS null_columns
                FROM (
                SELECT url, 'url' AS column_name FROM Game WHERE url IS NULL
                UNION ALL SELECT url, 'name' AS column_name FROM Game WHERE name IS NULL
                UNION ALL SELECT url, 'categories' AS column_name FROM Game WHERE categories IS NULL
                UNION ALL SELECT url, 'all_reviews' AS column_name FROM Game WHERE all_reviews IS NULL
                UNION ALL SELECT url, 'date' AS column_name FROM Game WHERE date IS NULL
                UNION ALL SELECT url, 'developer' AS column_name FROM Game WHERE developer IS NULL
                UNION ALL SELECT url, 'price' AS column_name FROM Game WHERE price IS NULL
                UNION ALL SELECT url, 'desc' AS column_name FROM Game WHERE desc IS NULL
                UNION ALL SELECT url, 'full_desc' AS column_name FROM Game WHERE full_desc IS NULL
                UNION ALL SELECT url, 'requirements' AS column_name FROM Game WHERE requirements IS NULL
                ) t
                GROUP BY url;'''

    db_cur.execute(query)
    missing = db_cur.fetchall()

    retry_attempt_time_seconds = 3
    api_call_nr = 0

    if SHOW_DETAILED_INFO:
        print(f"Number of rows with missing infomation: {len(missing)}")

    for row in missing:

        url = row[0]
        columns = row[1].split(",")
        game_id = re.search(r"/app/(\d+)/", url).group(1)

        filters = []
        for column in columns:
            if column == "all_reviews": continue
            filters.append(sql_to_api_filter_map[column])

        filters_text = "".join(filters)
        # api_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}&l=english&cc=US&filters={filters_text}"

        # response = req.get(api_url)
        # if(response.status_code != 200): continue

        # responseData = response.json()
        api_call_nr += 1
        try:
            responseData = steam.apps.get_app_details(game_id, filters=filters_text)
        except:
            print(f"Couldn't execute API Call #{api_call_nr}/{len(missing)}. Ignoring.")
            continue

        first = True
        while (responseData == None):
            # response = req.get(api_url)
            # if(response.status_code != 200): continue
            # responseData = response.json()
            if SHOW_DETAILED_INFO:
                if first:
                    print()
                    first = False
                print(f"Unable to fecth game id {game_id}. Retrying in: {retry_attempt_time_seconds} seconds")
            time.sleep(retry_attempt_time_seconds)
            try:
                responseData = steam.apps.get_app_details(game_id, filters=filters_text)
            except:
                print(f"Couldn't execute API Call #{api_call_nr}/{len(missing)}. Retrying.")
                continue
        if not responseData[f'{game_id}']['success']: continue

        if SHOW_DETAILED_INFO:
            print(f"\nAPI Call #{api_call_nr}/{len(missing)}")
            print(f"Game ID: {game_id}")

        data = responseData[f'{game_id}']['data']
        for column in columns:
            if column == "all_reviews":
                info = fetch_reviews_api(game_id)
            else:
                json_entries = sql_to_api_response_map[column].split(",")
                info = dict(data)

                for entry in json_entries:
                    try:
                        info = info[entry]
                    except:
                        info = None
                        break

                if column == "categories" and info is not None:
                    cats = info
                    info = []

                    for cat in cats:
                        info.append(cat['description'].lower())

                    info = standardize_categories(info)

                if column == "price" and info is not None:
                    info = float(int(info) / 100)

                if (column == "desc" or column == "full_desc") and info is not None:
                    info = remove_html_tags(info)

                if column == "requirements" and info is not None:
                    info = remove_html_tags(info)
                    info = get_system_requirements(info)

            if type(info) == list:
                info = info[0]

            if info in ["", " ", "-"]:
                info = None

            if SHOW_DETAILED_INFO:
                print(f"Column: {column} -> Fetched data: \"{info}\"")

            update_query = f'''UPDATE Game SET {column} = ? WHERE url = ?;'''
            db_cur.execute(update_query, (info, url))

    conn.commit()
    # create_snapshot_file(DB_PATH, 'data/steam_games_no_nulls.db')


def parse_price(conn, db_cur):
    """Parses the price column to the format of a FLOAT.

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Parsing 'price' column values...")
    db_cur.execute('SELECT rowid, price FROM Game WHERE price is not NULL')
    rows = db_cur.fetchall()

    NTD_TO_USD_FACTOR = 0.031

    for row in rows:
        is_ntd = False
        rowid, price = row

        if 'Free' in price:
            new_price = '0'

        else:
            if "NT$" in price:
                is_ntd = True
            match = re.search(r'\$\s*([\d.]+)', price)
            if match:
                new_price = match.group(1)
                if is_ntd:
                    new_price = str(float(new_price) * NTD_TO_USD_FACTOR)
            else:
                new_price = '0'

        db_cur.execute('UPDATE Game SET price = ? WHERE rowid = ?', (new_price, rowid))

    conn.commit()


def parse_categories(conn, db_cur):
    """Parses the categories column

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Parsing 'categories' column values...")

    db_cur.execute('SELECT rowid, categories FROM Game where categories is not NULL')
    rows = db_cur.fetchall()

    for row in rows:
        rowid, categories = row
        categories = categories.lower()
        new_categories = ''
        if 'single-player' in categories or 'singleplayer' in categories:
            new_categories += 'Single-player;'
        if 'multi-player' in categories or 'multiplayer' in categories:
            new_categories += 'Multi-player;'
        if 'online pvp' in categories:
            new_categories += 'Online PvP;'
        if 'online co-op' in categories or 'online coop' in categories:
            new_categories += 'Online Co-op;'
        if 'lan pvp' in categories:
            new_categories += 'LAN PvP;'
        if 'lan co-op' in categories:
            new_categories += 'LAN Co-op;'
        if 'mmo' in categories:
            new_categories += 'MMO;'
        if 'shared/split screen pvp' in categories:
            new_categories += 'Shared/Split Screen PvP;'
        if new_categories == '':
            new_categories = 'Other;'

        db_cur.execute('UPDATE Game SET categories = ? WHERE rowid = ?', (new_categories, rowid))

    conn.commit()


def standardize_categories(categories):
    """Parses the categories column

    Args:
        :param categories: list of categories
    """

    new_categories = ''
    if categories is None:
        new_categories = 'Other;'
    else:
        if 'single-player' in categories or 'singleplayer' in categories:
            new_categories += 'Single-player;'
        if 'multi-player' in categories or 'multiplayer' in categories:
            new_categories += 'Multi-player;'
        if 'online pvp' in categories:
            new_categories += 'Online PvP;'
        if 'online co-op' in categories or 'online coop' in categories:
            new_categories += 'Online Co-op;'
        if 'lan pvp' in categories:
            new_categories += 'LAN PvP;'
        if 'lan co-op' in categories:
            new_categories += 'LAN Co-op;'
        if 'mmo' in categories:
            new_categories += 'MMO;'
        if 'shared/split screen pvp' in categories:
            new_categories += 'Shared/Split Screen PvP;'
        if new_categories == '':
            new_categories = 'Other;'

    return new_categories


def parse_reviews(conn, db_cur):
    """Parses the all_reviews column to the desired format

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Parsing 'all_reviews' column values...")

    query = f'''UPDATE Game
                SET all_reviews = 
                CASE
                    WHEN all_reviews LIKE '%Positive%' OR all_reviews LIKE '%Negative%' THEN
                        (SUBSTR(all_reviews, INSTR(all_reviews, '-') + 2, INSTR(all_reviews, '%') - INSTR(all_reviews, '-') - 2))
                    ELSE null
                END;
                
                UPDATE Game
                SET user_reviews = 
                CASE
                    WHEN user_reviews LIKE '%Positive%' OR user_reviews LIKE '%Negative%' THEN
                        (SUBSTR(user_reviews, INSTR(user_reviews, '-') + 2, INSTR(user_reviews, '%') - INSTR(user_reviews, '-') - 2))
                    ELSE null
                END;
                
                UPDATE Game
                SET all_reviews = user_reviews
                WHERE all_reviews IS NULL;
                
            '''

    db_cur.executescript(query)
    conn.commit()


def parse_date(conn, db_cur):
    """Parses the dates column to the desired format

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Parsing 'date' column values...")

    query = f'''DELETE FROM Game
                WHERE NOT (date LIKE '___ %, ____' OR date LIKE '% ___, ____');

                DELETE FROM Game
                WHERE NOT (
                    (length(date) = 11) OR 
                    (length(date) = 12)
                );

                UPDATE Game
                SET date = 
                    CASE 
                        WHEN length(date) = 11 THEN 
                            substr(date, 5, 1) || ' ' || substr(date, 1, 3) || ', ' || substr(date, 8,4)
                        WHEN length(date) = 12 THEN 
                            substr(date, 5, 2) || ' ' || substr(date, 1, 3) || ', ' || substr(date, 9,4)
                    END
                WHERE 
                    date LIKE "___ %, ____";

            '''

    db_cur.executescript(query)
    conn.commit()


def parse_developer(conn, db_cur):
    """Parses the developer column. If developer is empty, copy from publisher

        Args:
            conn: database connection
            db_cur: database cursor
    """
    print("Parsing 'developer' column values...")

    db_cur.executescript('''
                        UPDATE Game
                        SET developer = publisher
                        WHERE developer IS NULL;
                        ''')
    conn.commit()


def parse_full_desc(conn, db_cur):
    """Parses the full_desc column. Removes "About This" prefix in all entries.

    Args:
        conn: database connection
        db_cur: database cursor
    """

    print("Parsing 'full_desc' column values...")
    query = '''
            UPDATE Game
            SET full_desc = REPLACE(REPLACE(full_desc, 'About This Game', ''), 'About This Content', '');
    '''

    db_cur.executescript(query)
    conn.commit()


def fetch_reviews_api(game_id):
    """Fetches Reviews from a game

    Args:
        game_id: steam id of game

    Returns:
        The percentage of positive reviews
    """
    # https://store.steampowered.com/appreviews/{game_id}?json=1&language=all
    api_url = f"https://store.steampowered.com/appreviews/{game_id}?json=1&language=all"

    response = req.get(api_url)

    if (response.status_code != 200):
        return None

    responseData = response.json()

    if (responseData['success'] != 1):
        return None

    if (responseData['query_summary']['total_reviews'] == 0):
        return None
    res = int(
        round(responseData['query_summary']['total_positive'] / responseData['query_summary']['total_reviews'] * 100,
              0))
    return res


def cast_table_types(conn, db_cur):
    """Alters the Table to the appropriate types

    Args:
        conn: database connection
        db_cur: database cursor
    """
    print("Casting column types...")

    db_cur.executescript('''
                        CREATE TABLE IF NOT EXISTS NewGame (
                        url TEXT,
                        name TEXT,
                        categories TEXT,
                        all_reviews INTEGER,
                        date TEXT,
                        developer TEXT,
                        price REAL,
                        desc TEXT,
                        full_desc TEXT,
                        requirements TEXT,
                        PRIMARY KEY (url)
                        );
                        
                        INSERT INTO NewGame (
                            url, name, categories, all_reviews, date, 
                            developer, price, desc, full_desc, requirements
                        )
                        SELECT 
                            url, name, categories, CAST(all_reviews AS INTEGER), date, 
                            developer, CAST(price AS REAL), desc, full_desc, requirements
                        FROM Game;
                        
                        DROP TABLE IF EXISTS Game;      
                        
                        ALTER TABLE NewGame RENAME TO Game;
                        
                         ''')

    conn.commit()


def replace_null_values_in_price(conn, db_cur):
    """Replaces the null values in price by the respective average

    Args:
        conn: database connection
        db_cur: database cursor
    """
    query = '''
            UPDATE Game
            SET price = (
                SELECT AVG(price)
                FROM Game
                WHERE price IS NOT NULL
            )
            WHERE price IS NULL;
            '''

    db_cur.executescript(query)
    conn.commit()


def find_words_in_text(text, attributes):
    found_attributes = {}

    for attr in attributes:
        pattern = re.compile(rf"{attr}:\s*(.*?)(?=\w+:|$)", re.DOTALL)
        match = pattern.search(text)

        if match:
            found_attributes[attr] = match.group(1).strip()

    return found_attributes


def get_system_requirements(text):
    # Split the text into minimum and recommended sections
    if "Recommended:" in text:
        sections = re.split(r'Recommended:', text)
        minimum_section = sections[0]
        recommended_section = sections[1]
    else:
        minimum_section = text
        recommended_section = ""

    minimum_requirements = {}
    recommended_requirements = {}

    attributes = ["OS", "Processor", "Memory", "Graphics", "Storage", "DirectX", "Network", "Sound Card",
                  "Additional Notes"]

    # Find the words in the minimum section of the text
    requirements_found = find_words_in_text(minimum_section, attributes)

    minimum_requirements.update(requirements_found)

    if (recommended_section != ""):
        # Find the words in the recommended section of the text
        requirements_found = find_words_in_text(recommended_section, attributes)
        recommended_requirements.update(requirements_found)

    if (minimum_requirements != {}):
        text = "Minimum:"
        for key, value in minimum_requirements.items():
            text += f"\n{key}: {value}"

    if (recommended_requirements != {}):
        text += "\nRecommended:"
        for key, value in recommended_requirements.items():
            text += f"\n{key}: {value}"

    return text


def parse_system_requirements(conn, db_cur):
    """Parses the requirements column. """
    print("Parsing 'requirements' column values...")
    db_cur.execute('SELECT rowid, requirements FROM Game where requirements is not NULL')
    rows = db_cur.fetchall()

    for row in rows:
        rowid, requirements = row
        new_requirements = get_system_requirements(requirements)
        db_cur.execute('UPDATE Game SET requirements = ? WHERE rowid = ?', (new_requirements, rowid))

    conn.commit()


def main():
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    db_cur = conn.cursor()

    detailed_info_input = input("Display detailed information (Y/N): ").upper()
    while detailed_info_input not in ["Y", "N"]:
        detailed_info_input = input("Display detailed information (Y/N): ").upper()

    global SHOW_DETAILED_INFO
    SHOW_DETAILED_INFO = True if detailed_info_input == "Y" else False

    start = timer()

    current_start_time = datetime.datetime.now()
    print(f"\nInitializing pipeline at {current_start_time}...")

    # Create Database
    create_raw_db(conn, db_cur)

    # Data Cleaning Phase 1
    remove_duplicates_url(conn, db_cur)
    merge_raw(conn, db_cur)
    drop_columns(conn, db_cur, ["pegi", "pegi_url", "img_url", "popu_tags"])
    remove_useless_information(conn, db_cur)
    standardize_nulls(conn, db_cur)

    # Data Transformation
    parse_price(conn, db_cur)
    parse_full_desc(conn, db_cur)
    parse_categories(conn, db_cur)
    parse_date(conn, db_cur)
    parse_system_requirements(conn, db_cur)
    parse_reviews(conn, db_cur)
    parse_developer(conn, db_cur)
    drop_columns(conn, db_cur, ["publisher", "user_reviews"])
    cast_table_types(conn, db_cur)
    standardize_nulls(conn, db_cur)

    # Data Cleaning Phase 2
    if SHOW_DETAILED_INFO: check_missing_values(db_cur, "Game")
    remove_null_values(conn, db_cur, 3)
    if SHOW_DETAILED_INFO: check_missing_values(db_cur, "Game")

    # Data Integration
    fill_null_values_from_steam_api(conn, db_cur)
    if SHOW_DETAILED_INFO: check_missing_values(db_cur, "Game")

    conn.close()

    end = timer()
    elapsed = end - start

    current_end_time = datetime.datetime.now()
    print(f"Pipeline finalized at {current_end_time} in {elapsed} seconds!")

    final_db_path = "data/steam_games_final.db"
    if os.path.isfile(final_db_path):
        os.remove(final_db_path)
    create_snapshot_file(DB_PATH, final_db_path)


main()
