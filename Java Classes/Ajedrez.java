import java.io.EOFException;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Scanner;

/**Clase principal del juego. Gestiona el resto de objetos "Piezas" "Tablero" y "Config"*/
public class Ajedrez {
	
	//Constante que marca la cantidad de lineas que se usan para limpiar la pantalla
	static final int LINEAS = 30;
	
	//Entrada de datos utilizada en todo el programa
	static Scanner kb = new Scanner(System.in);

	/**Main, gestiona las ordenes principales del programa*/
	public static void main(String[] args) {

		//Comprobación de que se han enviado los argumentos correctos al iniciar el juego
		if(args.length != 2){
			System.err.println("Invocación erronea\nUso: <java Ajedrez \"ruta partidas.arp\" \"ruta config.arp\">");
			return;
			}

		
		kb.useDelimiter(System.getProperty("line.separator"));
		
		//Creamos los objetos iniciales que usaremos durante el juego
		Tablero partida = new Tablero();
		Config con = new Config();
		
		//Variables para trabajar con los menús
		byte opcion;
		boolean correcto = false, salir = false;

		//Primer bucle para las opciones iniciales del programa
		do{
			opcion = menu_inicial();

			switch(opcion){
			case 1: 
				//Se crea un tablero con las piezas en sus posiciones iniciales
				Tablero.tablero_inicial(partida);
				correcto = true;
			break;

			case 2:
				//Se carga una partida desde el archivo enviado por ags[0]
				if((partida = cargar_tablero(partida, args[0])) != null){
					System.out.println("Se ha cargado el tablero correctamente");
					kb.nextLine();
					System.out.println("\nPulse enter para empezar.");
					
					correcto = true;
				}else
					System.out.println("Hubo un problema cargando el tablero");

				kb.nextLine();
			break;

			case 3:
				//Se carga una configuración visual desde el archivo enviado por args[1]
				if((con = Config.carga(con, args[1])) != null){
					System.out.println("Se ha cargado la configuración correctamente");
					kb.nextLine();

				}else
					System.out.println("Hubo un problema cargando la configuración");
			
				kb.nextLine();
			break;

			case 4:
				//Se crea una nueva configuración visual personalizada
				Config.creaConfig(con, args[1]);
			break;

			case 5:
				correcto = true;
				salir = true;
			break;

			default:
				System.out.println("La opción introducida no ha sido válida ...");
				kb.nextLine();
			break;
			}

		}while(!correcto);
		
		//Si no se ha establecido una configuración previa, se pone la default
		if (con == null) con = new Config();
		if(con.nombre == "") con = Config.cDefault(con);

		String jugada;
		
		//Flujo principal del juego
		try{
			//Se ejecuta siempre que no se quiera salir y no haya ningún mate
			while(!salir && (!partida.piezas[4].mate || !partida.piezas[28].mate)){
				try{

					if(!salir) limpiar_pantalla();
					
					//Se muestra el tablero y si se quiere, se puede descomentar la segunda linea para ver las posiciones de las piezas
					if(!salir) Tablero.mostrar_matriz(partida.tablero, con);
//					Tablero.mostrar_piezas_prueba(partida.piezas);
					
					//Se van contando los movimientos para saber si es el turno de las blancas o de las negras
					partida.movimiento++;
					
					System.out.println("\t\t(Introduce \"opciones\" para otras acciones)");
					System.out.println("\t\t(Introduce \"mate\" si has perdido o te quieres rendir)\n");

					if(partida.movimiento % 2 != 0) System.out.println("\t\tTURNO DE LAS BLANCAS");
					else                            System.out.println("\t\tTURNO DE LAS NEGRAS");

					System.out.print("\n\t\tIntroduce una jugada: ");
					jugada = kb.nextLine();
					
					//Si se introduce opciones, se abre el menú de guardado y salida, si se introduce mate, se considera perdido para ese color, en otro caso, se toma como movimiento
					if(jugada.equalsIgnoreCase("opciones")){
						partida.movimiento--;

						limpiar_pantalla();
						salir = menu_opciones(partida, args[0]);
					
					}else if(jugada.equalsIgnoreCase("mate")){
						if(partida.movimiento % 2 != 0) partida.piezas[4].mate = true;
						else partida.piezas[28].mate = true;
						salir = true;
					
					}else if (!salir)	
						if(!nuevo_movimiento(partida, partida.movimiento, jugada)){
							kb.nextLine();
							partida.movimiento--;
						}
				
				//Captura del error por dar una posición fuera del tablero
				}catch(ArrayIndexOutOfBoundsException e){
					System.out.println("posición especificada fuera del tablero ...");
					kb.nextLine();
				}
			}
		//Captura si algo apunta a una zona nula
		}catch(NullPointerException e){
		}

		if(partida.piezas[4].mate) System.out.println("\n\n\t\t\tENHORABUENA A LAS NEGRAS, HABÉIS GANADO");
		if(partida.piezas[28].mate)System.out.println("\n\n\t\t\tENHORABUENA A LAS BLANCAS, HABÉIS GANADO");

		kb.close();
		System.out.println("\n\nSe ha salido del programa con éxito\n\n");
	}

