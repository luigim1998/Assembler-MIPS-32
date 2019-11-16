def flip(c):
	return '1' if (c == '0') else '0'

def printOneAndTwosComplement(numero): 
    '''Retorna a binário no complemento a 2
    :parâmetro bin: número.
    :return: Binário do número.
    '''
    bin = "{0:b}".format(numero) if (numero >= 0) else "{0:b}".format(-numero)
    n = len(bin)
    ones = "" 
    twos = "" 

    # inverte os bits 
    for i in range(n): 
        ones += flip(bin[i]) 

    # soma o binário com 1 
    ones = list(ones.strip("")) 
    twos = list(ones) 
    for i in range(n - 1, -1, -1): 
	
        if (ones[i] == '1'): 
            twos[i] = '0'
        else:		 
            twos[i] = '1'
            break
		
    # Se o bit mais significativo for 1, 
    # incrementa um no final 
    if (i == -1): 
        twos.insert(0, '1') 

    aux = ''
    for i in twos:
        aux += i
    
    return aux
	
# A função original printOneAndTwosComplement() e flip() 
# foi contribuída por SHUBHAMSINGH10 e está disponível em: 
# https://www.geeksforgeeks.org/1s-2s-complement-binary-number/

def decimalToBinary(n, largura):
    binary = printOneAndTwosComplement(n)
    if(len(binary) > largura):
        return binary[-largura:]
    else:
        if(n >= 0):
            return '0'*(largura - len(binary)) + binary
        else:
            return '1'*(largura - len(binary)) + binary

def validate_reg(nome):
    return nome in registradores

def validate_imm(imm):
    return imm[1:].isdigit() if (imm[0] == '-') else imm.isdigit()

def validate_uns(uns):
    return uns.isdigit()

def validate_label(label):
    return label in labels

def validate_parentese(linha):
    if(linha.count('(') == 1 and linha.count(')') == 1):
        return linha.find('(') < linha.find(')')
    else:
        return False

def tratar_linha(linha):
    campos = linha.split(maxsplit=1)
    if(len(campos) >= 2):
        campos.extend(campos[1].split(','))
        campos.pop(1)
        campos = [i.strip() for i in campos] #apaga os espaços vazios
    return campos

def tratar_parentese(linha):
    if(not validate_parentese(linha)):
        raise Exception('{}: Parênteses inválidos'.format(linha))
    aux = tratar_linha(linha)
    if(len(aux) == 3):
        aux[2] = aux[2].replace(')', '')
        aux.extend(aux[2].split('('))
        aux.pop(2)
        aux = [i.strip() for i in aux] #apaga os espaços vazios
        return aux
    else:
        raise Exception('{}: Formato dos campos inválidos'.format(linha))

def instrucao_i(linha):
    """
    Retorna a instrução tipo I em binário.
    :parâmetro linha: a linha do código.
    :return: Binário da instrução.
    """
    campos = tratar_linha(linha)

    if(campos[0] in ['bgez', 'bgezal', 'bgtz', 'blez', 'bltz', 'bltzal', 'lui']): #instrução reg, imediato
        
        #verifica por erros
        if(len(campos) != 3):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not validate_reg(campos[1])):
            raise Exception("'{}': nome de registrador inválido".format(linha))
        
        if(campos[0] in ['lui']): #instrução rt, imediato
            if(validate_uns(campos[2])): #é uma instrução válida
                return opcode_i[campos[0]][0] + '00000' + registradores[campos[1]] + decimalToBinary(int( campos[2] ), 16)
            else:
                raise Exception("'{}': Campo imediato inválido".format(linha))
                
        else: #instrução rs, label
            if(validate_label(campos[2])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[1]] + opcode_i[campos[0]][1] + decimalToBinary(int( labels[campos[2]] ), 16)
            else:
                raise Exception("'{}': Campo de label inválido".format(linha))

    elif(campos[0] in ['addi', 'addiu', 'andi', 'beq', 'bne', 'ori', 'slti', 'sltiu', 'xori']): #instrução reg, reg, imediato
        #verifica erros
        if(len(campos) != 4):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[1]) and validate_reg(campos[2])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        if(campos[0] in ['addi', 'andi', 'ori', 'slti', 'xori']): #instrução rt, rs, imediato
            if(validate_imm(campos[3])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[2]] + registradores[campos[1]] + decimalToBinary(int(campos[3]), 16)
            else:
                raise Exception("'{}': Campo imediato inválido".format(linha))
        elif(campos[0] in ['addiu', 'sltiu']): #instrução rt, rs, unisgned
            if(validate_uns(campos[3])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[2]] + registradores[campos[1]] + decimalToBinary(int(campos[3]), 16)
            else:
                raise Exception("'{}': Campo imediato unsigned inválido".format(linha))
        else: #instrução rs, rt, label
            if(validate_label(campos[3])): #é uma instrução válida
                return opcode_i[campos[0]][0] + registradores[campos[1]] + registradores[campos[2]] + decimalToBinary(int(labels[campos[3]]), 16)
            else:
                raise Exception("'{}': Campo de label inválido".format(linha))
    elif(campos[0] in ['break', 'syscall']): #instrução break
        if(len(campos) == 1):
            return opcode_i[campos[0]][0] + '0'*20 + opcode_i[campos[0]][1]
        else:
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
    else: #instrução rt, offset(rs) (lb, lbu, lh, lhu, lw, sb, sh, sw)
        campos = tratar_parentese(linha)
        #verifica erros
        if(len(campos) != 4):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[1]) and validate_reg(campos[3])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))
        if(campos[0] in ['lbu', 'lhu']):
            if(not (validate_uns(campos[2])) ):
                raise Exception("'{}': Campo imediato unsigned inválido".format(linha))
        else:
            if(not (validate_imm(campos[2])) ):
                raise Exception("'{}': Campo imediato inválido".format(linha))

        return opcode_i[campos[0]][0] + registradores[campos[3]] + registradores[campos[1]] + decimalToBinary(int(campos[2]), 16)

