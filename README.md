# bookcli-webinar

Code from Anders webinar (26 Nov 2020). A quick tutorial to build a CLI application that read a pdf book out loud.

You can use this code as the MVP and consider building/adding feature to your application as suggested [below](#suggestion-for-improvement)
## Installation:
```
pip install -r requirements.txt
```

**Note:** This project use `pdftotext`, please check `pdftotext` [documentation](https://github.com/jalan/pdftotext) for its OS specific dependencies

## Usage:

Check `--help` for detail usage

```
python main.py --help
```

## Reference

- Convert PDF to text: [pdftotext](https://github.com/jalan/pdftotext)
- Python toolkit for working with databases: [SQLAlchemy](https://www.sqlalchemy.org/)
- Python CLI framework: [Click](https://click.palletsprojects.com/en/7.x/)
- Python Text-to-Speech library: [Pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- Python library for printing nice looking table to console: [python-tabulate](https://github.com/astanin/python-tabulate)
- Database migration tool: [alembic](https://alembic.sqlalchemy.org/en/latest/)


## Suggestion for improvement

- Functionality for storing the last read page
- Functionality to continue from the last read page
- Functionality to start reading from a specific page
- Functionality to change voices
- Functionality to automatically detect book's language and choose the suitable voices according to the detected language
- And more...