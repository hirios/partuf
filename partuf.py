Meu Drive
Ontem
qui 12:17

Você compartilhou 1 item
Texto
partuf.py
Pode ver
Qualquer pessoa com o link
qui 12:08

Você editou 1 item
Arquivo compactado
partuf_windows.rar
qui 10:28

Você fez o upload de 1 item
Arquivo compactado
partuf_windows.rar
qui 10:05

Você criou e compartilhou um item em
Pasta do Google Drive
PROGRAMAS E APKS
Pasta do Google Drive
Partuf
Pode ver
Qualquer pessoa com o link
No início desta semana
qua 16:20

Você editou 1 item
Colaboratory
Untitled2.ipynb
qua 10:13

Você fez o upload de 1 item
Texto
partuf.py
ter 16:09

Você editou 1 item
Colaboratory
Untitled2.ipynb
ter 16:06

Você renomeou 1 item
Colaboratory
Untitled2.ipynb
Untitled
ter 16:06

Você fez o upload de 1 item
Colaboratory
Untitled
Semana passada
5 de ago

Vocêmoveu 307 itens para a lixeira
Arquivo desconhecido
hp_roman8.pyc
Arquivo desconhecido
__init__.pyc
Arquivo desconhecido
cp850.pyc
Arquivo desconhecido
iso2022_jp_2004.pyc
Arquivo desconhecido
iso8859_3.pyc
Arquivo desconhecido
cp862.pyc
import requests
from bs4 import BeautifulSoup
import subprocess

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
lin = links[select_number - 1]

link = requests.get(lin)
soup = BeautifulSoup(link.text, 'html.parser')

html_qualidades = soup.find_all("td", {'class':  'td-mv-res'})
html_magnetic = soup.find_all("td", {'class':  'td-mv-dow'})

resolut = []
magnetico = []

for link_mag in range(0, len(html_magnetic)):
    resolut.append(html_qualidades[link_mag].string)
    magnetico.append(str(html_magnetic[link_mag]).split('"')[3])

for cont in range(0, len(magnetico)):
    print([cont + 1], resolut[cont])

print()
selected_resolution = int(input('Esolha a resolução: '))
mag_final = magnetico[selected_resolution]

print()
print("Aguarde o carregamento... \nEnjoy!!")
start = subprocess.check_call(["peerflix", mag_final, "--vlc"])
