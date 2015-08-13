# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import logging
import os
import json
import csv
import pycountry
import time
import shutil

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO)
START_TIME = time.time()

def download():
    """
    Caches multiple Wikipedia country code pages as a single json file to parse in
    transformation process.
    """
    if not os.path.exists(ARGS.filepath + '/cache'):
        os.makedirs(ARGS.filepath + '/cache')

    if not os.path.exists(ARGS.filepath + '/data'):
        os.makedirs(ARGS.filepath + '/data')

    # get OKF source
    if not os.path.exists(ARGS.filepath + '/cache/okf_country_codes_cache.csv'):
        okf = 'https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv'
        with open(ARGS.filepath + '/cache/okf_country_codes_cache.csv', 'wb') as outfile:
            req = requests.get(okf, stream=True)
            if not req.ok:
                print req.status
            for block in req.iter_content(1024):
                outfile.write(block)
            outfile.close()

    # get OKF source
    if not os.path.exists(ARGS.filepath + '/cache/wu_country_codes_cache.csv'):
        wu = 'https://countrycode.org/customer/countryCode/downloadCountryCodes'
        with open(ARGS.filepath + '/cache/wu_country_codes_cache.csv', 'wb') as outfile:
            req = requests.get(wu, stream=True)
            if not req.ok:
                print req.status
            for block in req.iter_content(1024):
                outfile.write(block)
            outfile.close()

    # get WIKI source
    if not os.path.exists(ARGS.filepath + '/cache/wiki_country_codes_cache.json'):

        pages = ['/wiki/Country_codes:_A']
        wiki = 'https://en.wikipedia.org'
        out_json = {'header':[], 'data': []}

        # Get seed list of pages to parse
        req = requests.get(wiki + pages[0])
        cont = req.content
        seed_soup = BeautifulSoup(cont, 'html.parser')

        seed_index = seed_soup.find('div', 'toc plainlinks hlist').ul.find_all('li')
        for seed in seed_index:
            try:
                pages.append(seed.a.attrs['href'])
            except AttributeError:
                pass

        # parse and cache pages
        for page in pages:
            req = requests.get(wiki + page)
            cont = req.content
            soup = BeautifulSoup(cont, 'html.parser')

            # Get h2 country names
            titles = soup.find_all('h2')
            title_array = []
            for title in titles:
                t_spans = title.find_all('span')
                try:
                    title_array.append(t_spans[0].find('a').attrs['title'])
                except IndexError:
                    pass
                except AttributeError:
                    pass

            # find and parse tables into rows
            tables = soup.find_all('table')
            table_counter = 0
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) != 1:
                    t_obj = {'wiki_name' :title_array[table_counter]}
                    table_counter += 1
                    for row in rows:
                        cells = row.find_all('td')
                        for cell in cells:
                            h_val = cell.a.attrs['title']\
                            .strip()\
                            .lower()\
                            .replace(' ', '_')\
                            .replace('-', '_')\
                            .replace('.', '_')
                            try:
                                out_json['header'].index(h_val)
                            except ValueError:
                                out_json['header'].append(h_val)
                            except:
                                raise

                            # Get values
                            try:
                                val = cell.span.text
                                if val == u"\u2014":
                                    val = val.replace(u"\u2014", u"NULL")
                                else:
                                    val = val.encode('utf-8')
                            except AttributeError:
                                pass

                            t_obj[h_val] = val
                    out_json['data'].append(t_obj)

        out_json['header'] = ['wiki_name'] + out_json['header']

        write_json(out_json)
        elapsed_time = time.time() - START_TIME
        LOGGER.info('Retrieved source data to %s (elapsed time - %d seconds)' % (LOCAL_FILENAME, elapsed_time))
    else:
        LOGGER.info('Data already cached, moving on...')

