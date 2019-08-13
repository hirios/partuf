import requests
from bs4 import BeautifulSoup

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
print(url_final)
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
print(links[select_number - 1])
