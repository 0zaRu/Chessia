import java.io.Serializable;

/**Clase para establecer los atributos de todas las piezas de la partida, contiene los métodos de movimiento de estas*/

class Pieza implements Serializable{

	private static final long serialVersionUID = 03042153;

	String nombre="";
	boolean vivo = true;
	boolean color;
	boolean mate;

	int posicionX;
	int posicionY; 

	/**Método específico para el movimiento del peón, recibe el tablero y color para saber cuál mover*/
	static boolean movimientoPeon(Tablero partida, int color){	
		//Se comprueba que la casilla a la que se quiere ir está vacía, porque sino, no se puede ir ahí
		if(!partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		if(color % 2 != 0)
			//Bucle para evaluar todos los peones blancos
			for (int i = 8; i <= 15; i++) {
				//Si un peón coincide, se envía su índice a efectuar movimiento
				if(partida.nuevaX == (partida.piezas[i].posicionX) && partida.nuevaY-1 == partida.piezas[i].posicionY) {
					Tablero.efectuar_movimiento(partida, i, color);
					return true;
				}
				//Con este se comprueba el movimiento de 2 casillas. Si un peón coincide, se envía su índice a efectuar movimiento				
				if(partida.nuevaX == partida.piezas[i].posicionX 
						&& (partida.nuevaY-2 == partida.piezas[i].posicionY && partida.nuevaY-2 == 1) 
						&& partida.tablero[partida.nuevaY-1][partida.nuevaX].isBlank()){
					
					Tablero.efectuar_movimiento(partida, i, color);
					return true;
				}
				//Si ninguno ha coincidido, se devuelve false
				if(i == 16) return false;			
			}
		else
			//Bucle para evaluar todos los peones negros
			for (int i = 16; i <= 23; i++) {
				//Si un peón coincide, se envía su índice a efectuar movimiento
				if(partida.nuevaX == (partida.piezas[i].posicionX) && partida.nuevaY+1 == partida.piezas[i].posicionY) {
					Tablero.efectuar_movimiento(partida, i, color);
					return true;
				}
				//Con este se comprueba el movimiento de 2 casillas. Si un peón coincide, se envía su índice a efectuar movimiento
				if(partida.nuevaX == partida.piezas[i].posicionX
						&& (partida.nuevaY+2 == partida.piezas[i].posicionY && partida.nuevaY+2 == 6)
						&& partida.tablero[partida.nuevaY+1][partida.nuevaX].isBlank()){
					
					Tablero.efectuar_movimiento(partida, i, color);
					return true;
				}
				//Si ninguno ha coincidio se sale y devuelve false
				if(i == 23) return false;			
			}
		return false;
	}

	/**Método específico para la captura de los peones, recibe el tablero, el color, y un boolean para saber si se quiere mover de verdad o solo comprobar*/
	static boolean comerDePeon(Tablero partida, int color, boolean mover){
		//Si no hay una pieza a donde se quiere ir, se devuelve false
		if(partida.comer && partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		boolean valido = false;
		int pieza = -1;

		//Bucles para comprobar si alguno de los peones puede capturar, se guarda el índice de el que sí
		if(color % 2 != 0){
			for(int x = 8; x < 16; x++)
				if(partida.piezas[x].posicionY == partida.nuevaY-1 && partida.piezas[x].posicionX == partida.pieza_específica-97){
					valido = true;
					pieza = x;
				}

		}else{
			for(int x = 16; x < 24; x++)
				if(partida.piezas[x].posicionY == partida.nuevaY+1 && partida.piezas[x].posicionX == partida.pieza_específica-97){
					valido = true;
					pieza = x;
				}
		}
		
		//Si se ha encontrado un peón válido y se quiere efectuar el movimiento, se hace
		if(valido && mover)
			Tablero.efectuar_movimiento(partida, pieza, color);
	
		return valido;
	}

	/**Método para el movimiento y captura de las torres, recibe el tablero, el color, y un boolean para saber si se quiere mover de verdad o solo comprobar*/
	static boolean movimientoTorre(Tablero partida, int color, boolean mover){	
		//Se comprueba que la casilla está vacía si se quiere mover, y que contiene una pieza si se quiere comer
		
		if(!partida.comer && !partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		if(partida.comer && partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		
		boolean valido0 = false, valido7 = false, valido24 = false, valido31 = false;
		int pieza = -1;
		
		//Se comprueba con el método comprobar_fila_columna si alguna de las torres vivas puede ir hasta la casilla a la que se quiere
		if(color % 2 != 0) {
			if(partida.piezas[0].vivo) valido0  = comprobar_fila_columnas(partida, 0);
			if(partida.piezas[7].vivo) valido7  = comprobar_fila_columnas(partida, 7);
			
			//Si es una pieza específica, se guardará su índice, pero para que esta sintaxis sea correcta, las 2 piezas deben de ser válidas
			if(valido0 && valido7)
				if(partida.pieza_específica != -1)
					pieza = partida.pieza_específica;

				else
					return false;
	
			if(partida.pieza_específica == -1){
				if(valido0) pieza = 0;
				if(valido7) pieza = 7;
			}
				
		}else {
			if(partida.piezas[24].vivo) valido24 = comprobar_fila_columnas(partida, 24);
			if(partida.piezas[31].vivo) valido31 = comprobar_fila_columnas(partida, 31);
			
			if(valido24 && valido31)
				if(partida.pieza_específica != -1)
					pieza = partida.pieza_específica;

				else
					return false;
	
			if(partida.pieza_específica == -1){
				if(valido24) pieza = 24;
				if(valido31) pieza = 31;
			}
		}
		
		boolean devolver = false;

		if(pieza != -1) devolver = true;
		
		//Si se ha encontrado una pieza y se quiere mover, se envía a efectuar_movimiento
		if(mover && devolver){
			devolver = Tablero.efectuar_movimiento(partida, pieza, color);
		}
		return devolver;
	}
	
	/**Método para el movimiento y captura de los alfiles, recibe el tablero, el color, y un boolean para saber si se quiere mover de verdad o solo comprobar*/
	static boolean movimientoAlfil(Tablero partida, int color, boolean mover){
		
		//Se comprueba que la casilla está vacía si se quiere mover, y que contiene una pieza si se quiere comer
		if(!partida.comer && !partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		if(partida.comer && partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		boolean valido2 = false, valido5 = false, valido26 = false, valido29 = false;
		int pieza = -1;
		
		//Se comprueba con el método comprobar_diagonal si alguno de los alfiles vivos puede ir hasta la casilla a la que se quiere
		if(color % 2 != 0) {
			if(partida.piezas[2].vivo) valido2  = comprobar_diagonal(partida, 2);
			if(partida.piezas[5].vivo) valido5  = comprobar_diagonal(partida, 5);
			
			//Si es una pieza específica, se guardará su índice, pero para que esta sintaxis sea correcta, las 2 piezas deben de ser válidas
			if(valido2 && valido5)
				if(partida.pieza_específica != -1)
					pieza = partida.pieza_específica;

			else
				return false;

			if(partida.pieza_específica == -1){
				if(valido2) pieza = 2;
				if(valido5) pieza = 5;
			}
		
		}else {
			if(partida.piezas[26].vivo) valido26 = comprobar_diagonal(partida, 26);
			if(partida.piezas[29].vivo) valido29 = comprobar_diagonal(partida, 29);
			
			if(valido26 && valido29)
				if(partida.pieza_específica != -1)
					pieza = partida.pieza_específica;

				else
					return false;
	
			if(partida.pieza_específica == -1){
				if(valido26) pieza = 26;
				if(valido29) pieza = 29;
			}
		}
		
		boolean devolver = false;

		if(pieza != -1) devolver = true;

		if(mover && devolver){
			devolver = Tablero.efectuar_movimiento(partida, pieza, color);
		}
		return devolver;
	}

	/**Método para el movimiento y captura de los caballos, recibe el tablero, el color, y un boolean para saber si se quiere mover de verdad o solo comprobar*/
	static boolean movimientoCaballo(Tablero partida, int color, boolean mover){

		//Se comprueba que la casilla está vacía si se quiere mover, y que contiene una pieza si se quiere comer
		if(!partida.comer && !partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		if(partida.comer && partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		boolean valido1 = false, valido6 = false, valido25 = false, valido30 = false;
		int pieza = -1;
		
		//Se comprueba con el método comprobar_salto si alguno de los caballos vivos puede ir hasta la casilla a la que se quiere
		if(color % 2 != 0) {
			if(partida.piezas[1].vivo) valido1 = comprobar_salto(partida, 1);
			if(partida.piezas[6].vivo) valido6 = comprobar_salto(partida, 6);

			//Si es una pieza específica, se guardará su índice, pero para que esta sintaxis sea correcta, las 2 piezas deben de ser válidas
			if(valido1 && valido6)
				if(partida.pieza_específica != -1){
					pieza = partida.pieza_específica;

				}else
					return false;
	
			if(partida.pieza_específica == -1){
				if(valido1) pieza = 1;
				if(valido6) pieza = 6;
			}
		
		}else {
			if(partida.piezas[25].vivo) valido25 = comprobar_salto(partida, 25);
			if(partida.piezas[30].vivo) valido30 = comprobar_salto(partida, 30);

			if(valido25 && valido30)
				if(partida.pieza_específica != -1){
					pieza = partida.pieza_específica;

				}else
					return false;
	
			if(partida.pieza_específica == -1){
				if(valido25) pieza = 25;
				if(valido30) pieza = 30;
			}
		}
		
		boolean devolver = false;

		if(pieza != -1){
			devolver = true;
		}

		if(mover && devolver){
			devolver = Tablero.efectuar_movimiento(partida, pieza, color);
		}

		return devolver;
	}

	/**Método para el movimiento y captura de las damas, recibe el tablero, el color, y un boolean para saber si se quiere mover de verdad o solo comprobar*/
	static boolean movimientoDama(Tablero partida, int color, boolean mover){	

		//Se comprueba que la casilla está vacía si se quiere mover, y que contiene una pieza si se quiere comer
		if(!partida.comer && !partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		if(partida.comer && partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		boolean valido3 = false, valido27 = false;
		int pieza = -1;
		
		//Se comprueba con el método comprobar_fila_columna y comprobar_diagonal si alguna de las damas puede ir hasta la casilla a la que se quiere
		if(color % 2 != 0) {
			if(partida.piezas[3].vivo) if(comprobar_fila_columnas(partida, 3) || comprobar_diagonal(partida, 3))
				valido3 = true;

			if(valido3) pieza = 3;
			else return false;
		
		}else {
			if(partida.piezas[27].vivo) if(comprobar_fila_columnas(partida, 27) || comprobar_diagonal(partida, 27))
				valido27 = true;

			if(valido27) pieza = 27;
			else return false;
		}
		
		boolean devolver = true;;

		if(mover){
			devolver = Tablero.efectuar_movimiento(partida, pieza, color);
		}
		return devolver;
	}

	/**Método para comprobar que la casillas entre la pieza pasada y la nueva posición están vacías*/
	static boolean comprobar_fila_columnas(Tablero partida, int pieza) {
		
		//Asigno los datos a variables locales para facilitar la visualización de las operaciones
		Pieza piezas[] = partida.piezas;
		int nuevaX     = partida.nuevaX;
		int nuevaY     = partida.nuevaY;
		
		//Comprobamos que coincide en la fila o la columna para que sea válido
		if(piezas[pieza].posicionX != nuevaX && piezas[pieza].posicionY != nuevaY)
			return false;
		
		//Si coinciden en la columna, comprobamos si el trayecto desde la pieza hasta la casilla está vacío
		if(piezas[pieza].posicionX == nuevaX) {
			
			if(Math.abs(nuevaY-piezas[pieza].posicionY) == 1)
				return true;
			
			//Comprobamos cuando está por debajo de la nueva casilla y a más de 1 de distancia
			if(piezas[pieza].posicionY < nuevaY) {
				for(int i = piezas[pieza].posicionY+1; i < nuevaY; i++) {
					if(!partida.tablero[i][nuevaX].isBlank()) return false;
				}
			
			//comprobamos cuano está por encima de la casilla
			}else if(piezas[pieza].posicionY > nuevaY) {
				for(int i = nuevaY+1; i < piezas[pieza].posicionY; i++) {
					if(!partida.tablero[i][nuevaX].isBlank()) return false;
				}
			
			//Por si acaso se hubiese saltado algun paso (en principio nunca pasará por aquí)
			}else return false;
		}
		
		//Si coincide en la fila, se comprueba por arriba y por abajo
		if(piezas[pieza].posicionY == nuevaY) {
			
			if(Math.abs(nuevaX-piezas[pieza].posicionX) == 1)
				return true;
			
			//Comprobamos cuando está por la izquierda
			if(piezas[pieza].posicionX < nuevaX) {
				for(int i = piezas[pieza].posicionX+1; i < nuevaX; i++) {
					if(!partida.tablero[nuevaY][i].isBlank()) return false;				
				}
			
			//Comprobamos cuando está por la derecha
			}else if(piezas[pieza].posicionX > nuevaX) {
				for(int i = nuevaX+1; i < piezas[pieza].posicionX; i++) {
					if(!partida.tablero[nuevaY][i].isBlank()) return false;
				}
				
			//en principio nunca pasaremos por aquí
			}else
				return false;
		}
		return true;
	}

	/**Método para comprobar que las casillas entre la pieza pasada y la nueva posición están despejadas*/
	static boolean comprobar_diagonal(Tablero partida, int pieza) {
		
		Pieza piezas[] = partida.piezas;
		int nuevaX     = partida.nuevaX;
		int nuevaY     = partida.nuevaY;

		if(Math.abs(piezas[pieza].posicionX - nuevaX) != Math.abs(piezas[pieza].posicionY - nuevaY))
			return false;
		
		//Alfil a la izquierda de la nueva posición
		if(piezas[pieza].posicionX < nuevaX) {
			//Alfil por debajo
			if(piezas[pieza].posicionY < nuevaY && Math.abs(nuevaY-piezas[pieza].posicionY) != 1) {
				for(int i = piezas[pieza].posicionY+1, j = piezas[pieza].posicionX+1; i < nuevaY; i++, j++) {
					if(!partida.tablero[i][j].isBlank()) return false;
				}
			}

			//Alfil por encima
			if(piezas[pieza].posicionY > nuevaY && Math.abs(nuevaY-piezas[pieza].posicionY) != 1){
				for(int i = piezas[pieza].posicionY-1, j = piezas[pieza].posicionX+1; nuevaY < i; i--, j++) {
					if(!partida.tablero[i][j].isBlank()) return false;
				}
			}
				
		}
		
		
		//Alfil a la derecha de la nueva posición
		if(piezas[pieza].posicionX > nuevaX) {
			//Alfil por debajo
			if(piezas[pieza].posicionY < nuevaY && Math.abs(nuevaY-piezas[pieza].posicionY) != 1) {
				for(int i = piezas[pieza].posicionY+1, j = piezas[pieza].posicionX-1; i < nuevaY; i++, j--) {
					if(!partida.tablero[i][j].isBlank()) return false;
				}
			}

			//Alfil por encima
			if(piezas[pieza].posicionY > nuevaY && Math.abs(nuevaY-piezas[pieza].posicionY) != 1) {
				for(int i = piezas[pieza].posicionY-1, j = piezas[pieza].posicionX-1; nuevaY < i; i--, j--) {
					if(!partida.tablero[i][j].isBlank()) return false;
				}
			}
		}
		return true;
	}

	/**Método (algo cutre) para comprobar los saltos del caballo*/
	static boolean comprobar_salto(Tablero partida, int pieza){
		
		Pieza piezas[] = partida.piezas;
		int nuevaX     = partida.nuevaX;
		int nuevaY     = partida.nuevaY;

		if(nuevaX+1 == piezas[pieza].posicionX && nuevaY+2 == piezas[pieza].posicionY)
			return true;
			
		if(nuevaX+2 == piezas[pieza].posicionX && nuevaY+1 == piezas[pieza].posicionY)
			return true;

		if(nuevaX+2 == piezas[pieza].posicionX && nuevaY-1 == piezas[pieza].posicionY)
			return true;

		if(nuevaX+1 == piezas[pieza].posicionX && nuevaY-2 == piezas[pieza].posicionY)
			return true;
		
		if(nuevaX-1 == piezas[pieza].posicionX && nuevaY-2 == piezas[pieza].posicionY)
			return true;

		if(nuevaX-2 == piezas[pieza].posicionX && nuevaY-1 == piezas[pieza].posicionY)
			return true;

		if(nuevaX-2 == piezas[pieza].posicionX && nuevaY+1 == piezas[pieza].posicionY)
			return true;

		if(nuevaX-1 == piezas[pieza].posicionX && nuevaY+2 == piezas[pieza].posicionY)
			return true;

		return false;
	}

	/**Método para compronar el movimiento del rey*/
	static boolean movimientoRey(Tablero partida, int color, boolean mover){	
		
		//Se comprueba que la casilla a la que se quiere ir está vacía en caso de movimiento, y rellena en caso de captura
		if(!partida.comer && !partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		if(partida.comer && partida.tablero[partida.nuevaY][partida.nuevaX].isBlank())
			return false;

		boolean valido4 = false, valido28 = false;
		int pieza = -1;
		
		//Se comprueba si, estando a 1 casilla de diferente de forma absoluta, el rey podría ir hasta allí
		if(color % 2 != 0) {
			if(Math.abs(partida.piezas[4].posicionX - partida.nuevaX) <= 1 && Math.abs(partida.piezas[4].posicionY - partida.nuevaY) <= 1)
				if(mover) valido4 = comprobar_movimiento_Rey(partida, color, 4);
				else valido4 = true;

			if(valido4) pieza = 4;
			else return false;
		
		}else {
			if(Math.abs(partida.piezas[28].posicionX - partida.nuevaX) <= 1 && Math.abs(partida.piezas[28].posicionY - partida.nuevaY) <= 1)
				if(mover) valido28 = comprobar_movimiento_Rey(partida, color, 28);
				else valido28 = true;

			if(valido28) pieza = 28;
			else return false;
		}
		
		boolean devolver = true;
		if(mover) devolver = Tablero.efectuar_movimiento(partida, pieza, color);
	
		return devolver;
	}

	/**Método para hacer las comprobaciones de movimiento del rey, tanto si llega como si hay otra pieza amenazando a esa posición*/
	static boolean comprobar_movimiento_Rey(Tablero partida, int color, int pieza){

		int zona, cambioColor = 0, rey;
		String saveRey;

		//Se establecen las zonas de comprobación en función de si se mueve el rey u otra pieza para saber a qué color comprobar
		//No implementado comprobación por parte de otras piezas diferentes al rey, aunque este if else si que lo compruebe y defina
		if(color % 2 != 0){
			if(pieza == 4){
				cambioColor++;
				zona = 16;
				rey = 4;
			
			}else{
				zona = 0;
				rey = 28;
			}

		}else{
			if(pieza == 28){
				cambioColor++;
				zona = 0;
				rey = 28;
			
			}else{
				zona = 16;
				rey = 4;
			}
		}
		//Se elimina al rey del tablero a la hora de las comprobocaciones porque si quiere ir a una casilla amenazada, se tapa a sí mismo y se permitiría el movimiento
		saveRey = partida.tablero[partida.piezas[rey].posicionY][partida.piezas[rey].posicionX];
		partida.tablero[partida.piezas[rey].posicionY][partida.piezas[rey].posicionX] = " ";

		if((pieza != 4 && color % 2 != 0) || (pieza != 28 && color % 2 == 0)){ 
			partida.nuevaX = partida.piezas[rey].posicionX;
			partida.nuevaY = partida.piezas[rey].posicionY;
		}

		if(partida.comer) return true;

		for(int x = 0+zona; x < 16+zona; x++){
			if(x >= 8 && x <= 23)
				comerDePeon(partida, color+cambioColor, false);
			
			else if(Ajedrez.selecciona_pieza(partida, color+cambioColor, partida.piezas[x].nombre.charAt(0), false)){
				System.out.println("Jaque");
				partida.tablero[partida.piezas[rey].posicionY][partida.piezas[rey].posicionX] = saveRey;

				return false;
			}
		}
		partida.tablero[partida.piezas[rey].posicionY][partida.piezas[rey].posicionX] = saveRey;

		return true;
	}
}