	/**Menú inicial. Devuelve byte para saber la opción elegida*/
	static byte menu_inicial(){

		Ajedrez.limpiar_pantalla();
		
		System.out.println("\t\t\t===================================================================================================");
		System.out.println("\t\t\t                                                                                                   ");
		System.out.println("\t\t\t              _                                                             _                      ");
		System.out.println("\t\t\t            _| |_                                                         _| |_                    ");
		System.out.println("\t\t\t           |_   _|             BIENVENIDO AL AJEDREZ DE ALBERTO          |_   _|                   ");
		System.out.println("\t\t\t           __| |__            ==================================         __| |__                   ");
		System.out.println("\t\t\t          (_______)                                                     (_______)                  ");
		System.out.println("\t\t\t          /_______\\           1. Iniciar una partida nueva              /_______\\                   ");
		System.out.println("\t\t\t          \\       /           2. Cargar una partida de un archivo       \\       /                  ");
		System.out.println("\t\t\t           |     |            3. Cargar configuración de archivo         |     |                   ");
		System.out.println("\t\t\t           |     |            4. Nueva Configuración visual              |     |                   ");
		System.out.println("\t\t\t           |     |            5. Salir del programa                      |     |                   ");
		System.out.println("\t\t\t          /       \\                                                     /       \\                  ");
		System.out.println("\t\t\t         (_________)                                                   (_________)                 ");
		System.out.println("\t\t\t         |_________|           (Si no se toca la configuración,        |_________|                 ");
		System.out.println("\t\t\t         /_________\\           se cargará la predeterminada)           /_________\\                 ");
		System.out.println("\t\t\t        (___________)                                                 (___________)                  ");
		System.out.println("\t\t\t                                                                                                   ");
		System.out.println("\t\t\t                                                                                                   ");
		System.out.println("\t\t\t===================================================================================================");
		System.out.println();
		System.out.print("\t\t\tIntroduce el número de la acción que desea realizar: ");
		byte opcion = kb.nextByte();
		kb.nextLine();

		return opcion;
	}

