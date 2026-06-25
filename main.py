import csv
import win32com.client as win32
from flask import Flask, redirect, render_template, request, url_for
import pythoncom
from halo_events import halo_events_bp, adicionar_evento

app = Flask(__name__)

app.register_blueprint(halo_events_bp)

COMENTARIO_HALO = (
    "Olá, seu chamado foi recebido pelo time Arklok.\n"
    "Enviaremos um técnico até a localidade para verificar o ocorrido com o equipamento.\n\n"
    "Em breve você terá um posicionamento sobre este acionamento.\n\n"
    "Atenciosamente,\n"
    "Suporte Técnico Arklok | Equipamentos de Informática"
)

teste = False

def carregar_bases():
    bases = {}
    with open('Bases.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            base = row['BASES ATENDIDAS'].strip()
            email_base = (row['EMAIL PORTARIAS'] or '').strip()
            email_contato = (row['EMAILS_CONTATO'] or '').strip()
            if base:
                bases[base] = {'email_base': email_base, 'email_contato': email_contato}
    return bases

bases = carregar_bases()

def obter_email_por_base(base):
    info_base = bases.get(base)
    if info_base:
        email_base = info_base.get('email_base')
        print(f"Email Base: {email_base}")
        return email_base
    

def obter_email_contato_por_base(base):
    info_base = bases.get(base)
    if info_base:
        email_contato = info_base.get('email_contato')
        print(f"Email Contato: {email_contato}")  
        return email_contato

def obter_email_copia():

    emailCopia = {}
    with open('emailCopia.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            nome = row['NOME'].strip()
            email = row['EMAIL'].strip()
            if nome:
                emailCopia[nome] = email
    return emailCopia

emailCopia = obter_email_copia()

# print(emailCopia.values())
copiaString = "; ".join(emailCopia.values())

@app.route('/')
def liberacao_tecnica():
    bases = carregar_bases()
    return render_template("liberacao_tecnica.html", bases=bases)


@app.route('/teste')
def teste():
    base = request.args.get('base')
    email = obter_email_por_base(base)
    print(obter_email_por_base(base))

    redirect(url_for('liberacao_tecnica'))

    return email


@app.route('/enviar', methods=['POST'])
def liberar():

    tipo = request.form.get('tipo', 'liberacao')
    print(tipo)

    apenas_vizuar = request.form.get('apenas_visualizar')

    base = request.form.get('base')
    numero_chamado = request.form.get('numero-chamado')
    dados_tecnico = request.form.get('dados-tecnico')
    dados_tecnico = dados_tecnico.replace('\n', '<br>') 
    data_atendimento = request.form.get('data_atendimento')

    data_atendimento = data_atendimento.split('-')
    data_atendimento = f"{data_atendimento[2]}/{data_atendimento[1]}/{data_atendimento[0]}"

    email_base = obter_email_por_base(base)
    email_contato = obter_email_contato_por_base(base)

    if tipo == 'cadastro':
        assunto = f"Cadastro Técnico - {base}"
        acao = "cadastro de técnico"
        obs = f"SOLICITO CADASTRO DO TÉCNICO PARA {base}."
    else:
        assunto = f"Liberação Técnica - {base} - Chamado {numero_chamado}"
        acao = "liberação técnica"
        obs = f"OBS: SOLICITO LIBERAÇÃO PARA ATENDIMENTO TÉCNICO NA BASE PROTEGE - {base}. <br> <br> FAVOR LIBERAR O NOTEBOOK, PENDRIVE E CELULAR PARA O ATENDIMENTO TÉCNICO."

    corpo = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
            <meta charset="UTF-8">
            </head>
            <body style="margin: 0; padding: 16px; font-family: Arial, sans-serif; font-size: 14px; color: #000000; background-color: #ffffff; line-height: 1.6;">
            
            <p>Prezados, bom dia.</p>
            
            <p>Solicitamos {acao} para atendimento técnico na Base Protege. <strong>{base}</strong></p>
            
            <p>
                <span style="color: #1a73e8;">@Suporte Protege</span> Por gentileza encaminhar para base.<br>
                Segue dados:
            </p>
            
            <p>
                {dados_tecnico}<br>
            </p>
            
            <p>Atendimento ser realizado no dia {data_atendimento}. Horário comercial</p>
            
            <p>{obs}<br></p>

            
            </body>
            </html>"""
        

    pythoncom.CoInitialize()  # Inicializa o COM para a thread atual

    try:
        outlook = win32.DispatchEx("Outlook.Application")
        email = outlook.CreateItem(0)  # 0: olMailItem  
        email.display() 
        assinatura = email.HTMLBody

        corpo_final = corpo + assinatura

        email.To = f"{email_base};suporte@protege.com.br"
        if email_contato:
            email.To += f";{email_contato}"
        email.CC = copiaString
        email.Subject = assunto
        email.HTMLBody = corpo_final
        if apenas_vizuar:
            email.Display() 
        else:
            email.Display() 
            email.Send()
    finally:
        pythoncom.CoUninitialize()  # Desinicializa o COM para a thread atual
        adicionar_evento(numero_chamado, COMENTARIO_HALO)

    # print(f"Base: {base}")
    # print(f"Chamado: {numero_chamado}")
    # print(f"Técnico: {dados_tecnico}")
    # print(f"Data do Atendimento: {data_atendimento}")
    # print(f"Email da Base: {email_base}")

    return redirect(url_for('liberacao_tecnica'))

if __name__ == '__main__':
    app.run(debug=True)