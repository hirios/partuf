# Partuf
Busque e faça streaming de filmes enquanto baixe, via torent (link magnêtico). 

# Versão para windows:

https://github.com/hirios/partuf/releases

1) Abra o instalador.bat (NÂO precisa ser como adm)

2) Rode o partuf.exe

obs: Obs: Quando o vlc for aberto, muito provavelmente surgirá um erro dizendo que o a url do localhost não está transmitindo nada. Ignore o erro e clique no botão play e aguarde carregar (isso demora uns 2 minutos em média :/), possa ser que tenha que apertar novamente no botão play, então, caso não inicie de primeira, repita o processo.
Teria como evitar o erro, mas para isso precisa que o vlc esteja instalado na máquina, no casso dessa versão, ela utiliza explicitamente o vlc portable que está na pasta.

# Linux Users:

Instale primeiramente o vlc na sua máquina 

``` pip install bs4 requests```

``` npm install -g peerflix```

``` python partuf.py```

# Caso nao use vlc:
Altere a última linha do código para:

start = subprocess.check_call(["peerflix", mag_final])

Será criado um url de streaming, no caso, seu localhost:8888, que poderá ser usada com qualquer outro programa de streaming.