	/**Menú de opciones de una partida empezada, recibe un Tablero y la ruta de partidas, devuelve boolean*/
	static boolean menu_opciones(Tablero partida, String archivo){
		System.out.println("\n\n\n");
		System.out.println("\t\t\t===================================================================================================");
		System.out.println("\t\t\t                                                                                                   ");
		System.out.println("\t\t\t                   _                                                   _                           ");
		System.out.println("\t\t\t                 _| |_                                               _| |_                         ");
		System.out.println("\t\t\t                |_   _|             OPCIONES DE LA PARTIDA          |_   _|                        ");
		System.out.println("\t\t\t                __| |__            ========================         __| |__                        ");
		System.out.println("\t\t\t               (_______)                                           (_______)                       ");
		System.out.println("\t\t\t               /_______\\                                           /_______\\                        ");
		System.out.println("\t\t\t               \\       /                                           \\       /                       ");
		System.out.println("\t\t\t                |     |            1. Salir sin guardar             |     |                        ");
		System.out.println("\t\t\t                |     |            2. Guardar y salir               |     |                        ");
		System.out.println("\t\t\t                |     |            3. Cerrar menú y seguir          |     |                        ");
		System.out.println("\t\t\t               /       \\                                           /       \\                       ");
		System.out.println("\t\t\t              (_________)                                         (_________)                      ");
		System.out.println("\t\t\t              |_________|                                         |_________|                      ");
		System.out.println("\t\t\t              /_________\\                                         /_________\\                      ");
		System.out.println("\t\t\t             (___________)                                       (___________)                       ");
		System.out.println("\t\t\t                                                                                                   ");
		System.out.println("\t\t\t                                                                                                   ");
		System.out.println("\t\t\t===================================================================================================");
		System.out.println();
		System.out.print("\t\t\tIntroduce el número de la acción que desea realizar: ");
		byte opcion = kb.nextByte();
		kb.nextLine();

		boolean devolver = false;
		
		//Switch para elegir en función de la posición dada
		switch(opcion){
		case 1:
			//Se sale del programa directamente
			devolver = true;
		break;

		case 2:
			//Se envía la partida y el archivo a guardaEstado para almacenarlo en el fichero
			limpiar_pantalla();
			if(guardaEstado(partida, archivo))
				System.out.println("La partida se ha guardado correctamente ...");
			else
				System.out.println("Hubo un problema durante el guardado, se va a salir del programa ...");

			kb.nextLine();
			devolver = true;
		break;
		
		case 3:
			//No se hace nada, se vuelve a la partida
		break;
		
		default:
			//Se avisa de que no es válido y se vuelve a mostrar el menú de forma recursiva
			System.out.println("Opción introducida no válida ...");
			kb.nextLine();
			devolver = menu_opciones(partida, archivo);

		break;
		}

		return devolver;
	}


	static boolean nuevo_movimiento(Tablero partida, int color, String jugada){
		
		if(jugada.length() < 2 || jugada.length() > 5) return false;
		
		boolean valido = true;
		
		//Establecemos las ultimas dos posiciones como las coordenadas a las que se quiere ir, ya sea moviendo o comiendo
		partida.nuevaX = (int)(jugada.charAt(jugada.length()-2)-97);
		partida.nuevaY = (int)(jugada.charAt(jugada.length()-1)-49);
		
		//Hacemos un switch que gestionará la jugada en función del tipo introducido
		switch(jugada.length()){
			
		case 2: //Si es de 2 letras, será unicamente un peón, comprobamos que la sintaxis es correcta y lo enviamos a movimientoPeon
			if(Character.isLowerCase(jugada.charAt(0)) && Character.isDigit(jugada.charAt(1))) {
				
				if(!Pieza.movimientoPeon(partida, color))
				valido = false;
		
			} else{
				valido = false;
			}				
			break;
		
		case 3: //Si es de 3 letras, será unicamente una pieza normal moviendose, comprobamos su sintaxis y lo enviamos a selecciona_pieza para ejecute la correspondiente
			if(Character.isUpperCase(jugada.charAt(0))
			&& Character.isLowerCase(jugada.charAt(1))
			&& Character.isDigit(jugada.charAt(2))) 
				
				valido = selecciona_pieza(partida, color, jugada.charAt(0), true);
			
			else
				valido = false;
			break;
			
		case 4: // hay 3 opciones, en cualquiera de ellos comprobamos la sintaxis:
			//Pieza normal comiendo, EJ: Txa8, se envía a selecciona_pieza
			if(Character.isUpperCase(jugada.charAt(0))
			&& Character.toLowerCase(jugada.charAt(1)) == 'x'){
						
				partida.comer = true;
				valido = selecciona_pieza(partida, color, jugada.charAt(0), true);
				partida.comer = false;

			//Pieza normal pero con 2 opciones posibles, moviendose a otras casilla EJ Tab8   ||   T3c3
			//Se utiliza un método específico para saber que pieza en especial se va a comer, y se envía a selecciona_pieza
			}else if(Character.isUpperCase(jugada.charAt(0))
			&& Character.toLowerCase(jugada.charAt(1)) != 'x'){
					
				partida.pieza_específica = encuentra_pieza(partida, jugada.charAt(0), jugada.charAt(1), color);
				valido = selecciona_pieza(partida, color, jugada.charAt(0), true);
				partida.pieza_específica = -1;
			
			//Peon comiendo: EJ cxd4
			}else if(Character.isLowerCase(jugada.charAt(0))
			&& Character.toLowerCase(jugada.charAt(1)) == 'x'){
					
				partida.pieza_específica = jugada.charAt(0);
				partida.comer = true;

				valido = Pieza.comerDePeon(partida, color, true);

				partida.comer = false;
				partida.pieza_específica = -1;

			}else
				valido = false;
			
			break;
			
		case 5: //Solo puede usar una pieza específica comiendo, se marca que es una en especial y que se quiere comer y se envía a selecciona_pieza
			//EJ Taxh8
			if(Character.isUpperCase(jugada.charAt(0))
			&& Character.toLowerCase(jugada.charAt(2)) == 'x'){

				partida.pieza_específica = encuentra_pieza(partida, jugada.charAt(0), jugada.charAt(1), color);
				partida.comer = true;
				valido = selecciona_pieza(partida, color, jugada.charAt(0), true);
				partida.comer = false;
				partida.pieza_específica = -1;
			
			}else 
				valido = false;
			
			break;
			
		default:
			valido = false;
			break;
		}
		
		//Si cualquiera de los métodos superiores es erroneo, se devuelve valido = false y se avisa que la jugada no es válida
		if(!valido){
			System.err.println("Jugada no válida ... ");
			return false;
		}

		System.out.println("\n\n");	
		return true;
	}

