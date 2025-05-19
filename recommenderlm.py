import openai
import json
import sys

def recomendar_dieta(resultados):
    client = openai.OpenAI(
        base_url="http://localhost/v1",
        api_key="lm-studio"
    )

    messages = [
        {"role": "system", "content": "Você é um nutricionista. Faça uma rotina de dieta de segunda a domingo com os dados referente de amostras de sangue. Considere valores ruins para colesterol acima de 190, para glicose acima de 126, para T3 acima de 1.81, para T4 acima de 12.3, para TSH acima de 5.60 e para triglicerídeos acima de 150. Fale no início da recomendação o que está ruim a partir dessa referência que te forneci."},
        {"role": "user", "content": json.dumps(resultados, indent=4, ensure_ascii=False)}
    ]

    try:
        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        if hasattr(response, "choices"):
            return response.choices[0].message.content
        else:
            return "Nenhuma resposta recebida."

    except Exception as e:
        return f"Erro ao obter recomendação: {e}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            dados = json.loads(sys.argv[1])
            print(recomendar_dieta(dados))
        except json.JSONDecodeError:
            print("Erro: Os dados enviados não estão no formato JSON válido.")
    else:
        print("Erro: Nenhum dado fornecido.")