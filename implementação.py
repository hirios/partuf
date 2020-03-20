from bs4 import BeautifulSoup
from shutil import which
from zipfile import ZipFile
import subprocess
import cfscrape
import socket
import fire
import os
import time
requests = cfscrape.create_scraper()


use = 666
options = 1
tabelas = None
resolut = []
magnetico = []
localhost = socket.gethostbyname(socket.gethostname())


def pacotes():
    print("[+] Fazendo download de dependêndencias")
    try:
        zip_html = requests.get("https://www71.zippyshare.com/v/UQmnOz27/file.html").text.replace('(','"'). replace(')', '"')
        zip_html = zip_html.split('"')
        index = zip_html.index("/d/UQmnOz27/")
        url_zip = "https://www71.zippyshare.com/d/UQmnOz27/" + str(eval(zip_html[index + 2])) + "/dependencias.zip"
        
        arquivo = requests.get(url_zip)                         
        with open("requisitos.zip", "wb") as r:
            r.write(arquivo.content)
        
        with ZipFile("requisitos.zip", "r") as extract:
                extract.extractall()
        os.remove("requisitos.zip")
        os.system("cls")
    except:
        print("!!!!! Servidor de dependências não inoperante !!!!!")


def process_status():
    """ Verifica se a instalação do Node foi encerrada """
    print("\n[+] Uma nova janela de instalação foi aberta\n[+] Prossiga você mesmo a instalação do Node") 
    msiexec = 1
    while msiexec != 0:
        time.sleep(3)
        processos = os.popen(f'tasklist /FI "STATUS eq running" | more').read()
        lista_processos = processos.split()
        msiexec = len([x for x in lista_processos if x.find("msiexec") != -1])
                

def dependencias():
    """ Verifica se alguma instalação está faltando e as instala se for o caso """
    global use
    if not which("npm"):
        if os.path.isfile(os.path.join("dependencias", "node.msi")):
            print("[+] Instalando Node...")
            os.popen(os.path.join("dependencias", "node.msi"))
            process_status()
            use = 1
        else:
            print("[+] Iniciando download do Node...")
            pacotes()
            print("[+] Instalando node.js")
            os.popen(os.path.join("dependencias", "node.msi"))
            process_status()
            use = 1
        os.system("cls")
        time.sleep(1)
        
    if not which("peerflix"):
        try:    
            print("[+] Iniciando instalação do Peerflix...")
            os.system(os.path.join("dependencias", "refreshenv.cmd") + " & npm install -g peerflix")
            os.system("cls")
        except:
            print("Erro ao instalar peerflix!")
        use = 1
        
    if not os.path.isdir(os.path.join("dependencias", "vlc")):
        pacotes()
        use = 1
        
    if not os.path.isfile(os.path.join("dependencias", "refreshenv.cmd")):
        pacotes()
        use = 1


def url_scrape():
    busca = input('Nome do filme: ')
    busca = busca.split()
    termos_da_busca = []
    # -1 porque o último termo será excluido (pois não tem o sinal [+] na url)
    for item in range(len(busca)-1):
        termos_da_busca.append(busca[item] + '+')
    concatenando = "".join(termos_da_busca)
    # Último termo é aderido a url de busca
    url = concatenando + busca[-1]
    url_final = 'https://www.baixarfilmetorrent.net/?s='+url
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
    return links


def get_tables():
    """ Retorna a tabela com links-magneticos do filme selecionado """
    
    movie_list = show_movie_list()
    select_number = int(input('Selecione um número: '))
    url_of_movie = movie_list[select_number - 1]

    html = requests.get(url_of_movie)
    soup = BeautifulSoup(html.text, 'html.parser')
    tabelas = soup.find_all("table")
    return tabelas


def magnetics_and_resolution_of_movies():
    """ PARA FILMES: Adiciona resolucoes e links magneticos às suas respectivas listas """
    
    global tabelas, resolut, magnetico
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


def magnetics_and_resolution_of_series():
    """
    PARA SERIES: Adiciona resolucoes e links magneticos as suas respectivas listas
    """
    global tabelas, resolut, magnetico
    if len(magnetico) == 0:
        for tabela in range(0, len(tabelas)):
            single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')
            strong = single_table.find("strong")

            # HTML para episódios da série
            html_num_epi = single_table.find_all("td", {'class': 'td-ep-eps'})
            html_qualidades = single_table.find_all("td", {'class': 'td-ep-res'})
            html_magnetic = single_table.find_all("td", {'class': 'td-ep-dow'})

            for quali in range(0, len(html_qualidades)):
                resolut.append(f"{html_num_epi[quali].string.replace('Ep.', '-')} {'->>'} {html_qualidades[quali].string} {strong.string}")
                magnetico.append(str(html_magnetic[quali]).split('"')[3])

        magnetico.append("")
        resolut.append("")


def select_resolution():
    c = 1
    for x in resolut:
        print([c], x)
        c += 1

    selected_resolution = int(input('\nEsolha a resolução: '))
    mag_final = magnetico[selected_resolution - 1]
    return mag_final


def options(numero=1):
    global options
    options = int(numero)

    mag_final = select_resolution()
    # Faz streming enquanto realiza o download
    if options == 1:
        print("\nAguarde o carregamento... \nEnjoy!!\n")
        if use == 666:
            start_host = subprocess.Popen(["peerflix", mag_final, "--path", os.getcwd()], shell=True)
            time.sleep(3)
            start_vlc = subprocess.Popen([os.path.join("dependencias", "vlc", "App", "vlc", "vlc.exe"), f"http://{localhost}:8888"], shell=True) 
        else:
            start_host = subprocess.Popen([os.path.join("dependencias", "refreshenv.cmd") + " & peerflix", mag_final, "--path", os.getcwd()], shell=True)
            time.sleep(3)
            start_vlc = subprocess.Popen([os.path.join("dependencias", "refreshenv.cmd") + " & " + os.path.join("dependencias", "vlc", "App", "vlc", "vlc.exe"), f"http://{localhost}:8888"], shell=True)

        
    # Somente faz o download
    elif options == 2:
        print("\nDownload iniciado...\n")
        if use == 666:
            start_host = subprocess.Popen(["peerflix", mag_final, "--path", os.getcwd()])
        else:
            start_host = subprocess.Popen([os.path.join("dependencias", "refreshenv.cmd") + " & peerflix", mag_final, "--path", os.getcwd()])


    # Retorna o link magnético
    elif options == 3:
        print("\nLink magnético:\n")
        print(mag_final)
        print()


while True:
    if __name__ == '__main__':
        dependencias()
        tabelas = get_tables()
        magnetics_and_resolution_of_movies()
        magnetics_and_resolution_of_series()
        fire.Fire(options)                      
                               
