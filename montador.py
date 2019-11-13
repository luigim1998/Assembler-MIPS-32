def decimalToBinary(n, largura):  
    binary = ''
    if(n == 0):
        return '0'
    else:
        while(n > 0):
            binary = str(n%2) + binary
            n = n//2
    if(len(binary) > largura):
        return binary[-largura:]
    else:
        return "{0:{fill}{align}{width}}".format(binary, width = largura, fill='0', align='>')

def validate_reg(nome):
    return nome in registradores

def validate_imm(imm):
    return imm.isdigit()

def validate_label(label):
    return label in labels

def tratar_linha(linha):
    campos = linha.split(maxsplit=1)
    if(len(campos) >= 2):
        campos.extend(campos[1].split(','))
        campos.pop(1)
        campos = [i.strip() for i in campos] #apaga os espaços vazios
    return campos

def instrucao_i(linha):
    """
    Retorna a instrução em binário.
    :parâmetro linha: a linha do código.
    :return: Binário da instrução.
    """
    #TODO: verificar o parâmetro e analisar se é número ou endereço de memória
    campos = tratar_linha(linha)

    if(campos[0] in ['bgez', 'bgezal', 'bgtz', 'blez', 'bltz', 'bltzal', 'lui']): #instrução reg, imediato
        
        #verifica por erros
        if(len(campos) != 3):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not validate_reg(campos[1])):
            raise Exception("'{}': nome de registrador inválido".format(linha))
        
        if(campos[0] in ['lui']): #instrução rt, imediato
            if(validate_imm(campos[2])): #é uma instrução válida
                return opcode_i[campos[0]][0] + '00000' + registradores[campos[1]][0] + decimalToBinary(int(campos[2]), 16)
            else:
                raise Exception("'{}': Campo imediato inválido".format(linha))
                
        else: #instrução rs, imediato
            if(validate_label(campos[2])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[1]][0] + opcode_i[campos[0]][1] + decimalToBinary(int(campos[2]), 16)
            else:
                raise Exception("'{}': Campo de label inválido".format(linha))

    elif(campos[0] in ['addi', 'addiu', 'andi', 'beq', 'bne', 'ori', 'slti', 'sltiu', 'xori']): #instrução reg, reg, imediato
        #verifica por erros
        if(len(campos) != 4):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[1]) and validate_reg(campos[2])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        if(campos[0] in ['addi', 'addiu', 'andi', 'ori', 'slti', 'sltiu', 'xori']): #instrução rt, rs, imediato
            if(validate_imm(campos[3])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[1]][0] + registradores[campos[2]][0] + decimalToBinary(int(campos[3]), 16)
            else:
                raise Exception("'{}': Campo imediato inválido".format(linha))
        else: #instrução rs, rt, label
            if(validate_label(campos[3])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[1]][0] + registradores[campos[2]][0] + decimalToBinary(labels[campos[3]], 16)
            else:
                raise Exception("'{}': Campo de label inválido".format(linha))
    elif(campos[0] in ['break', 'syscall']): #instrução break
        if(len(campos) == 1):
            return opcode_i[campos[0]][0] + '0'*20 + opcode_i[campos[0]][1]
        else:
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
    else: #instrução rt, offset(rs) (lb, lbu, lh, lhu, lw, sb, sh, sw)

#TODO: CONTINUAR CÓDIGO, colocar registradores nos comentários
    elif(linha[0] in []): #instrução reg, offset(reg)

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