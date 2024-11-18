from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    # Lança o Chromium (sem precisar do ChromeDriver)
    browser = p.chromium.launch(headless=False)  # headless=True se não quiser abrir o navegador
    page = browser.new_page()

    # Acessa a página do Google
    page.goto("https://www.google.com/search?q=python")

    # Captura os resultados da pesquisa
    resultados = page.query_selector_all('h3')
    dados = [resultado.inner_text() for resultado in resultados]

    # Cria um DataFrame com os dados coletados
    df = pd.DataFrame(dados, columns=["Resultado"])

    # Salva os dados em um arquivo Excel
    df.to_excel('resultados_google_playwright.xlsx', index=False)

    print("Dados salvos com sucesso!")
    
    # Fecha o navegador
    browser.close()
