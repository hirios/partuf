import os
import importlib


def bible(lib):
    try:
        if importlib.import_module(lib):
            return importlib.import_module(lib)
    except:
        try:
            os.system(f'pip install {lib}')
            return importlib.import_module(lib)
        except:
            os.system(f'sudo pip install {lib}')
            return importlib.import_module(lib)
        
bs4 = bible("bs4")
cfscrape = bible("cfscrape")
from bs4 import BeautifulSoup
from shutil import which
from zipfile import ZipFile
import threading   
import subprocess
import socket
import os
import time
requests = cfscrape.create_scraper()


tabelas = None
serie = None
resolut = []
magnetico = []
localhost = socket.gethostbyname(socket.gethostname())


def getLink(MAGNETIC):
    HASH = MAGNETIC.split(':')[-1]
    url = f"https://itorrents.org/torrent/{HASH}.torrent"
    return url


def downloadTorrent(linkTorrent):
    out = requests.get(linkTorrent)
    with open('torrent.torrent', 'wb') as f:
        f.write(out.content)


def url_scrape():
    busca = input('Digite o nome do filme: ')
    busca = busca.split()
    termos_da_busca = []
    # -1 porque o último termo será excluido (pois não tem o sinal [+] na url)
    for item in range(len(busca)-1):
        termos_da_busca.append(busca[item] + '+')
    concatenando = "".join(termos_da_busca)
    # Último termo é aderido a url de busca
    url = concatenando + busca[-1]
    url_final = 'https://www.baixafilme.net/?s='+url
    return url_final


def show_movie_list():
    """ Mostra a lista de filmes e armazena a url de cada um deles em [links] """

    req = requests.get(url_scrape())
    soup = BeautifulSoup(req.text, 'html.parser')
    listagem_da_pesquisa = soup.find_all("div", {'class':  'item'})
    titulos = []
    links = []
    
    print("\nCarregando lista de filmes...\n")
    for filme in listagem_da_pesquisa:
        titulos.append(str(filme).split('"')[5])
        links.append(str(filme).split('"')[3])
    for titulo in range(0, len(titulos)):
        print([titulo + 1], titulos[titulo])
    print()
    return [links, titulos]


def layout_selecionar_filmes():
    listas = show_movie_list()
    titulos = listas[1]
    links = listas[0]
    posit = int(input('Digite um número: ')) - 1
    return links[posit]
    

def get_tables():
    """ Retorna a tabela com links-magneticos do filme selecionado """
    
    #movie_list = show_movie_list()[0]
    #select_number = int(input('Selecione um número: '))
    url_of_movie = layout_selecionar_filmes() #movie_list[select_number - 1]
    html = requests.get(url_of_movie)
    soup = BeautifulSoup(html.text, 'html.parser')
    tabelas = soup.find_all("table")
    return tabelas


def magnetics_and_resolution_of_movies():
    """ PARA FILMES: Adiciona resolucoes e links magneticos às suas respectivas listas """
    
    for tabela in range(0, len(tabelas)):
        single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')
        strong = single_table.find("strong")

        try:
            html_qualidades = single_table.find_all("td", {'class':  'td-mv-res'})
            html_magnetic = single_table.find_all("td", {'class':  'td-mv-dow'})
            html_tamanho = single_table.find_all("td", {'class': 'td-mv-tam'})   
            
            for quali in range(0, len(html_qualidades)):
                resolut.append(f"{html_qualidades[quali].string} {strong.string}    |||     {html_tamanho[quali].string}")

            for link_mag in range(len(html_magnetic)):
                magnetico.append(str(html_magnetic[link_mag]).split('"')[3])
        except:
            pass


