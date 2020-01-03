import huepy
from huepy import *
from bs4 import BeautifulSoup
import PySimpleGUI as sg
import subprocess
import cfscrape
import fire
import os


requests = cfscrape.create_scraper()


escolha = 0
def option(numero=0):
    global escolha
    escolha = int(numero)
    
if __name__ == '__main__':
    fire.Fire(option)


def layout_inicial():
    global escolha
    layout = [[sg.Text(16*" " + 'PARTUF - SUA FERRAMENTA DE STREAMING E DOWNLOAD DE TORRENT', size=(80,2))],
              [sg.Text('                       '), sg.Radio('Streaming!', "1", default=True),
               sg.Radio('Download!', "1"),
               sg.Radio('Link Magnético!', "1")],
              [sg.Input(size=(80,1))],
              [sg.Cancel(), sg.OK()]]
              
    window = sg.Window('Partuf', layout)
    event, values = window.read()
    window.close()

    if values[0] is True:
        escolha = 0
    elif values[1] is True:
        escolha = 1
    elif values[2] is True:
        escolha = 2
        
    return values[3]


def url_scrape():
    busca = layout_inicial()
    busca = busca.split()
    termos_da_busca = []

    for item in range(len(busca)-1):
        termos_da_busca.append(busca[item] + '+')

    concatenando = "".join(termos_da_busca)
    # busca[len(busca)-1] Retorna a último palavra capturada pelo input
    url = concatenando + busca[len(busca)-1]
    url_final = 'https://www.baixarfilmetorrent.net/?s='+url
    return url_final


def mostrar_lista_filmes():
    global titulos, links
    
    print()
    print("Carregando lista de filmes...")
    print()

    req = requests.get(url_scrape())
    soup = BeautifulSoup(req.text, 'html.parser')
    listagem_da_pesquisa = soup.find_all("div", {'class':  'item'})

    titulos = []
    links = []

    for filme in listagem_da_pesquisa:
        titulos.append(str(filme).split('"')[5])
        links.append(str(filme).split('"')[3])

    for titulo in range(0, len(titulos)):
        print([titulo + 1], titulos[titulo])


def layout_selecionar_filmes():
    layout = [[sg.Listbox(titulos, size=(60, 18), font='Arial 18')],
          [sg.OK()]]

    window = sg.Window('Títulos', layout)
    event, values = window.read()
    window.close()
