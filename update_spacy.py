"""Запустив этот модуль, мы обновим списки слов в каталоге text2words/data.
Этот модуль требует довольно тяжелой зависимости spacy + модели языков.

Но сам пакет text2words останется компактным и нетребовательным.
"""

import subprocess
import sys
from pathlib import Path

import spacy


def install_model(package: str):
    """Устанавливает модель spacy.

    Список возможных моделей: (https://spacy.io/models).

    Пример:
        install_model("en_core_web_sm")
    """
    spacy.cli.download(package)  # type: ignore


def uninstall_model(package: str):
    """Удаляет ранее установленную модель spacy."""
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'uninstall', package, '-y'])


def load_model(pkg: str):
    """Загружает модель spacy. Если она не установлена - скачивает
    и загружает."""
    try:
        return spacy.load(pkg)
    except OSError:
        spacy.cli.download(pkg)
        return spacy.load(pkg)


def update():
    """Обновляет списки слов в каталоге `text2words/data`. """
    for model in ["en_core_web_sm",
                  "fr_core_news_sm",
                  'es_core_news_sm',
                  'de_core_news_sm']:
        target_file = Path(__file__).parent / "text2words" / "data" / \
                      (model + ".txt")
        words = '\n'.join(sorted(load_model(model).Defaults.stop_words))
        target_file.write_text(words)


if __name__ == "__main__":
    update()
