import os

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = os.getenv('USERNAME_SEF')
password = os.getenv('PASSWORD_SEF')
driver = None


def start_chrome():
    global driver
    driver_path = 'driver/chromedriver'

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    # Inicializar o navegador Chrome
    driver = webdriver.Chrome(options=options)

    # URL do site
    url = 'https://www.sef.pt/pt/Pages/Homepage.aspx'

    driver.get(url)
    print('Navegador iniciado')
    return driver


def close_chrome():
    global driver
    driver.quit()
    print("Navegador fechado.")


def iniciar_login():
    login_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'login-launcher'))
    )

    # Clicar no botão "Login"
    login_button.click()

    print("Botão 'Login' clicado com sucesso! -- OK")


def insert_user_pass():
    user_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'txtUsername'))
    )
    pass_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'txtPassword'))
    )
    user_input.send_keys(username)
    pass_input.send_keys(password)

    print("Login e senha inseridos com sucesso! -- OK")


def select_login_button():
    # Localizar o botão de pesquisa pelo ID
    login_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'btnLogin'))
    )

    # Clicar no botão de pesquisa
    login_button.click()

    print("Clicar no botão ENTRAR! -- OK")


def select_agendamento():
    # elemento do botao de resultado da pesquisa
    
    try:
        agendamento_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_ctl53_g_59a32ede_8107_49fd_89e4_d64dcb5b7c73_ctl00_Scheduling'))
        )

        try:
            agendamento_button.click()
            print("Selecionar Agendamentos! -- OK")
            return True
        
        except NoSuchElementException:
            print('Botao agendamento nao encontrado -- NOK')
            return False
        
    except TimeoutException:
        print('Login nao realizado -- NOK')
        return False
    

def novo_agendamento():
    # Aguardar até que o botão 'proximoButton' seja visível
    novo_agendamento_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "btnNovoAgendamento"))
    )

    # Clicar no botão 'proximoButton'
    novo_agendamento_button.click()

    print("Clicar em novo agendamento! -- OK")


def verifica_mensagem():
    # Aguardar até que o elemento 'IdDistrito' seja visível
    try:
        menssagem_erro_label = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_ctl53_g_948e31d8_a34a_4c4d_aa9f_c457786c05b7_ctl00_lblPostosEmpty'))
        )

        assert menssagem_erro_label.text == 'De momento, não existe disponibilidade nos postos de atendimento para o serviço selecionado.', \
            'Mensagem de erro não corresponde ao esperado.'
        print('Não existe disponibilidade para o serviço selecionado. -- OK')

    except Exception as e:
        print(f'Erro durante a verificação da mensagem: {str(e)} -- NOK')
        raise AssertionError('Falha ao verificar a mensagem de erro.')





# Cenários de teste
def exec_test_full():
    max_attempts = 4
    attempts = 0

    while attempts < max_attempts:
        try:
            print(f"Tentativa {attempts + 1} de {max_attempts}...")
            start_chrome()
            iniciar_login()
            insert_user_pass()
            select_login_button()
            break
        except Exception as e:
            attempts += 1
            print(f"Tentativa {attempts} falhou: {str(e)} -- Retentando...")
            close_chrome()

            if attempts >= max_attempts:
                print("Número máximo de tentativas atingido. Teste falhou.")
                raise

    try:

        select_agendamento()
        novo_agendamento()
        verifica_mensagem()
    finally:
        close_chrome()


#driver = start_chrome()

exec_test_full()