def instrucao_j(linha):
    """
    Retorna a instrução tipo J em binário.
    :parâmetro linha: a linha do código.
    :return: Binário da instrução.
    """
    campos = tratar_linha(linha)

    if(campos[0] in ['j', 'jal']): #instrução label
        if(len(campos) != 2):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not validate_label(campos[1])):
            raise Exception("'{}': Campo de label inválido".format(linha))
        return opcode_j[campos[0]][0] + decimalToBinary(int( labels[campos[1]] ), 26)
    
    elif(campos[0] in ['jalr']): #instrução rd, rs
        if(len(campos) != 3):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[1]) and validate_reg(campos[2])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))
        return opcode_j[campos[0]][0] + registradores[campos[2]] + opcode_j[campos[0]][1] + registradores[campos[1]] + opcode_j[campos[0]][2] + opcode_j[campos[0]][3]
    else: #instrução rs (instrução jr)
        if(len(campos) != 2):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not validate_reg(campos[1]) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))
        return opcode_j[campos[0]][0] + registradores[campos[1]] + opcode_j[campos[0]][1]

def instrucao_r(linha):
    """
    Retorna a instrução tipo R em binário.
    :parâmetro linha: a linha do código.
    :return: Binário da instrução tipo R.
    """
    campos = tratar_linha(linha)

    if(campos[0] in ['add', 'addu', 'and', 'nor', 'or', 'slt', 'sltu', 'srlv', 'sub', 'subu', 'xor']): #instrução rd, rs, rt

        if(len(campos) != 4):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[2]) and validate_reg(campos[3]) and validate_reg(campos[1])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        return opcode_r[campos[0]][0] + registradores[campos[2]] + registradores[campos[3]] + registradores[campos[1]] + opcode_r[campos[0]][1] + opcode_r[campos[0]][2]
    
    elif(campos[0] in ['div', 'divu', 'mult', 'multu']): #instrução rs, rt
        if(len(campos) != 3):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[1]) and validate_reg(campos[2])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        return opcode_r[campos[0]][0] + registradores[campos[1]] + registradores[campos[2]] + opcode_r[campos[0]][1] + opcode_r[campos[0]][2]

    elif(campos[0] in ['mfc0', 'mtc0']): #instrução rt, rd
        if(len(campos) != 3):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not (validate_reg(campos[1]) and validate_reg(campos[2])) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        return opcode_r[campos[0]][0] + opcode_r[campos[0]][1] + registradores[campos[1]] + registradores[campos[2]] + opcode_r[campos[0]][2]
    
    elif(campos[0] in ['mfhi', 'mflo']): #instrução rd
        if(len(campos) != 2):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not validate_reg(campos[1]) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        return opcode_r[campos[0]][0] + opcode_r[campos[0]][1] + registradores[campos[1]] + opcode_r[campos[0]][2] + opcode_r[campos[0]][3]

    elif(campos[0] in ['mthi', 'mtlo']): #instrução rs
        if(len(campos) != 2):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not validate_reg(campos[1]) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        return opcode_r[campos[0]][0] + registradores[campos[1]] + opcode_r[campos[0]][1] + opcode_r[campos[0]][2]

    elif(campos[0] in ['sll', 'sra', 'srl']): #instrução rd, rt, sa
        if(len(campos) != 4):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not ( validate_reg(campos[1]) and validate_reg(campos[2]) ) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))
        if(not validate_imm(campos[3]) ):
            raise Exception("'{}': campo de shamt inválido".format(linha))

        return opcode_r[campos[0]][0] + '00000' + registradores[campos[2]] + registradores[campos[1]] + decimalToBinary(int(campos[3]), 5) + opcode_r[campos[0]][1]

    elif(campos[0] in ['sllv', 'srav', 'srlv']): #instrução rd, rt, rs
        if(len(campos) != 4):
            raise Exception("'{}': Formato dos campos inválidos".format(linha))
        if(not ( validate_reg(campos[1]) and validate_reg(campos[2]) and validate_reg(campos[3]) ) ):
            raise Exception("'{}': nome de registrador inválido".format(linha))

        return opcode_r[campos[0]][0] + registradores[campos[3]] + registradores[campos[2]] + registradores[campos[1]] + opcode_r[campos[0]][1] + opcode_r[campos[0]][2]


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
            cont += 1

    elif(codigo[cont].count(':') > 1): #não pode haver mais de dois ':'
        raise Exception('Sintaxe inválida')

    else:
        cont += 1

for i in range(0, len(codigo)): #leitura do código
    inst = codigo[i].split(maxsplit=1)
    if(inst[0] in opcode_i):
        binario.append( instrucao_i(codigo[i]) )
    elif (inst[0] in opcode_j):
        binario.append( instrucao_j(codigo[i]) )
    elif (inst[0] in opcode_r):
        binario.append( instrucao_r(codigo[i]) )
    else:
        raise Exception('Instrução não reconhecida')


with open('binario.txt', 'w') as f:
    for linha in binario:
        f.write(linha + '\n')


print(registradores)
print()
print(opcode_i)
print()
print(opcode_j)
print()
print(opcode_r)
print()
print(codigo)
print()
print(labels)