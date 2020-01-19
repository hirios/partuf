import huepy
from huepy import *
from bs4 import BeautifulSoup
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


while True:
    busca = input('Nome do filme: ')
    busca = busca.split()
    termos_da_busca = []

    for item in range(len(busca)-1):
        termos_da_busca.append(busca[item] + '+')

    concatenando = "".join(termos_da_busca)
    # busca[len(busca)-1] Retorna a último palavra capturada pelo input
    url = concatenando + busca[len(busca)-1]
    url_final = 'https://www.baixarfilmetorrent.net/?s='+url

    print()
    print("Carregando lista de filmes...")
    print()

    req = requests.get(url_final)
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
    select_number = int(input('Selecione um número: '))
    lin = links[select_number - 1]

    link = requests.get(lin)
    soup = BeautifulSoup(link.text, 'html.parser')
    tabelas = soup.find_all("table")

    resolut = []
    magnetico = []

    # Para filmes
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

    # SE NÃO FOR UM FILME
    if len(magnetico) == 0:
        for tabela in range(0, len(tabelas)):
            single_table = BeautifulSoup(str(tabelas[tabela]), 'html.parser')
            strong = single_table.find("strong")

            # HTML para episódios de séries
            html_num_epi = single_table.find_all("td", {'class': 'td-ep-eps'})
            html_qualidades = single_table.find_all("td", {'class': 'td-ep-res'})
            html_magnetic = single_table.find_all("td", {'class': 'td-ep-dow'})

            for quali in range(0, len(html_qualidades)):
                resolut.append(f"{yellow(html_num_epi[quali].string.replace('Ep.', '-'))} {orange('->>')} {html_qualidades[quali].string} {strong.string}")
                magnetico.append(str(html_magnetic[quali]).split('"')[3])

        magnetico.append("")
        resolut.append("")

    # Verifica se espaços em branco, se tiver ignora os primeiros
        space = 1
        for c in resolut:
            if len(c) != 0:
                print([space], c)
                space += 1
    #        if c == "" and space == 0:
    #            resolut.pop(c)
    #        else:
    #            space = 1
    #            print(c)


        selected_resolution = int(input('Esolha a resolução: '))
        mag_final = magnetico[selected_resolution - 1]
        #print(mag_final)

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
                               
    # SE FOR UM FILME
    else:
        for cont in range(0, len(magnetico)):
            print([cont + 1], resolut[cont])

        print()
        selected_resolution = int(input('Esolha a resolução: '))
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
