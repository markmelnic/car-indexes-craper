
from mobile_de import mde_scraper
from autoscout24_ch import ats_scraper


if __name__ == '__main__':
    try:
        #ats_scraper.scrape_models()
        mde_scraper.scrape_models()
    except KeyboardInterrupt:
        exit(0)