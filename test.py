
import os
import json
import subprocess

import mobile_de
import autoscout24_ch
import anibis_ch


if __name__ == '__main__':

    try:
        #autoscout24_ch.scrape_makes()
        #autoscout24_ch.scrape_models()
        #mobile_de.scrape_makes()
        #mobile_de.scrape_models()
        anibis_ch.scrape_makes()
        # check "models": []
    except KeyboardInterrupt:
        exit(0)
    except json.decoder.JSONDecodeError:
        os.remove('makes.json')
        subprocess.run('python test.py')
