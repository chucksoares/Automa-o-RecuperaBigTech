from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
import subprocess
import tempfile
import shutil

# Garantir que o Chromium seja extraído corretamente
chromium_directory = 'C:/Users/Felipe/AppData/Local/ms-playwright/chromium-1140/chrome-win/'

# Cria um diretório temporário
temp_dir = tempfile.mkdtemp()

# Copia o diretório inteiro
shutil.copytree(chromium_directory, os.path.join(temp_dir, 'chromium'))

# Garante que o Playwright tem os navegadores necessários
subprocess.run(["playwright", "install"])

# Inicia o Playwright e configura o Chromium
with sync_playwright() as p:
    chromium_path = os.path.join(temp_dir, 'chromium', 'chrome.exe')  # Caminho do Chromium copiado
    browser = p.chromium.launch(executable_path=chromium_path, headless=False)  # headless=False se quiser visualizar o navegador
    page = browser.new_page()

    try:
        # Acessa a página de login com aumento do tempo limite para 60 segundos
        page.goto("https://recuperabigtech.com/login", timeout=60000, wait_until="domcontentloaded")
    except Exception as e:
        print(f"Erro ao acessar a página de login: {e}")
        browser.close()
        exit()

    # Preenche o campo de email
    page.fill('input[name="email"]', 'EMAILAQUI')

    # Preenche o campo de senha
    page.fill('input[name="password"]', 'SENHAQUI')

    # Clica no botão de login
    page.click('button[type="submit"]')

    # Espera um pouco para garantir que o login foi realizado
    time.sleep(3)

    # Acessa a página após login ou pode capturar informações da página após o login
    page.goto("https://recuperabigtech.com/home", timeout=60000, wait_until="domcontentloaded")

    # Aumente o tempo de espera para garantir que o botão esteja visível
    page.wait_for_selector('button[aria-label="menu"]:visible', timeout=30000)

    # Simula o hover sobre o botão para ativar o efeito visual
    page.hover('button[aria-label="menu"]')

    # Agora clica no botão
    page.click('button[aria-label="menu"]')

    # Aguarda o menu expandir
    time.sleep(1)  # Ajuste o tempo conforme necessário para garantir que o menu tenha tempo de abrir

    # Rola a página para baixo (ajustar o número de pixels conforme necessário)
    page.mouse.wheel(0, 300)  # Rola para baixo 300 pixels, ajuste conforme necessário

    # Aguarda o botão "Relatórios" aparecer
    page.wait_for_selector('text=Relatórios')  # Certifique-se de que o texto "Relatórios" está correto ou use o seletor adequado

    # Clica em "Relatórios"
    page.click('text=Relatórios')  # Se "Relatórios" for um link ou botão com esse texto

    # Espera um pouco para garantir que a página de relatórios seja carregada
    time.sleep(3)

    # Agora, vamos capturar as informações de usuário, parâmetros e data
    page.wait_for_selector('td.MuiTableCell-root.MuiTableCell-body.MuiTableCell-alignCenter.MuiTableCell-sizeSmall')  # Espera a tabela de dados carregar

    usuarios = page.query_selector_all('td.MuiTableCell-root.MuiTableCell-body.MuiTableCell-alignCenter.MuiTableCell-sizeSmall')
    parametros = page.query_selector_all('td.MuiTableCell-root.MuiTableCell-body.MuiTableCell-alignCenter.MuiTableCell-sizeSmall')  # Ajuste se necessário
    datas = page.query_selector_all('td.MuiTableCell-root.MuiTableCell-body.MuiTableCell-alignCenter.MuiTableCell-sizeSmall')  # Ajuste se necessário

    # Coletando os textos dos elementos
    dados_usuarios = [usuario.inner_text() for usuario in usuarios]
    dados_parametros = [parametro.inner_text() for parametro in parametros]
    dados_datas = [data.inner_text() for data in datas]

    # Verificando os dados coletados
    print(f"Usuários: {dados_usuarios}")
    print(f"Parâmetros: {dados_parametros}")
    print(f"Datas: {dados_datas}")

    # Cria um DataFrame com os dados coletados
    df = pd.DataFrame({
        "Usuario": dados_usuarios,
        "Parametros": dados_parametros,
        "Data": dados_datas
    })

    # Salva os dados em um arquivo Excel
    df.to_excel('resultados_google_playwright.xlsx', index=False)

    print("Dados salvos com sucesso!")

    # Fecha o navegador
    browser.close()
