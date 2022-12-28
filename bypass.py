import requests
import lxml.html


def Parser(text):
	parser = lxml.html.fromstring(text)
	url = parser.xpath('//a[@id="link"]')[0].get('href')
	return url


def GetMagnetic(url):
    s = requests.Session()
    url_inicial = url

    primeiraPagina = s.get(url_inicial)
    parser_01 = Parser(primeiraPagina.text)

    segundaPagina = s.get(parser_01)
    parser_02 = Parser(segundaPagina.text)

    terceiraPagina = s.get(parser_02)
    parser_03 = Parser(terceiraPagina.text)

    quartaPagina = s.get(parser_03)
    parser_04 = Parser(quartaPagina.text) # + /?utm_source=facebook&utm_medium=social&utm_campaign=fanpages

    paginaDoLink = s.get(parser_04)
    paginaDoLinkParser = lxml.html.fromstring(paginaDoLink.text)
    linkMagnetico = paginaDoLinkParser.xpath('//div[@id="baixar"]/p/a')[0].get('href')
    return linkMagnetico




