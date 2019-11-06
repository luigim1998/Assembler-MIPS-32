codigo = []

with open('teste1.asm', 'r') as f:
    linha = f.readline()
    while(linha != ''):
        linha = linha.lower() #deixa tudo minúsculo
        linha = linha.partition("#") #separa os comentários
        linha = linha[0] #a linha fica com o código
        linha = linha.strip() #retira os espaços no começo e final da linha
        print(linha)
        linha = linha.split(maxsplit=1)
        print(linha)

        codigo.append(linha)

        linha = f.readline()

print(codigo)