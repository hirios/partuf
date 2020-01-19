# Partuf
Busque e assista streaming de filmes enquanto faz download via torent (link magnêtico). 

# Modo de uso:

Instale primeiramente o vlc na sua máquina, depois dê os seguintes comandos no terminal (se você tiver o pip, node e npm instalados):

```
pip install bs4 cfscrape PySimpleGUI huepy fire
```

```
npm install -g peerflix
```

Se você usa **línux**, tente usar esse comando em linha única:

```sudo pip install bs4 requests huepy fire cfscrape PySimpleGUI && sudo apt install nodejs && sudo apt install npm && sudo npm install -g peerflix && sudo apt install vlc```


**Versão com GUI**:

```
python partuf_gui.py
```

**Versão console**:

1) Para assistir ao streaming do filme/série:
```
python partuf.py
```

2) Para somente baixar o filme/série: 
```
python partuf.py 1
```

3) Para capturar o link magnético do filme/série: 
```
python partuf.py 2
```



