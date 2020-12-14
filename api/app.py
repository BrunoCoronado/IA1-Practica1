from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS, cross_origin
import random
from statistics import mean 
from datetime import datetime

app = FlaskAPI(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

criterio = 1
seleccion = 1
data = []
generacion = 0
tam_poblacion = 10
tam_solucion = 4

class Nodo:

    def __init__(self, solucion = [], fitness = 0):
        self.solucion = solucion
        self.fitness = fitness

def mutar(solucion):
    if random.uniform(0, 1) <= 0.5:
        index = 0
        while index < tam_solucion:
            if random.uniform(0, 1) <= 0.5:
                solucion[index] = round(random.uniform(-2, 2), 5)
            index += 1

    return solucion

def cruzar(padre1, padre2):
    hijo = []

    index = 0

    while index < tam_solucion:
        if random.uniform(0, 1) <= 0.6:
            hijo.append(padre1.solucion[index])
        else:
            hijo.append(padre2.solucion[index])
        index += 1
    return hijo

def emparejar(padres):
    nuevaPoblacion = padres

    i = 0
    while i < tam_poblacion - len(padres): #debo asegurar al menos dos padres
        hijo = Nodo()
        index_padre1 = random.randint(0, len(padres) - 1)
        index_padre2 = random.randint(0, len(padres) - 1)
        while index_padre2 == index_padre1:
            index_padre2 = random.randint(0, len(padres) - 1)            

        hijo.solucion = cruzar(padres[index_padre1], padres[index_padre2])
        hijo.solucion = mutar(hijo.solucion)
        hijo.fitness = evaluarFitness(hijo.solucion)
        nuevaPoblacion.append(hijo)
        i += 0

    return nuevaPoblacion

def seleccionarPadres(poblacion):
    global seleccion
    if seleccion == 1: #selecion aleatoria
        padres = []

        tmp = sorted(poblacion, key=lambda item: item.fitness, reverse=False)

        padres.append(tmp[0])
        padres.append(tmp[1])
        padres.append(tmp[len(tmp) - 1])
        padres.append(tmp[len(tmp) - 2])

        return padres


        # indices = []
        # padres = []
        # cantidad_padres = random.randint(2, tam_poblacion)
        # i = 0
        # while i < cantidad_padres:
        #     index = random.randint(0, tam_poblacion - 1)
        #     while index in indices:
        #         index = random.randint(0, tam_poblacion - 1)            
        #     indices.append(index)
        #     padres.append(poblacion[index])    
        #     i += 1

        # return padres
    elif seleccion == 2: #selecion por mejor fitness (mitad de la poblacion)
        return sorted(poblacion, key=lambda item: item.fitness, reverse=False)[:tam_poblacion//2]
    else: #selecion de los pares
        #return poblacion[::2]
        padres = []
        index = 0
        while index < 5:
            if poblacion[index].fitness < poblacion[len(poblacion) - index - 1].fitness:
                padres.append(poblacion[index])
            else:
                padres.append(poblacion[len(poblacion) - index - 1])
            index += 1
        return padres

def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        print('Individuo: ', individuo.solucion, ' Fitness: ', individuo.fitness)

def imprimirMejorSolucion(poblacion, generacion):
    poblacion = sorted(poblacion, key=lambda item: item.fitness, reverse=False)
    print('\nGeneración: ', generacion, '\nMejor Solución: ', poblacion[0].solucion, '\nMejor Fitness: ', poblacion[0].fitness, '\n')

def obtenerMejorSolucion(poblacion):
    return sorted(poblacion, key=lambda item: item.fitness, reverse=False)[0]

def verificarCriterio(poblacion):
    # if generacion == 30000:
    #     return True
    global criterio
    if criterio == 1: #maximo de 5000 generaciones
        if generacion == 5000:
            return True
        return None
    elif criterio == 2:
        for sol in poblacion:
            if sol.fitness <= 1:
                return True
        return None 
    else:
        contador_soluciones = 0
        for sol in poblacion:
            if sol.fitness <= 5:
                contador_soluciones += 1

        if contador_soluciones >= (tam_poblacion // 4):
            return True
        return None 

        # media = mean([o.fitness for o in poblacion])
        # if media <= 5:
        #     return True
        # return None

def evaluarFitness(solucion):
    valorFitness = 0

    global data
    notasCalculadas = []

    for val in data:
        # NC = w1P1 + w2P2 + w3P3 + w4P4
        #print('(',solucion[0],' * ',val[0],')+(',solucion[1],' * ',val[1],')+(',solucion[2],' * ',val[2],')+(',solucion[3],' * ',val[3],')')
        #print((solucion[0] * val[0]) + (solucion[1] * val[1]) + (solucion[2] * val[2]) + (solucion[3] * val[3]))
        notasCalculadas.append((solucion[0] * val[0]) + (solucion[1] * val[1]) + (solucion[2] * val[2]) + (solucion[3] * val[3]))
        #notasCalculadas.append((0.45 * val[0]) + (0.2 * val[1]) + (0.34 * val[2]) + (0.15 * val[3]))

    sum = 0
    for i in range(len(data)):
        sum += (data[i][4] - notasCalculadas[i])**2 

    valorFitness = round((1 / len(data)) * sum, 5)

    return valorFitness

def inicializarPoblacion():
    poblacion = []

    soluciones = 0

    while soluciones < tam_poblacion:
        posiciones = 0
        solucion = []
        while posiciones < tam_solucion:
            solucion.append(round(random.uniform(-2, 2), 5))
            posiciones += 1

        poblacion.append(Nodo(solucion, evaluarFitness(solucion)))
        soluciones += 1

    return poblacion

def ejecutar():
    global generacion
    generacion = 0
    poblacion = inicializarPoblacion()

    fin = verificarCriterio(poblacion)
    
    while(fin == None):
        # print('*************** GENERACION ', generacion, " ***************")
        # imprimirPoblacion(poblacion)
        padres = seleccionarPadres(poblacion)
        poblacion = emparejar(padres)
        generacion += 1
        
        fin = verificarCriterio(poblacion)
        
    # print('*************** GENERACION ', generacion, " ***************")
    # imprimirPoblacion(poblacion)
    imprimirMejorSolucion(poblacion, generacion)
    return obtenerMejorSolucion(poblacion)

def guardarBitacora(nombre, solucion):
    f = open("bitacora.txt", "a+")
    str_criterio = {
        1: 'Maximo numero de generaciones (5000)',
        2: 'Una solucion con fitness menor o igual a 2',
        3: '25% de soluciones con fitness menor o igual a 5'
    }
    str_seleccion = {
        1: 'Mejores y Peores Padres',
        2: 'Seleccion Por Mejor Fitness',
        3: 'Seleccion Por Torneo'
    }

    now = datetime.now()
    f.write(now.strftime("%d/%m/%Y %H:%M:%S") + ';' + nombre + ';' + str_criterio[criterio] + ';' + str_seleccion[seleccion] + ';' + str(generacion) + ';[' + str(solucion.solucion[0]) + ',' + str(solucion.solucion[1]) + ',' + str(solucion.solucion[2]) + ',' + str(solucion.solucion[3]) + '];' + str(solucion.fitness) + '\n')
    f.close()
    return

@app.route("/generar", methods=['POST'])
@cross_origin()
def generar():
    """
    Genera el modelo
    """
    
    global criterio
    global seleccion
    global data

    criterio = request.json['criterio']
    seleccion = request.json['seleccion']
    data = request.json['data']

    solucion = ejecutar()
    
    guardarBitacora(request.json['nombre'], solucion)

    return jsonify(
        solucion = solucion.solucion,
        mensaje = 'Modelo generado!',
        status = 200
    )

@app.route("/bitacora", methods=['GET'])
@cross_origin()
def bitacora():
    """
    Obtener la Bitacora
    """
    
    f = open("bitacora.txt", "r")
    bitacora = f.read()

    return jsonify(
        bitacora = bitacora,
        mensaje = 'Bitácora Obtenida!',
        status = 200
    )


if __name__ == "__main__":
    app.run(debug=True)
