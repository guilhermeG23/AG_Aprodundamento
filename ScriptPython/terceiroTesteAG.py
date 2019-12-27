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

def mutacao(entrada, mutacaoValor, solucao):
    chuteParaMutacao = randint(0, 100)
    if chuteParaMutacao < mutacaoValor:
        entrada[1] = randint(0, valorMaximoDeRandom)
        entrada[0] = saidaFitness(entrada[1], solucao)
    """
    
    #Esta parte está atrapalhando - Ele vai gerar um individuo sempre que não houver uma mutacao

    elif entrada[0] > 5:
        entrada = gerarIndividuo()
    """
    return entrada

#Ajustando para fazer a chance de crossover        
def crossover(pai, mae, mutacaoValor, solucao):
    chanceCrossover = randint(0, 100)
    if chanceCrossover < 50:
        novoIndividuo = [0, 0]

        #Melhorando a chance de diversificar
        if chanceCrossover <= 50:
            novoIndividuo[1] = ((pai[1] + mae[1]) / 2)
        else:
            novoIndividuo[1] = ((pai[1] - mae[1]) / 2)

        novoIndividuo[0] = saidaFitness(novoIndividuo[1], solucao)
        novoIndividuo = mutacao(novoIndividuo, mutacaoValor, solucao)
    elif chanceCrossover >= 50 and chanceCrossover <= 75:
        novoIndividuo = mutacao(mae, mutacaoValor, solucao)        
    else:
        novoIndividuo = mutacao(pai, mutacaoValor, solucao)
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
            if randint(0, 100) >= chanceReproducao:
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
        print("Fitness: {:.2f} - Valor atual: {}".format(todos[i][0], todos[i][1]))

populacao = 10
solucao = 21
mutacaoValor = 5
modelo = 1
valorMaximoDeRandom = populacao * solucao
matarGeracaoAtual = 1000
parar = False

#Gerações com modelos
while True:

    #Criando a nova geracao para o atual modelo
    populacaoAtual = []
    populacaoAtual = fitness(gerandoPopulacaoAleatoria(), populacao)
    contador = 1

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
