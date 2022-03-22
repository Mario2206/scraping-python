from scrapper import Scrapper
import requests_cache
import time
start_time = time.time()

requests_cache.install_cache('demo_cache')

scrapper = Scrapper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions')
scrapper.get_header_data()
scrapper.get_content_data()
scrapper.get_legend_table()
scrapper.get_champions()
scrapper.get_list_of_scrapped_champions()
scrapper.get_references()
scrapper.get_cost_reduction()
scrapper.display_data()


print("--- %s seconds ---" % (time.time() - start_time))
