import requests as req
import time

consulta_pokemon='https://pokeapi.co/api/v2/pokemon/{id_or_name}/'
consulta_movimiento="https://pokeapi.co/api/v2/move/{name}/"
consulta_balls="https://pokeapi.co/api/v2/item-category/{id}/"
consulta_evoluciones="https://pokeapi.co/api/v2/pokemon-species/{id_or_name}/"

def consultar_api (endpoint) :
    response = req.get(endpoint)
    if response.status_code != 200 :
        menu=0
    else:
        return response.json()

#Mira si se ha añadido algún pokémon desde la última modificación y se actualiza
numero_limite=905
while(consultar_api(consulta_evoluciones.replace('{id_or_name}',str(numero_limite))) is not None):
    numero_limite=numero_limite+1

numero_limite=numero_limite-1 #Como el últim no se encontró, se descuenta del límite
numero_formas=consultar_api("https://pokeapi.co/api/v2/pokemon/")["count"]

menu=3
while(menu>0):
    print("\nBienvenido a la app con conexión a la PokeApi.")
    print("\nHay registrados actualmente "+str(numero_limite)+" Pokémons")
    print("¿Qué desea realizar?")
    print("1. Buscar Pokemón por su número actual de Pokedex.")
    print("2. Buscar Pokemón por su nombre.")
    print("3. Ver el número de formas Pokémons existentes.")
    print("4. Consultar un movimiento.")
    print("5. Consultar tipos de Pokeballs.")
    print("0. Salir")
    menu=int(input("Introduzca la opción: "))

    if menu>=1 or menu<=5:
        
        if menu==1:
            numero=0
            while int(numero)<1 or int(numero)>numero_limite:
                numero=input("\nIntroduzca su número en la Pokedex: ")
            #Realiza la consulta
            respuesta=consultar_api(consulta_pokemon.replace('{id_or_name}',numero))
        if menu==2:
            nombre=input("Introduzca su nombre: ").lower() #El nombre debe ir en minúsculas para el endpoint
            #Realiza la consulta
            respuesta=consultar_api(consulta_pokemon.replace('{id_or_name}',nombre))

        if (menu==2 or menu==1) and menu!=0:
            #Saca el nombre a partir del número y viceversa
            nombre=respuesta['name'].title()
            numero=str(respuesta['id'])
            print("\nNombre: " + nombre)
            print("Número: "+ numero + " en la Pokedex\n")

            #Muestra los tipos que tiene
            for i in respuesta['types']:
                print("Es de tipo: "+ i["type"]["name"])

            #Muestra las estadístocas del Pokemón
            print("")
            estadisticas = respuesta['stats']
            base_stats = {}
            for stat in estadisticas:
                stat_name = stat['stat']['name'].title()
                base_stat = stat['base_stat']
                print("{0:15}  {1}".format(stat_name, base_stat))

            #Evoluciones
            linea_evolutiva=consultar_api(consulta_evoluciones.replace('{id_or_name}',numero))
            if(linea_evolutiva['evolution_chain'] is not None):
                linea_evolutiva=linea_evolutiva['evolution_chain']["url"]
                evoluciones=consultar_api(linea_evolutiva)
                if(evoluciones["chain"]["evolves_to"]==[]):
                    print("\nEste Pokemón no evoluciona")
                else:
                    print("\nSu forma base (la que nace de un huevo) es:")
                    print(evoluciones["chain"]["species"]["name"])

                    evoluciones=evoluciones["chain"]
                    while(evoluciones["evolves_to"]!=[]):
                        aux=evoluciones
                        evoluciones=evoluciones["evolves_to"][0]
                        print("Este último evoluciona a:")
                        print(evoluciones["species"]["name"])
                    
                    #Comprueba si hay más alternativas evolutivas
                    for i in range(len(aux["evolves_to"])):
                        if i!=0:
                            evoluciones=aux["evolves_to"][i]
                            print("Otra alternativa es que evolucione a:")
                            print(evoluciones["species"]["name"])
            else:
                print("\nEste Pokemón no evoluciona")

            #Delay hasta la siguiente aparición del menú
            time.sleep(2)


        if menu==3:
            print("\nActualmente existen: "+str(numero_formas)+" formas de Pokémons")
            print("Para: "+str(numero_limite)+" Pokémons diferentes")
            print("Recuerde que algunos Pokémons tienen varias formas, por lo que el número en Pokedex es inferior")
            time.sleep(2)
        
        if menu==4:
            movimiento=input("\nIntroduzca su nombre en inglés: ").lower()
            respuesta=consultar_api(consulta_movimiento.replace('{name}',movimiento))
            if menu!=0:
                print("\nNombre oficial: " + respuesta['name'].title())
                if respuesta['names'][5]["language"]["name"] == "es":
                    print("También conocido como: " + respuesta['names'][5]["name"].title())
                print("Probabilidad de éxito: " + str(respuesta['accuracy']))
                print("Poder o daño que inflige al enemigo: " + str(respuesta['power']))
                print("Puntos de poder disponibles (PP): " + str(respuesta['pp']))
                time.sleep(2)

        if menu==5:
            respuesta=consultar_api(consulta_balls.replace('{id}','34'))
            especiales=input("¿Desea incluir las Pokeballs especiales (Y/n)? ").lower()
            print("")
            for i in respuesta["items"]:
                print(i["name"])
            if especiales!="no" and especiales!="n":
                respuesta=consultar_api(consulta_balls.replace('{id}','33'))
                for i in respuesta["items"]:
                    print(i["name"])
            time.sleep(2)
    else:
        print("\nHasta pronto")
        menu=-1