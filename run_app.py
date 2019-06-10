""" Main app that runs script
"""

import meteo
import meteopost

def run():
    """ Runs script
    """

    data_base = dbase.read_file()
    last_entry_date = get_last_entry(data_base)

    meteopost_data = meteopost.run_meteopost()
    meteo_data = meteo.run_meteo()

    print(meteo_data)
    print(meteopost_data)


if __name__ == "__main__":
    run()
