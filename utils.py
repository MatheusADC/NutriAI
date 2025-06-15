import re

def formatar_recomendacao(texto):
    texto = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)

    texto = re.sub(r'\* +', '', texto)

    texto = re.sub(
        r'(?<!• )\b(\w+-feira)\b:?',  
        r'\n• \1:',                   
        texto,
        flags=re.IGNORECASE
    )

    texto = re.sub(r'\n{3,}', '\n\n', texto).strip()

    return texto
