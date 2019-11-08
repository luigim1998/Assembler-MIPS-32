codigo = []
registradores = {}
opcode_i = {}
opcode_j = {}
opcode_r = {}
labels = {}

with open('REGISTERS.txt', 'r') as f: #este arquivo possui os registradores
    linha = f.readline()
    while(linha != ''):
        linha = linha.lower()
        linha = linha.strip() #retira os espaços no começo e final da linha
        linha = linha.split() #separa o registrador e o binário
        registradores[linha[0]] = linha[1] #adiciona no dicionário
        linha = f.readline()

with open('OPCODE_R.txt', 'r') as f: #este arquivo possui os opcodes do tipo R
    linha = f.readline()
    while(linha.strip() != ''):
        linha = linha.lower()
        linha = linha.strip() #retira os espaços no começo e final da linha
        linha = linha.split() #separa o registrador e o binário
        opcode_r[linha[0]] = linha[1:] #adiciona no dicionário

        linha = f.readline()

with open('OPCODE_J.txt', 'r') as f: #este arquivo possui os opcodes do tipo R
    linha = f.readline()
    while(linha.strip() != ''):
        linha = linha.lower()
        linha = linha.strip() #retira os espaços no começo e final da linha
        linha = linha.split() #separa o registrador e o binário
        opcode_j[linha[0]] = linha[1] #adiciona no dicionário

        linha = f.readline()

with open('OPCODE_I.txt', 'r') as f: #este arquivo possui os opcodes do tipo R
    linha = f.readline()
    while(linha.strip() != ''):
        linha = linha.lower()
        linha = linha.strip() #retira os espaços no começo e final da linha
        linha = linha.split() #separa o registrador e o binário
        opcode_i[linha[0]] = linha[1] #adiciona no dicionário

        linha = f.readline()

with open('teste1.asm', 'r') as f:
    linha = f.readline()
    while(linha != ''):
        linha = linha.lower() #deixa tudo minúsculo
        linha = linha.partition("#") #separa os comentários
        linha = linha[0] #a linha fica com o código
        linha = linha.strip() #retira os espaços no começo e final da linha
        if(linha != ''): #adiciona se não for uma linha vazia
            codigo.append(linha)

        linha = f.readline()

cont = 0
while(cont < len(codigo)): #busca por labels
    if(codigo[cont].count(':') == 1): #busca por labels
        linha = codigo[cont].partition(':') #separa o código da label

        if(len(linha[0]) == 0): #tamanho da label não pode ser zero
            raise Exception('Sintaxe incorreta')

        if(not( linha[0][0].isalpha()) ): #label não pode começar com número
            raise Exception('Nome de label inicia somente com número')

        for i in linha[0]:
            if(not (i.isalpha() or i.isdigit())): #label pode ter somente número e letra
                raise Exception('Nome de label inválida')

        if(linha[0] not in labels): #adiciona a label
            labels[linha[0]] = cont
        else: #a label já foi declarada
            raise Exception("'{}' está definido múltiplas vezes".format(linha[0]) )
        
        print(linha)

        if(linha[2].strip() == ''): #caso a linha só tem a label
            codigo.pop(cont) #apaga a linha
        else:
            codigo[cont] = linha[2].strip()

    elif(codigo[cont].count(':') > 1): #não pode haver mais de dois ':'
        raise Exception('Sintaxe inválida')
    cont += 1

for i in codigo: #leitura do código
    linha = i.split(maxsplit=1)
    if(linha[0] in opcode_i):
        if(linha[0] in ['bgez', 'bgezal', 'bgtz', 'blez', 'bltz', 'bltzal', 'lui']): #instrução reg, imediato
            campos = linha[1].split(',')
        elif(linha[0] in []): #instrução reg, reg, imediato
        elif(linha[0] in []): #instrução reg, offset(reg)
        
    elif (linha[0] in opcode_j):
    elif (linha[0] in opcode_r):
    else:
        raise Exception('Instrução não reconhecida')


print(registradores)
print(opcode_i)
print(opcode_j)
print(opcode_r)
print(codigo)
print(labels)