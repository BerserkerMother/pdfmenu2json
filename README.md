
5 seconds# MenuAutomation

Afterhours pdf menu converter.

## Before running:

Set OPENAI_API_KEY enviroment variable to the open ai key and set PDF_PORT to the desired hosting port(defaults to 1234).

## To run:

```bash
python src/app.py
```

## Querying:

### Input

the input is a json object consiting of a path and demo field.

path(str): path to the pdf file

demo(bool): a boolean flag to indicate whether it's a demo use or not.

### Endpoint

[GET] localhost:PDF_PORT/convert