def magnetics_and_resolution_of_series():
    """ PARA SERIES: Adiciona resolucoes e links magneticos as suas respectivas listas """

    global tabelas,  resolut, magnetico    
    if len(magnetico) == 0:
        for tabela in range(0, len(tabelas)):
            single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')
            strong = single_table.find("strong")

            # HTML para episódios da série
            html_num_epi = single_table.find_all("td", {'class': 'td-ep-eps'})
            html_qualidades = single_table.find_all("td", {'class': 'td-ep-res'})
            html_magnetic = single_table.find_all("td", {'class': 'td-ep-dow'})

            try:
                for quali in range(0, len(html_qualidades)):
                    resolut.append(f"{html_num_epi[quali].string.replace('Ep.', '-')} {'->>'} {html_qualidades[quali].string} {strong.string}")
                for link_mag in range(len(html_magnetic)):
                    magnetico.append(str(html_magnetic[link_mag]).split('"')[3])
            except:
                pass


def magneticos_da_serie_completa():
    global serie, tabelas,  resolut, magnetico

    if len(magnetico) == 0:
        for tabela in range(0, len(tabelas)):
            single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')

            # HTML para episódios da série
            html_num_epi = single_table.find_all("td", {'class': 'td-tp-aud'})
            html_qualidades = single_table.find_all("td", {'class': 'td-tp-res'})
            html_magnetic = single_table.find_all("td", {'class': 'td-tp-dow'})
            
            try:
                for quali in range(0, len(html_qualidades)):
                    resolut.append(f"{html_num_epi[quali].string} {html_qualidades[quali].string}")

                for link_mag in range(len(html_magnetic)):
                    magnetico.append(str(html_magnetic[link_mag]).split('"')[3])
            except:
                pass
            
        if len(magnetico) == 0:
            serie = False
        else:
            serie = True


def get_episodes(magnetico):
    lista = os.popen(f'peerflix {magnetico} -l').readlines()
    lista = [x for x in lista if x.find('.jpg') == -1 and x.find('.srt') == -1 and x.find('.txt') == -1 and x.find('.png') == -1 and x.find('.jpeg') == -1 and x.find('.gif') == -1 and x.find('.bmp') == -1 and x.find('.pdf') == -1] 
    epi_titulos = []
    index = []

    for x in lista:
        try:

            epi_titulos.append(x.split("\x1b[35m")[1].split("\x1b[39m")[0])
        except:
            print('Não é um título de episódio')

    for x in lista:
        try:
            index.append(x.split("\x1b[1m")[1].split("\x1b[22m")[0].strip())
        except:
            print('Não é um index de episódio')

    final = []
    cont = 0
    for c in epi_titulos:
        final.append([c, [index[cont]]])
        cont += 1
    final = sorted(final)
    return final


def select_resolution():
    global window        

    c = 1
    for x in resolut:
        print([c], x)
        c += 1

    posit = int(input('\nSelecione um número: ')) - 1

    mag_final = magnetico[posit]
    return mag_final


def peneira():
    global resolut, magnetico, window
    
    if serie:
        url_magnetico = select_resolution()
        episodes = get_episodes(url_magnetico)
        resolut = [x[0] for x in episodes]
        magnetico = [x[1][0] for x in episodes]
        return [url_magnetico, select_resolution()]
    else:
        url_magnetico = select_resolution()
        return [url_magnetico, '']
        

def options():
    global serie    
    
    mag_final, index = peneira()
    downloadTorrent(getLink(mag_final))
    
    print("\nAguarde o carregamento... \nEnjoy!!\n")

    if index == '':
        start_host = subprocess.Popen(['peerflix', 'torrent.torrent', "--path", os.path.join("%USERPROFILE%", "Desktop", "Filmes")], shell=True)
    else:
        start_host = subprocess.Popen(['peerflix', 'torrent.torrent', "-i", index, "--path", os.path.join("%USERPROFILE%", "Desktop", "Filmes")], shell=True)


def main():
    global tabelas, resolut, magnetico, use

    resolut = []
    magnetico = []

    tabelas = get_tables()
    magnetics_and_resolution_of_movies()
    magneticos_da_serie_completa()
    magnetics_and_resolution_of_series()
    options()


while True:
    main()
