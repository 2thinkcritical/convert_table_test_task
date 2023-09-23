import argparse

def main(args):
    source_csv = args.source
    template_csv = args.template
    target_csv = args.target
    api_key = args.key

    # Ваш код обработки CSV файлов и использования API ключа здесь
    print(f"Source CSV: {source_csv}")
    print(f"Template CSV: {template_csv}")
    print(f"Target CSV: {target_csv}")
    print(f"API Key: {api_key}")
    
    import pandas as pd
    import openai

    openai.api_key = api_key

    df_source = pd.read_csv(source_csv)
    df_template = pd.read_csv(template_csv)
    
    print("Изначально таблица выглядит так:")
    print(df_source)
    print()
    print("Образец:")
    print(df_template)
    print()
    
    prompt = f"""
        Напиши код на питоне с использованием pandas чтобы изменить названия столбцов и формат содержания столбцов этой таблицы:
        ```{df_source.head(2)}```
        по этому образцу:
        ```{df_template.head(2)}```
        Переменная, в которой лежит датафрейм называется df_source.  
        """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Пиши только код на питоне"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            request_timeout=120,
        )
    except:
        print("Превышено время ожидания ChatGPT API")
        return 1
    
    resp = response['choices'][0]['message']['content']
    
    if resp.startswith("```python\n"):
        resp = resp[10:]
    if resp.endswith("```"):
        resp = resp[:-3]

    print("Выполняю следующий код для преобразования таблицы: \n", resp)
    try:  
        local_vars = locals()      
        exec(resp, local_vars)
        df_source = local_vars['df_source']        
        print("Код успешно выполнен!")
    except Exception as e:
        print(f"Ошибка при выполнении сгенерированного кода: {e}")
        return 1
    
    
    print("Теперь таблица выглядит так:")
    print(df_source)
    print()
    
    print("Записываю таблицу в файл ", target_csv)
    df_source.to_csv(target_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert source CSV based on template and save to target CSV.")
    
    parser.add_argument("--source", type=str, required=True, help="Path to source CSV file.")
    parser.add_argument("--template", type=str, required=True, help="Path to template CSV file.")
    parser.add_argument("--target", type=str, required=True, help="Path to target CSV file where the result will be saved.")
    parser.add_argument("--key", type=str, required=True, help="API key for accessing external services (openai API).")

    args = parser.parse_args()
    main(args)