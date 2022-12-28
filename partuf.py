import cfscrape
requests = cfscrape.create_scraper()
import lxml.html
from downTorrent import downloadTorrent
from bypass import GetMagnetic
import subprocess
import os


URL = 'https://baixarfilmestorrent.tv/?s='


def user():
        user = os.popen("whoami").read().split("\\")[1].strip()
        return user


peerflix_path = f"C:\\Users\\{user()}\\AppData\\Roaming\\npm\\node_modules\\peerflix\\app.js"


class Connection:
    def __init__(self):
        self.resolutions_list = []
        self.movies_list = []
        self.movie_selected = ''
        self.resolutions_selected = ''


    def search_movie(self):
        movie_name = '+'.join(input('Digite o nome do filme: ').split(' '))
        print()

        movies_page = requests.get(URL + movie_name)        
        movies_elements = lxml.html.fromstring(movies_page.text).cssselect('[class="item"]')

        for movie in movies_elements:
            try:
                self.movies_list.append({
                    'Titulo': movie.cssselect('a')[0].get('title'),
                    'Link': movie.cssselect('a')[0].get('href')
                    })
            except:
                pass

    def select_movie(self):
        cont = 1

        for movie in self.movies_list:
            print([cont], movie['Titulo'])
            cont += 1

        num_select = int(input('\nSelecione um número: ')) - 1
        self.movie_selected = self.movies_list[num_select]['Link']
    

    def get_resolutions(self):
        movie_select_page = requests.get(self.movie_selected)
        movie_resolutions = lxml.html.fromstring(movie_select_page.text).cssselect('[class="tr-mv-list tr-quality-web-dl"]')

        for resolution in movie_resolutions:
            self.resolutions_list.append({
                'Qualidade': resolution.cssselect('[class="td-mv-qua quality-web-dl"]')[0].text,
                'linkProtegido': resolution.cssselect('[class="td-mv-dow"] a')[0].get('href')
            })


    def select_resolution(self):
        cont = 1

        for x in self.resolutions_list:
            print([cont], x['Qualidade'])
            cont += 1
        
        num_select = int(input('\nSelecione um filme: ')) - 1
        self.resolutions_selected = self.resolutions_list[num_select]['linkProtegido']
        
    
    def play(self):
        magnetico = GetMagnetic(self.resolutions_selected)
        subprocess.Popen(f'peerflix "{magnetico}" --vlc', shell=True)
        

while True:
    site = Connection()
    site.search_movie()
    site.select_movie()
    site.get_resolutions()
    site.select_resolution()
    site.play()
