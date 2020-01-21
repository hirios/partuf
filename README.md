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

![Image description](https://user-images.githubusercontent.com/35049559/72764850-745d7000-3bc8-11ea-802a-f2cbb1f14887.png)
![Image description](https://user-images.githubusercontent.com/35049559/72764851-74f60680-3bc8-11ea-8261-49d0d0bec2eb.png)
![Image description](https://user-images.githubusercontent.com/35049559/72764852-74f60680-3bc8-11ea-96e2-8ba7e6059a53.png)
![Image description](https://user-images.githubusercontent.com/35049559/72764853-758e9d00-3bc8-11ea-8981-7ffb56e43260.png)


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



