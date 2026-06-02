import csv

def carregar_bases():
    bases = []
    with open('Bases.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            base = row['BASES ATENDIDAS'].strip()
            email_base = row['EMAIL PORTARIAS'].strip()
            if base:
                bases.append((base, email_base))
    return bases

def obter_email_por_base(base):
    bases = carregar_bases()
    for b, email in bases:
        if b == base:
            return email
    return None

bases = carregar_bases()
# print(bases)

exemplo = "PROTEGE - CAMPINAS"
email_base = obter_email_por_base(exemplo)


print(f"Email para {exemplo}: {email_base}")