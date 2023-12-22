# Load Tests
## Descripción
Estuvimos trabajando en desarrollar una herramienta de load testing para probar cuanta carga soporta un nodo de ZKSync. Si bien el desarrollo es un work-in-progress, ya se pueden hacer pruebas. Se ha trabajado principalmente en dos lineas:
- creación de un ecosistema que soporte una cantidad alta de transacciones por segundo
- desarrollo de una herramienta de load tests basada en Locust

#### Ecosistema
El desarrollo del ecosistema se basa principalmente en deployar un nodo de ZKSync Era con su respectiva base de datos y la comunicación con una L1 local. Para esto, nosotros usamos [local-setup](https://github.com/matter-labs/local-setup) pero podría usarse también zksync_stack o cualquier otra forma de levantar un nodo de ZKSync.
Luego, dadas las rich wallets iniciales del nodo, se genera la cantidad de wallets pedidas desde `config.json` con fondos suficientes para realizar las transacciones

Si bien es posible lanzar muchos requests desde una sola wallet, en las pruebas que hicimos esto no funciona. Suponiendo que la wallet partiera de un nonce N, al lanzar M requests nuevos todos estos se lanzarán con el mismo nonce, generando que muchos de ellos fallen porque la blockchain, al procesar una parte de esos M requests, va a seguir encotrando el nonce N (dado que todos los requests se enviaron con este nonce), cuando este ya quedó muy lejos del nuevo (que sería algo asi como N + M). Además, este no es un comportamiento normal en una blockchain: si bien es posible que haya N req/sec, es una anomalía que todos los requests sean de la misma wallet.

De este problema surgió la necesidad de setupear el nodo con una cantidad alta de wallets fondeadas, para correr el problema del nonce del medio. Si bien llegamos a algunas soluciones, desarrolladas en el archivo `setup.py`, el mayor problema que nos enfrentamos es la lentidud de este proceso. Creemos que este es el principal problema a resolver de los load-tests.

#### Herramienta de load test
Se le pega a un flask server que genera la comunicación via subprocess con zksync-era-cli. Por lo tanto, es una condición necesaria tener instalada esta libreria.
Es importante remarcar que elegimos usar un server de flask por dos motivos:
- Locust esta implementado para que a partir de sus pegadas http se tomen las mediciones, con lo cual facilitaba mucho el desarrollo inicial tener un server http
- Si bien se podia armar una pegada alternativa, que no usara zksync-era-cli, esto implicaba desarrollar todas las pegadas desde cero, lo cual implicaba mucho trabajo

Locust ofrece una interfaz web muy facil de usar, y que nuestro sistema soporta sin problemas. Recomendamos hacer las primeras pruebas usando esta interfaz, y luego de esto empezar a usar la pequeña CLI que dejamos armada en `main.py`. A su vez, locust tambien provee herramientas para guardar los resultados de las corridas, con lo cual no debería ser muy dificil ejecutar varias corridas con distintos parametros a traves de `main.py` y obtener de estas ejecuciones los distintos resultados para un posterior análisis

## Funcionamiento
El funcionamiento de la herramienta esta descripto en detalle en el archivo `README.md`. Es importante levantar el server de Flask y luego ejecutar los loadtest, dado que Locust por default hace pedidos HTTP y por lo que averiguamos las salidas que no incluian un server eran bastante mas costosas en tiempo, dado que implican reimplementar ciertas partes de la libreria. Invitamos a quien siga este proceso a revisar esta decisión.

## Desarrollo futuro
A continuación describiremos los desarrollos pendientes que nos quedaron en el tintero. Estos se dividen en dos categorías: por un lado, los desarrollos que son necesarios para asegurar que la herramienta pueda ser utilizada sin problemas (o sea, terminar las partes WIP) y, por otro lado, aquellos que harían que la herramienta tenga un mayor alcance (o sea, features).

### Lineas de desarrollo inmediatas
- Fondeo de wallets con eth y con ERC20. Si bien el setup corre las funciones `create_wallets_with_money` y `create_erc20_wallets_with_money` estas funciones tardan mucho en ejecutarse. Estuvimos trabajando alternativas pero no encontramos ninguna que mejore sustancialmente la velocidad de este proceso. Una posibilidad interesante que encontramos es la de lanzar varios subprocesos desde muchas wallets fondeadas (por ej: si de 1 wallet fondeada podes generar 10 nuevas con 1/10 de la plata, podrias correr 10 transacciones a la par. Si logras de esas 10 generar 50, podes correr 50 transacciones a la par)
- Posibilidad de reutilizar el mismo contrato ERC20 en más de una corrida, evitando así que el setup de las wallets con sus respectivos tokens deba ejecutarse cada vez

### Lineas de desarrollo 
- Agregar `deposit` y `withdraw` contra la L1

- Extender las pruebas. Si bien las herramientas para hacer las pruebas estan avanzadas, no hicimos pruebas con una cantidad de usuarios mayor a 1000. Esto no nos permitió llegar a ver pruebas con 100 reqs/sec y analizar en detalle el funcionamiento del nodo.

- Mejorar la comunicación con la blockchain. Hay tres capas hoy en dia: locust se comunica con flask, que a su vez lanza un subprocess que le pega a zksync-era-cli, que a su vez se comunica con el nodo.

- Nodo con prover. Javi nos dio esta idea y no la avanzamos, porque no llegamos a terminar las pruebas mas básicas, pero la idea era que estas mismas pruebas se hagan, en una segunda instancia, contra un nodo de zksync con prover

- Ver la posibilidad de obtener valores sobre el rendimiento del host. Locust no provee herramientas para analizar el rendimiento de la CPU donde se ejecuta el nodo, con lo cual solo se obtiene data sobre los tiempos de ejecución de las instrucciones. Obtener esta info sería de gran ayuda para entender como funciona el nodo con grandes cargas de trabajo.