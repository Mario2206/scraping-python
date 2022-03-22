import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

class Scrapper:
    def __init__(self, url) -> None:
        self.url = url 
        page = requests.get(self.url).text
        self.parser = BeautifulSoup(page, 'html.parser')
        self.data = {}
    
    def get_header_data(self):
        title = self.parser.find('h1', class_='page-header__title').get_text().strip()
        wrapper = self.parser.find("div", class_='mw-parser-output')
        description = wrapper.p.get_text().strip()

        self.data['title'] = title
        self.data['description'] = description

    def get_content_data(self):
        list_element = self.parser.find("div", id='toc').ul 
        items = list_element.find_all('li')
      
        data = list(map(lambda item: item.a.get_text(), items))
        
        self.data['content'] = data
    
    def get_legend_table(self):
        table = self.parser.find("table", class_= 'champions-list-legend')
        lines = table.find_all('tr')
        fields = list(map(lambda item: item.get_text().strip(),lines[0].find_all("th"))) 
        data = []
        for line in lines[1:]:
            items = line.find_all("td")
           
            data.append({ fields[0] : items[0].get_text().strip(), fields[1] : items[1].get_text().strip() })
        
        self.data['legend'] = data
    

    def get_champions(self):
        table = self.parser.find("table", class_="article-table")
        lines = table.find_all("tr")
        fields = list(map(lambda field: field.get_text().strip(), lines[0].find_all("th")))
        data = []
        for line in lines[1:]:
            cells = line.find_all("td")
            formated_cells = {}
            for index, cell in enumerate(cells):
                formated_cells[fields[index]] = cell.get_text().strip()
            
            data.append(formated_cells)
        
        self.data['champions'] = data

    def get_list_of_scrapped_champions(self):
        list_element = self.parser.find("div", class_='columntemplate').ul
        items = list_element.find_all("li")
        data = []
        for item in items:
            img = item.img['data-src']
            text = item.get_text()
            data.append({'img': img, 'text': text})
        
        self.data["scrapped_champions"] = data
    
    def get_cost_reduction(self):
        title = self.parser.h3
        title_text = title.get_text().strip()
        paragraph = title.find_next_sibling('dl')
        list_element = title.find_next_sibling('ul')
        print(  paragraph.get_text().strip())

        self.data[title_text] = [
            paragraph.get_text().strip(),
        ]

        self.data[title_text] += list(map(lambda item : item.get_text(),list_element.find_all("li")))

    def get_references(self):
        table = self.parser.find("div", class_='navbox-wrapper')
        fields = list(map(lambda item: item.get_text(), table.find_all('th')))
        cells = table.find_all("td")
        references = {}
        for index, cell in enumerate(cells) : 
            links = cell.find_all("a")
            links = list(map(lambda link: {'title' : link.get_text(), 'link': link['href']},links))
            references[fields[index]] = links

        self.data['references'] = references
    
    def display_data(self):
        for key, items in self.data.items():
            if isinstance(items, list): 
                print(key)
                df = DataFrame(items)
                print(df)
            
            elif key == 'references' : 
                for ref_key, references in items.items():
                    print(ref_key)
                    df = DataFrame(references)
                    print(df)
                    print('\n')

            else :
                print(items)
            
            print('\n\n')

    