	/**Método asociado a cualquier movimiento de una pieza no peón, devuelve boolean y recibe "tablero", color en el que esta, pieza que se quiere mover y boolean avisando si se va a mover o solo a comprobar*/
	static boolean selecciona_pieza(Tablero partida, int color, char pieza, boolean mover){
		//Redirije el movimiento al método específico de la pieza que toque
		boolean valido = true;

		switch(pieza) {
		case 'T':
			if(!Pieza.movimientoTorre(partida, color, mover))
				valido = false;
		break;
		
		case 'A':
		if(!Pieza.movimientoAlfil(partida, color, mover))
			valido = false;
		break;

		case 'D':
			if(!Pieza.movimientoDama(partida, color, mover))
				valido = false;
		break;

		case 'C':
			if(!Pieza.movimientoCaballo(partida, color, mover))
				valido = false;
		break;
		
		case 'R':
			if(!Pieza.movimientoRey(partida, color, mover))
				valido = false;
		break;
		
		default:
			System.out.println("Pieza no válida ...");
			break;
		}
		return valido;
	}

	/**Método que elige y almacena el índice de la pieza específica si fuese necesario, recibe la partida, tipo de pieza, posición específica de esta, y el color en el que se está*/
	static int encuentra_pieza(Tablero partida, char tipo, char posicion, int color){

		boolean escolumna;
		int zona;
		
		//Se marcan unos parámetros para saber en que parte del vector de piezas hay que hacer las comprobaciones
		if(color % 2 != 0)
			zona = 0;
		
		else
			zona = 16;


		//Seleccionamos si la fila/columna específica, es una fila o una columna
		if(Character.isDigit(posicion)) 
			escolumna = false;
		
		else if (Character.isLetter(posicion) && Character.isLowerCase(posicion)) 
			escolumna = true;

		else
			return -1;

		//Hacemos las comprobaciones con las piezas con posibles posibilidades (piezas dobles no peones)
		if(escolumna){
			for(int x = 0+zona; x < 16+zona; x++){
				if(x == 3 || x == 4 || (x >=8 && x<=23) || x == 27 || x == 28) continue;

				if(partida.piezas[x].posicionX == (int)(posicion - 97) && partida.piezas[x].nombre.charAt(0) == tipo)
					return x;
			}
		
		}else{
			for(int x = 0+zona; x < 16+zona; x++){
				if(x == 3 || x == 4 || (x >=8 && x<=23) || x == 27 || x == 28) continue;

				if(partida.piezas[x].posicionY == (int)(posicion - 49) && partida.piezas[x].nombre.charAt(0) == tipo)
					return x;
			}
		}
		System.out.println();
		//Si no se ha encontrado, se duelve -1 para marcarlo, pues no es un índice posible
		return -1;
	}

