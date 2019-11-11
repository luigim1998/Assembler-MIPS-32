def decimalToBinary(n, largura):  
    binary = ''
    if(n == 0):
        return '0'
    else:
        while(n > 0):
            binary = str(n%2) + binary
            n = n//2
    if(len(binary)   > largura):
        return binary[-largura:]
    elif(len(binary) < largura):
        return '0'*(largura-len(binary)) + binary

def validate_reg(nome):
    return nome in registradores

def validate_imm(imm):
    return imm.isdigit()

def instrucao_i(linha):
    """
    Retorna a instrução em binário.
    :parâmetro linha: a linha do código.
    :return: Binário da instrução.
    """
    #TODO: verificar o parâmetro e analisar se é número ou endereço de memória
    linha = linha.split(maxsplit=1)
    if(linha[0] in ['bgez', 'bgezal', 'bgtz', 'blez', 'bltz', 'bltzal', 'lui']): #instrução reg, imediato
        campos = linha[1].split(',')
        if(len(campos) == 2):
            campos = [i.strip() for i in campos] #apaga os espaços vazios
            if(validate_reg(campos[0])):
                if(validate_imm(campos[1])): #é uma instrução válida
                    if(linha[0] in ['lui']):
                        aux = opcode_i[linha[0]][0] + '00000' + registradores[campos[0]][0] + decimalToBinary(int(campos[1]), 16)
                    else:
                        aux = opcode_i[linha[0]][0] + registradores[campos[0]][0] + '00001' + decimalToBinary(int(campos[1]), 16)
                    binario.append(aux)
                else:
                    raise Exception("'{}': Campo imediato inválido".format(codigo[i]))
            else:
                raise Exception("'{}': nome de registrador inválido".format(codigo[i]))
        else:
            raise Exception("'{}': Formato dos campos inválidos".format(codigo[i]))
    elif(linha[0] in ['addi', 'addiu', 'andi', 'lui', 'ori', 'slti','sltiu', 'xori']): #instrução reg, reg, imediato
        campos = linha[1].split(',')
        if(len(campos) == 3):
            campos = [i.strip() for i in campos] #apaga os espaços vazios
            if(validate_reg(campos[0]) and validate_reg(campos[1])):
                if(validate_imm(campos[2])): #é uma instrução válida
#TODO: CONTINUAR CÓDIGO
#        #elif(linha[0] in []): #instrução reg, offset(reg)

codigo = []
registradores = {}
opcode_i = {}
opcode_j = {}
opcode_r = {}
labels = {}
binario = []

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
        opcode_j[linha[0]] = linha[1:] #adiciona no dicionário

        linha = f.readline()

with open('OPCODE_I.txt', 'r') as f: #este arquivo possui os opcodes do tipo R
    linha = f.readline()
    while(linha.strip() != ''):
        linha = linha.lower()
        linha = linha.strip() #retira os espaços no começo e final da linha
        linha = linha.split() #separa o registrador e o binário
        opcode_i[linha[0]] = linha[1:] #adiciona no dicionário

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

        if(linha[2].strip() == ''): #caso a linha só tem a label
            codigo.pop(cont) #apaga a linha
        else:
            codigo[cont] = linha[2].strip()

    elif(codigo[cont].count(':') > 1): #não pode haver mais de dois ':'
        raise Exception('Sintaxe inválida')
    cont += 1

for i in range(0, len(codigo)): #leitura do código
    inst = codigo[i].split(maxsplit=1)
    if(inst[0] in opcode_i):
        binario.append( instrucao_i(codigo[i]) )
    elif (inst[0] in opcode_j):
    elif (inst[0] in opcode_r):
    else:
        raise Exception('Instrução não reconhecida')


print(registradores)
print(opcode_i)
print(opcode_j)
print(opcode_r)
print(codigo)
print(labels)