from bs4 import BeautifulSoup
import subprocess
import cfscrape
import fire
import os
requests = cfscrape.create_scraper()

options = 1
tabelas = None
resolut = []
magnetico = []


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
    """
    Mostra a lista de filmes e armazena a url de cada um deles em [links]
    """

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
    print()
    print("\nCarregando lista de filmes...\n")

    return links


def get_tables():
    """
    Retorna a tabela com links-magneticos do filme selecionado
    """
    movie_list = show_movie_list()
    select_number = int(input('Selecione um número: '))
    url_of_movie = movie_list[select_number - 1]

    html = requests.get(url_of_movie)
    soup = BeautifulSoup(html.text, 'html.parser')
    tabelas = soup.find_all("table")
    return tabelas


def magnetics_and_resolution_of_movies():
    """
    PARA FILMES: Adiciona resolucoes e links magneticos às suas respectivas listas
    """
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
        start = subprocess.check_call(["peerflix", mag_final, "--path", os.getcwd(), "--vlc"])
    # Somente faz o download
    elif options == 2:
        print("\nDownload iniciado...\n")
        start = subprocess.check_call(["peerflix", mag_final, "--path", os.getcwd()])
    # Retorna o link magnético
    elif options == 3:
        print("\nLink magnético:\n")
        print(mag_final)
        print()


while True:
    if __name__ == '__main__':
        tabelas = get_tables()
        magnetics_and_resolution_of_movies()
        magnetics_and_resolution_of_series()
        fire.Fire(options)