	/**Método para leer partidas almacenadas en el archivo pasado por args[0], devuelve un objeto de la clase Tablero con toda la información*/
	static Tablero cargar_tablero(Tablero partida, String archivo){
		limpiar_pantalla();
		
		int cont = 1;
		boolean valido = true;
		ObjectInputStream ois = null;
		Tablero temporal = null;
		File ruta = new File(archivo);
		
		if(ruta.length() == 0){
			System.out.println("No hay partidas guardadas");
			return partida = null;
		}
			try {
				//Mostramos todas las partidas guardadas para que el usuario sepa cual elegir y cuales hay
				System.out.println("PARTIDAS GUARDADAS:");
				System.out.println("====================================");
				ois = new ObjectInputStream(new FileInputStream(ruta));
				
				while((temporal = (Tablero)ois.readObject()) != null)		
					System.out.println("\t"+(cont++) +". "+temporal.nombre);	
				
			} catch (EOFException e) {
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
				valido = false;
						
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				valido = false;
				
			} catch (IOException e) {
				e.printStackTrace();
				valido = false;
				
			}
		
			System.out.print("\n\nIntroduce el número de la partida que deseas cargar: ");
			int posicion = kb.nextInt();
			
			cont = 1;
			boolean seguir = true;

			try {
				ois = new ObjectInputStream(new FileInputStream(ruta));
				
				//Vamos buscando entre los objetos hasta llegar al que conincide con el índice pedido
				while(seguir && ((temporal = (Tablero)ois.readObject()) != null)){
					//Cargamos los objetos de las piezas que van detrás de cada tablero
					
					Tablero.mostrar_piezas_prueba(temporal.piezas);
					
					for (int i = 0; i < temporal.piezas.length; i++) 
						if(i == 4 || i == 28)
							System.out.println(temporal.piezas[i].mate);
					
					
					if(cont == posicion){
						//Cuando coincide, lo almacenamos, salimos, y devolvemos el objeto al curso principal del juego
						partida = temporal;
//						partida.tablero= Tablero.reajustar_tablero(partida);
						seguir = false;
					}
					cont++;
				}
	
			} catch (EOFException e) {
			} catch (ClassCastException e){
				System.out.println("Partida no encontrada");
				valido = false;

			} catch (ClassNotFoundException e) {
				valido = false;
						
			} catch (FileNotFoundException e) {
				System.out.println("No se encontró el archivo");
				valido = false;
				
			} catch (IOException e) {
				e.printStackTrace();
				valido = false;
				
			}
			finally {
				try {
					ois.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
				if(!valido)
					partida = null;
			}

		return partida;
	}

	/**Método que recibe la partida y archivo de partidas pasado por args[0], almacena tanto el objeto Tablero como los objetos Pieza de la partida que está siendo jugada*/
	static boolean guardaEstado(Tablero partida, String archivo){
		
		System.out.println("Nombre de la partida: ");
		partida.nombre = kb.nextLine();

		File ruta = new File(archivo);
		
		if(ruta.exists())
			try {
				ruta.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}

		ObjectOutputStream oos = null;
		MiObjectOutputStream moos = null;
		boolean valido = true;
		
		if(ruta.length() == 0) { 
			try {
				System.out.println("\nCon cabecera\n");
				oos = new ObjectOutputStream(new FileOutputStream(ruta));
				oos.writeObject(partida);
				
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				valido = false;
			} catch (IOException e) {
				e.printStackTrace();
				valido = false;
			
			}finally {
				try {
					oos.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}else {
			
			try {
				moos = new MiObjectOutputStream(new FileOutputStream(ruta, true));
				moos.writeObject(partida);
		
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				valido = false;
				
			} catch (IOException e) {
				e.printStackTrace();
				valido = false;
			}
		}

/*		try{
			//A continuación del tablero, se almacenan los 32 objetos de las piezas de la partida
			for(int x = 0; x<32; x++){
				moos = new MiObjectOutputStream(new FileOutputStream(ruta, true));
				moos.writeObject(partida.piezas[x]);
			}

		} catch (FileNotFoundException e) {
			e.printStackTrace();
			valido = false;
			
		} catch (IOException e) {
			e.printStackTrace();
			valido = false;
		}
		finally {
			try {
				moos.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
*/
		if(!valido) return false;

		return true;
	}

	/**Método para simular que se limpia la pantalla*/
	static void limpiar_pantalla(){
		for (int i = 0; i < LINEAS; i++) {
			System.out.println();
		}
	}
}