def transform():
    """
    Transforme cached cached country code data into datapackage for loading into ckan. Source is html 
    and export is flat csv files.
    """
    LOGGER.info('Starting transfromation process of data from: %s' % LOCAL_FILENAME)

    with open(LOCAL_FILENAME) as wiki_json_in:
        wiki_data_in = json.load(wiki_json_in)
        wiki_json_in.close()
    LOGGER.info('WIKI data consists of %d records' % len(wiki_data_in['data']))

    with open(ARGS.filepath + '/cache/wu_country_codes_cache.csv') as wu_csv_in:
        wu_data_in = {'data': []}
        csvreader = csv.reader(wu_csv_in, delimiter=',', quotechar='"')
        wu_data_in['header'] = csvreader.next()
        for row in csvreader:
            wu_data_in['data'].append(row)
        wu_csv_in.close()
    LOGGER.info('WU data consists of %d records' % len(wu_data_in['data']))

    with open(ARGS.filepath + '/cache/okf_country_codes_cache.csv') as okf_csv_in:
        okf_data_in = {'data': []}
        csvreader = csv.reader(okf_csv_in, delimiter=',', quotechar='"')
        okf_data_in['header'] = csvreader.next()
        for row in csvreader:
            okf_data_in['data'].append(row)
        okf_csv_in.close()
    LOGGER.info('OKF data consists of %d records' % len(okf_data_in['data']))

    # Create WU dict
    wu_header = []
    wu_lkey = {}
    wu_data = {}
    for i in range(0, len(wu_data_in['header'])):
        h_val = wu_data_in['header'][i]
        wu_lkey[h_val] = i
        if h_val == 'Country Name'\
         or h_val == 'ISO3'\
         or h_val == 'Top Level Domain'\
         or h_val == 'FIPS'\
         or h_val == 'ISO Numeric'\
         or h_val == 'E164'\
         or h_val == 'Phone Code'\
         or h_val == 'Internet Hosts'\
         or h_val == 'Internet Users'\
         or h_val == 'Phones (Mobile)'\
         or h_val == 'Phones (Landline)'\
         or h_val == 'GDP':
            pass
        else:
            wu_header.append(h_val)
    for row in wu_data_in['data']:
        iso2c = row[wu_lkey['ISO2']]
        wu_data[iso2c] = []
        for i in range(1, len(wu_header)):
            if row[wu_lkey[wu_header[i]]] != '':
                wu_data[iso2c].append(row[wu_lkey[wu_header[i]]])
            else:
                wu_data[iso2c].append('NULL')

    # Create OKF dict
    okf_header = []
    okf_lkey = {}
    okf_data = {}
    for i in range(0, len(okf_data_in['header'])):
        h_val = okf_data_in['header'][i]
        okf_lkey[h_val] = i
        if h_val == 'Country Name'\
         or h_val == 'ISO3'\
         or h_val == 'Top Level Domain'\
         or h_val == 'FIPS'\
         or h_val == 'ISO Numeric'\
         or h_val == 'E164'\
         or h_val == 'Phone Code'\
         or h_val == 'Internet Hosts'\
         or h_val == 'Internet Users'\
         or h_val == 'Phones (Mobile)'\
         or h_val == 'Phones (Landline)'\
         or h_val == 'GDP':
            pass
        else:
            okf_header.append(h_val)
    for row in okf_data_in['data']:
        iso2c = row[okf_lkey['ISO3166-1-Alpha-2']]
        okf_data[iso2c] = []
        for i in range(1, len(okf_header)):
            if row[okf_lkey[okf_header[i]]] != '':
                okf_data[iso2c].append(row[okf_lkey[okf_header[i]]])
            else:
                okf_data[iso2c].append('NULL')

    # parse and merge data from wikipedia
    header = wiki_data_in['header']
    header = ['name'] + header
    wiki_data = wiki_data_in['data']
    # wiki_lkey = {}

    out_data = []
    for row in wiki_data:
        add_array = ['NULL']
        for i in range(1, len(header)):
            add_array.append(row[header[i]])
        try:
            add_array[0] = pycountry.countries.get(alpha2=row['iso_3166_1_alpha_2']).name
        except KeyError:
            add_array[0] = row['wiki_name']
        try:
            add_array = add_array + wu_data[row['iso_3166_1_alpha_2']]
        except KeyError:
            add_array = add_array + (['NULL'] * (len(wu_header) - 1))

        out_data.append(add_array)

    wu_header.remove('ISO2')
    okf_header.remove('ISO3166-1-Alpha-2')
    header = header + wu_header + okf_header

    elapsed_time = time.time() - START_TIME
    LOGGER.info('Transformation complete, writing to %s (elapsed time - %d seconds)' % (ARGS.filepath + '/data/country-codes.csv', elapsed_time))
    write_csv(header, out_data, 'country-codes')

def write_json(data):
    """
    Write parsed html to cached json file for transformation
    """
    with open(LOCAL_FILENAME, 'wb') as output:
        # write json
        json.dump(data, output)
        # close file
        output.close()



def write_csv(header, rows, filename):
    """
    Write rows to a CSV file. Use default dialect for the CSV. If a file name
    is not provided, the rows will be printed to standard output
    """

    # Set the file as stdout if no filename, else open the file for writing
    with open(ARGS.filepath + '/data/' + filename + '.csv', 'wb') as output:
        # Create the csv writer
        csvwriter = csv.writer(output)
        # Write the header
        csvwriter.writerow(header)
        # Write all the rows
        for i in range(0, len(rows)):
            new_array = []
            for cell in rows[i]:
                new_array.append(cell.encode('utf-8'))
            csvwriter.writerow(new_array)
        # Close the output file (or stdout)
        output.close()

def cleanup():
    """
    Erases cahced data
    """
    shutil.rmtree(ARGS.filepath + '/cache')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import argparse
    PARSER = argparse.ArgumentParser(description='Process Country Codes from wikipedia')

    # Output file option
    PARSER.add_argument('-o', '--output', dest='filepath', action='store',\
        default=None, metavar='filepath',\
        help='define output filepath')

    # TODO: create option to reconfigure source url for subpage
    # # Source file option (default is the global source_url)
    # parser.add_argument('-s', '--source', dest='source_url', action='store',
    #     default=source_url, metavar='source_url',
    #     help='source URL to generate output from')

    # Parse the arguments into args
    ARGS = PARSER.parse_args()

    LOCAL_FILENAME = ARGS.filepath + '/cache/wiki_country_codes_cache.json'

    download()
    transform()
    cleanup()
    # elapsed_time = time.time() - START_TIME
    LOGGER.info('ETL process complete: elapsed time - %d seconds' % (time.time() - START_TIME))
