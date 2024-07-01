# 🎵 SpotiTube 🎵
> Aplicação que consulta as músicas de uma playlist do Spotify no YouTube e faz o download.
<br>
<p>
<img alt="Python ver." src="https://img.shields.io/badge/python%20-%203.14-%20green?logo=python">
<img alt="Pytube ver." src="https://img.shields.io/badge/pytube-15.0.0-blue">
<img alt="PySimpleGUI ver." src="https://img.shields.io/badge/PySimpleGUI-4.60.5-blue">
</p>
SpotiTube é uma aplicação simples que recebe as informações de caminho para salvamento e o link da playlist do Spotify. A aplicação consulta as músicas da playlist no Youtube e é feito o download do primeiro resultado apresentado com formato .mp3.
<br>
<img src="https://i.imgur.com/k2jdFWG.png" alt="SpotiTube Logo" style="width:400px; text-align=center"/>

## Instalação / Execução
Com o python instalado, apenas execute o arquivo spotitube.py:
```sh
python3 spotitube.py
```

Caso queira criar um executável, utilize o <a href="https://pypi.org/project/pyinstaller/">PyInstaller</a> e o comando:
```sh
pyinstaller "spotitube.py" -F -i "spotitube.ico" -n SpotiTube --windowed
```

## Exemplo de utilização

1. Selecione o diretório que será salvo os arquivos, digitando ou clicando no botão Browse.<br><br>
<img alt = "Select Save Dir" src="https://i.imgur.com/H1jka3X.png"><br><br>
2. Copie o link da playlist de sua escolha no Spotify. Exemplo no aplicativo Desktop:<br><br>
<img alt = "Spotify link" src="https://i.imgur.com/1uSCQXt.png" style="width:400px;"><br><br>
3. Cole o link na aplicação e clique no botão Download.<br><br>
<img alt = "Paste link" src="https://i.imgur.com/gBCy3rm.png"><br><br>
4. A aplicação começará a fazer o download das músicas. O título da música atual será mostrada, assim como a barra de progresso.<br><br>
<img alt = "Tracks download" src="https://i.imgur.com/pyY8vU9.png"><br><br>
5. Ao concluir o download, será mostrado um aviso de conclusão.<br><br>
<img alt = "Popup download finished" src="https://i.imgur.com/Wpmjin6.png"><br><br>
<br>

## Dependências


-> <a href="https://pypi.org/project/pytube/">Pytube
</a>
<br>

```sh
pip install pytube
```


-> <a href="https://pypi.org/project/PySimpleGUI/">PySimpleGUI
</a>

```sh
pip install PySimpleGUI
```


-> <a href="https://pypi.org/project/deepmerge/">Deepmerge
</a>

```sh
pip install deepmerge
```

<p align="center">
  <img alt = "GitHub language count" src="https://img.shields.io/github/languages/count/srkrash/spotitube">

  <a href="https://github.com/srkrash/spotitube">
    <img src="https://img.shields.io/github/last-commit/srkrash/spotitube">
  </a>
</p>

