from random import randint

def gerarIndividuo():
    return [0, randint(0, valorMaximoDeRandom)]

def gerandoPopulacaoAleatoria():
    todaPopulacao = []
    contadorInterno = 0
    while True:
        todaPopulacao.append(gerarIndividuo())
        if contadorInterno == populacao:
            break
        contadorInterno+=1
    return todaPopulacao

def gerarValorAleatorio():
    return randint(0, 100)

def mutacao(entrada, mutacaoValor, solucao):
    chuteParaMutacao = gerarValorAleatorio()
    if chuteParaMutacao < mutacaoValor:
        entrada = [0, randint(0, valorMaximoDeRandom)]
    """
    
    #Esta parte está atrapalhando - Ele vai gerar um individuo sempre que não houver uma mutacao

    elif entrada[0] > 5:
        entrada = gerarIndividuo()
    """
    return entrada

#Ajustando para fazer a chance de crossover   
# Definido como um crossover aritimético  
def crossover(pai, mae, mutacaoValor, solucao):
    chanceCrossover = gerarValorAleatorio()
    if chanceCrossover <= 50:
        novoIndividuo = [0, 0]

        #Melhorando a chance de diversificar
        if chanceCrossover <= 50:
            novoIndividuo[1] = ((pai[1] + mae[1]) / 2)
        else:
            novoIndividuo[1] = ((pai[1] - mae[1]) / 2)

        novoIndividuo = mutacao(novoIndividuo, mutacaoValor, solucao)
    elif chanceCrossover >= 50 and chanceCrossover <= 75:
        novoIndividuo = mutacao(mae, mutacaoValor, solucao)        
    else:
        novoIndividuo = mutacao(pai, mutacaoValor, solucao)

    novoIndividuo[0] = saidaFitness(novoIndividuo[1], solucao)

    return novoIndividuo

def saidaFitness(valor, solucao):
        return valor / solucao

def fitness(todos, populacao):
    for i in range(0, populacao):
        todos[i][0] = saidaFitness(todos[i][1],solucao)
    return todos

def SolucaoFinal(todos, populacao):
    valor = False
    for i in range(0, populacao):
        if todos[i][0] == 1:
            valor = True
    return valor

#Ajustada a roleta para ser mais precisa
def podemReproduzir(pai, mae):
    confirmar = False
    valorFiltroIndividuo = 1000
    chanceReproducao = 5
    if pai != mae:
        if (pai[0] >= valorFiltroIndividuo) or (mae[0] >= valorFiltroIndividuo):
            if gerarValorAleatorio() >= chanceReproducao:
                confirmar = True
        else:
            confirmar = True
            
    return confirmar
        
def roleta(todos):
    novaPopulacao = []
    contadorInterno = 0
    while True:
        pai = todos[randint(0, populacao-1)]
        mae  = todos[randint(0, populacao-1)]
        if podemReproduzir(pai, mae):
            novaPopulacao.append(crossover(todos[randint(0, populacao-1)], todos[randint(0, populacao-1)], mutacaoValor, solucao))
            if contadorInterno == populacao:
                break
            contadorInterno+=1
    return novaPopulacao

def apresentarSolucao(todos, populacao):
    for i in range(0, populacao):
        print("{} - Fitness: {:.2f} - Valor atual: {}".format(i+1, todos[i][0], todos[i][1]))

populacao = 50
solucao = 511
mutacaoValor = 1
modelo = 1
valorMaximoDeRandom = populacao * solucao
matarGeracaoAtual = 1000
contadorLoop = 1
parar = False
populacoes = []

#Gerações com modelos
while True:

    #Criando a nova geracao para o atual modelo
    populacaoAtual = populacoes
    populacaoAtual = fitness(gerandoPopulacaoAleatoria(), populacao)
    contador = contadorLoop

    while True:
        populacaoAtual = roleta(populacaoAtual)
        if SolucaoFinal(populacaoAtual, populacao):
            parar = True
            print("Solucao buscada: {}".format(solucao))
            print("Modelo atual: {}".format(modelo))
            print("Geração atual: {}".format(contador))
            apresentarSolucao(populacaoAtual, populacao)
            break
        else:
            if contador == matarGeracaoAtual:
                break
        contador+=1

    #Quando achar o resultado final, pare todo o while
    if parar:
        break
    modelo+=1
