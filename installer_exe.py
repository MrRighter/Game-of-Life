import PyInstaller.__main__


PyInstaller.__main__.run([
    'ИМЯ/ПУТЬ.py',  # имя/путь желаемого файла
    '--onefile',  # сделать приложение одним файлом
    '--windowed',  # без консольного окна
    # '--icon=имя/путь.ico',  # имя/путь файла иконки
    # '--name=ЛЮБОЕ ИМЯ'  # любое название для приложения
])
