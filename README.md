Comprehensive country code information, including ISO 3166 codes, ITU dialing
codes, ISO 4217 currency codes, and many others. Provided as a Simple Data
Format Data Package.

## Data

###Structure
Main data comes in three sheets or tables: central, general and merged (see notes for description). Each is organized into country-year records with multiple variables. Included is a field dictionary for the entire dataset: var_list.

###Included variables

* **name** - English spelling of name *(string)*
* **name_fr** - French spelling of name *(string)*
* **ISO3166-1-Alpha-2** - [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country ID *(string)*
* **ISO3166-1-Alpha-3** - [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) *(string)*
* **ISO3166-1-numeric** - [ISO 3166-1 numeric](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) *(sting/int)*
* **ITU** - ITU-T Recommendation E.164 assigned country code *(string)*
* **MARC** - MARC 21 two letter country code *(string)*
* **WMO** - World Meteorological two letter country codes *(string)*
* **DS** - Distinguishing signs of vehicles in international traffic (oval bumper sticker codes) *(string)*
* **Dial** - Country code from ITU-T recommendation E.164 (international dialing code), sometimes followed by area code *(string/int)*
* **FIFA** - Codes assigned by the [Fédération Internationale de Football Association](http://www.fifa.com/en/organisation/na/index.html) *(string)*
* **FIPS** -  *()*
* **GAUL** - Global Administrative Unit Layers from the Food and Agriculture Organization *(int)*
* **IOC** - Codes assigned by the [International Olympics Committee](http://www.olympic.org/uk/organisation/noc/index_uk.asp). These codes identify the nationality of athletes and teams during Olympic events *()*
* **currency_alphabetic_code** - [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) three letter code *(string)*
* **currency_country_name** - [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) country string name *(string)*
* **currency_minor_unit** - [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) minor unit *(int)*
* **currency_name** - [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency string name *(string)*
* **currency_numeric_code** - [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) numeric code *(int)*
* **is_independent** - Country status, based on the CIA World Factbook. This column is just a superficial note, provided for convenience. I don't care to
argue about it. For full details, please consult your favorite official source. *(string)*
        
### Notes from the Source
Data comes from multiple sources as follows.

ISO 3166 offical English and French short names are from
[iso.org](http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm)
Note: ISO is no longer providing these code lists for free.

ISO 4217 currency codes are from
[currency-iso.org](http://www.currency-iso.org/en/home/tables/table-a1.html)

Many other country codes are from
[statoids.com](http://www.statoids.com/wab.html)

Special thanks to Gwillim Law for his excellent
[statoids.com](http://www.statoids.com) site (some of the field descriptions
are excerpted from his site), which is more up-to-date than most similar
resources and is much easier to scrape than multiple Wikipedia pages.


## Preparation

This package includes a Python script to fetch current country information
and output a JSON document of combined country code information.
Per-country JSON documents may be keyed by any of the fields below.

CSV output is provided via the `in2csv` and `csvcut` utilities from [csvkit](http://github.com/onyxfish/csvkit)

Run **scripts/get_countries_of_earth.py --help** for usage information

### data/country-codes.csv

Install requirements:

    pip install -r scripts/requirements.pip


Run the python script to generate json file:

    python scripts/get_countries_of_earth.py -l


Convert json file to csv (and reorder columns):

    in2csv data/country-codes.json > data/country-codes.csv
    python scripts/reorder_columns.py


## License

This material is licensed by its maintainers under the Public Domain Dedication
and License.

Nevertheless, it should be noted that this material is ultimately sourced from
ISO and other standards bodies and their rights and licensing policies are somewhat
unclear. As this is a short, simple database of facts there is a strong argument
that no rights can subsist in this collection. However, ISO state on [their
site](http://www.iso.org/iso/home/standards/country_codes.htm):

> ISO makes the list of alpha-2 country codes available for internal use and
> non-commercial purposes free of charge.

This carries the implication (though not spelled out) that other uses are not
permitted and that, therefore, there may be rights preventing further general
use and reuse.

If you intended to use these data in a public or commercial product, please
check the original sources for any specific restrictions.

