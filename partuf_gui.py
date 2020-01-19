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

    posit = 666
    for p in range(0, len(titulos)):
        if titulos[p] == values[0][0]:
            posit = p
    return posit + 1


def table():
    global tabelas
    
    print()
    select_number = layout_selecionar_filmes()
    lin = links[select_number - 1]
    
    link = requests.get(lin)
    soup = BeautifulSoup(link.text, 'html.parser')
    tabelas = soup.find_all("table")
    return None

#######################
resolut = []
magnetico = []
#######################

# **PARA FILMES** Adiciona resolucoes e links magneticos as suas respectivas listas
def lista_magneticos_do_filme_selecionado():
    for tabela in range(0, len(tabelas)):
        single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')
        strong = single_table.find("strong")

        try:
            html_qualidades = single_table.find_all("td", {'class':  'td-mv-res'})
            html_magnetic = single_table.find_all("td", {'class':  'td-mv-dow'})

            for quali in range(0, len(html_qualidades)):
                resolut.append(f"{html_qualidades[quali].string} {strong.string}")

            for link_mag in range(len(html_magnetic)):
                magnetico.append(str(html_magnetic[link_mag]).split('"')[3])
        except:
            pass
        
# **PARA SERIES** Adiciona resolucoes e links magneticos as suas respectivas listas 
def lista_magneticos_da_serie_selecionada():
    if len(magnetico) == 0:
        for tabela in range(0, len(tabelas)):
            single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')
            strong = single_table.find("strong")

            # HTML para episódios da série
            html_num_epi = single_table.find_all("td", {'class': 'td-ep-eps'})
            html_qualidades = single_table.find_all("td", {'class': 'td-ep-res'})
            html_magnetic = single_table.find_all("td", {'class': 'td-ep-dow'})

            for quali in range(0, len(html_qualidades)):
                resolut.append(f"{yellow(html_num_epi[quali].string.replace('Ep.', '-'))} {orange('->>')} {html_qualidades[quali].string} {strong.string}")
                magnetico.append(str(html_magnetic[quali]).split('"')[3])
                
        magnetico.append("")
        resolut.append("")


def layout_selecionar_resolucao():
    if len(magnetico) != 0:
        for cont in range(0, len(magnetico)):
            print([cont + 1], resolut[cont])

    layout = [[sg.Listbox(resolut, size=(60, 18), font='Arial 18')],
              [sg.OK()]]
    window = sg.Window('Resolut', layout)
    event, values = window.read()
    window.close()

    posit = 666
    for p in range(0, len(resolut)):
        if resolut[p] == values[0][0]:
            posit = p
    return posit + 1


def opcoes_de_uso():
    global escolha
    selected_resolution = layout_selecionar_resolucao()
    mag_final = magnetico[selected_resolution - 1]

    if escolha == 0:
        print()
        print("Aguarde o carregamento... \nEnjoy!!")
        start = subprocess.check_call(["peerflix", mag_final, "--path", os.getcwd(), "--vlc"])

    elif escolha == 1:
        print()
        print("Download iniciado... ")
        start = subprocess.check_call(["peerflix", mag_final, "--path", os.getcwd()])

    elif escolha == 2:
        print()
        print("Link magnético:")
        print(mag_final)
        print()                               


while True:
    mostrar_lista_filmes() # Essa função chama outra função chamada "url_scrape(), a "url_scrape" chama a "layout_inicial()".
    table() # Table chama "layout_selecionar_filmes()"
    lista_magneticos_do_filme_selecionado()
    lista_magneticos_da_serie_selecionada()
    opcoes_de_uso()


