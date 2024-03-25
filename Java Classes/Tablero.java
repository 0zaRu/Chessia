import java.io.Serializable;

/**Clase tablero para generar objetos que llevan toda la información necesaria de la partida en tiempo real para evitar tantos pasos entre métodos y permitir el almacenamiento*/

class Tablero implements Serializable{

	private static final long serialVersionUID = 03042153;
	String nombre;

	String tablero[][]= new String[8][8];
	Pieza piezas[] = new Pieza[32];

	int nuevaX;
	int nuevaY;

	int pieza_específica = -1;
	boolean comer=false;
	int movimiento = 0;
	
	/**Método para iniciar la generación de un nuevo tablero desde 0*/
	static void tablero_inicial(Tablero partida){
		int nPieza = 0;
		for(partida.nuevaY=0; partida.nuevaY < partida.tablero.length; partida.nuevaY++){
			for (partida.nuevaX=0; partida.nuevaX < partida.tablero[partida.nuevaY].length; partida.nuevaX++){
				partida.tablero[partida.nuevaY][partida.nuevaX] = " ";

				if(partida.nuevaY == 0) fila_trasera(partida, true,  nPieza++);
				if(partida.nuevaY == 7) fila_trasera(partida, false, nPieza++);

				if(partida.nuevaY == 1 || partida.nuevaY == 6){ 
					Pieza pieza = new Pieza();
					pieza.posicionX = partida.nuevaX;
					pieza.posicionY = partida.nuevaY;

					if(partida.nuevaY == 1) pieza.color = true;
					else         pieza.color = false;
					
					pieza.nombre = "Peon";
					if(partida.nuevaY == 1) partida.tablero[partida.nuevaY][partida.nuevaX] = Character.toString(pieza.nombre.charAt(0));
					else 		 partida.tablero[partida.nuevaY][partida.nuevaX] = "*"+Character.toString(pieza.nombre.charAt(0))+"*";

					partida.piezas[nPieza++] = pieza;

				}
			}
		}
	}
	
	/**Método para generar la fila trasera de una nueva partida, tanto de las blancas como de las negras*/
	static void fila_trasera(Tablero partida, boolean color, int nPieza){
		Pieza pieza = new Pieza();
		pieza.color = color;
		
		pieza.posicionY = partida.nuevaY;
		pieza.posicionX = partida.nuevaX;
						
		switch(partida.nuevaX){
			case 0: case 7:
				pieza.nombre = "Torre";
				break;
			
			case 1: case 6:
				pieza.nombre = "Caballo";
				break;
			
			case 2: case 5:
				pieza.nombre = "Alfil";
				break;
			
			case 3:
				if(color) pieza.nombre = "Dama blanca";
				else      pieza.nombre = "Dama negra";
				break;
			
			case 4:
				if(color) pieza.nombre = "Rey blanco";
				else      pieza.nombre = "Rey negro";
				pieza.mate = false;
				break;
		}

		if(color) partida.tablero[partida.nuevaY][partida.nuevaX] = Character.toString(pieza.nombre.charAt(0));
		else      partida.tablero[partida.nuevaY][partida.nuevaX] = "*"+Character.toString(pieza.nombre.charAt(0))+"*";

		partida.piezas[nPieza] = pieza;

	}
	
	/**Método de impresión que muestra el tablero y piezas en función de la configuración visual de la partida*/
    static void mostrar_matriz(String[][] matriz, Config con){

		String casilla = "";

        System.out.println("\n\n\t\t\tTABLERO: ");
        System.out.println("\t\t\t===================================\n");

        for(int x=matriz.length-1; x>=0; x--){
			if(x == 7){ System.out.print("\t\t\t  "+con.supIzq);
            for(int y=1; y<matriz[x].length; y++)
				System.out.print(con.lineaHor+""+con.lineaHor+""+con.lineaHor+""+con.aristSup);

			System.out.print(con.lineaHor+""+con.lineaHor+""+con.lineaHor+""+con.supDer);
			}

			if(x < 7 && x >= 0){ System.out.print("\t\t\t  "+con.aristIzq);
				for(int y=1; y<matriz[x].length; y++)
					System.out.print(con.lineaHor+""+con.lineaHor+""+con.lineaHor+""+con.arist);
	
				System.out.print(con.lineaHor+""+con.lineaHor+""+con.lineaHor+""+con.aristDer);
			}

            System.out.println();
			System.out.print("\t\t\t"+(x+1)+" "+con.lineaVer);
            for(int y=0; y<matriz[x].length; y++){
				if(matriz[x][y].contains("*")){
					casilla = con.rojo+""+matriz[x][y].charAt(1)+""+con.blanco;
				
				}else if(matriz[x][y] == " "){
					casilla = "   ";
				
				}else
					casilla = " "+matriz[x][y]+" ";
				

                System.out.print(casilla+""+con.lineaVer);
				
			}
			if(x == 0){
				System.out.println();
				System.out.print("\t\t\t  "+con.infIzq);
				for(int y=1; y<matriz[x].length; y++)
					System.out.print(con.lineaHor+""+con.lineaHor+""+con.lineaHor+""+con.aristInf);
	
				System.out.print(con.lineaHor+""+con.lineaHor+""+con.lineaHor+""+con.infDer);
			}
            System.out.println();
        }
		System.out.println("\t\t\t    a   b   c   d   e   f   g   h");
        System.out.println("\n\n");
    }

    /**Método utilizado durante el desarrollo para ver las posiciones de las piezas en el tablero y hacer comprobaciones*/
	static void mostrar_piezas_prueba(Pieza piezas[]){
		for (int i = 0; i < piezas.length; i++)
			if(i<10)
				System.out.println(" "+i+". "+piezas[i].nombre+"\t"+piezas[i].posicionX+piezas[i].posicionY);
			else
				System.out.println(i+". "+piezas[i].nombre+"\t"+piezas[i].posicionX+piezas[i].posicionY);
	}

	/**Aquí se envía el índice de la pieza y la nueva posición en la que estará y se hace el movimiento, ya sea comiendo o moviendo*/
	static boolean efectuar_movimiento(Tablero partida, int pieza, int color){
		
		partida.tablero[partida.nuevaY][partida.nuevaX] = " ";	

		//Este primer if else solo comprueba si se puede comer o no y sale antes de hacer el movimiento si no es así
		
			if(partida.comer){
			boolean comer_valido = false;
			if(color % 2 != 0){
				for(int x = 16; x < 32; x++)
					if(partida.piezas[x].posicionX == partida.nuevaX && partida.piezas[x].posicionY == partida.nuevaY && x != 28){
						partida.piezas[x].vivo = false;
						comer_valido = true;
					}
			}
			else{
				for(int x = 0; x < 16; x++)
					if(partida.piezas[x].posicionX == partida.nuevaX && partida.piezas[x].posicionY == partida.nuevaY && x != 4){
						partida.piezas[x].vivo = false;
						comer_valido = true;
					}
			}
			if(!comer_valido){
				System.out.println("No se ha podido comer: Es el rey o es de tu color");
				return false;
			}
		}

			//si se quiere mover o se quería comer y ha sido válido, se efectua el cambio en el tablero de dicha pieza
		partida.tablero[partida.piezas[pieza].posicionY][partida.piezas[pieza].posicionX] = " ";
		partida.piezas[pieza].posicionY=partida.nuevaY;
		partida.piezas[pieza].posicionX=partida.nuevaX;
		
		if(pieza < 16)
			partida.tablero[partida.nuevaY][partida.nuevaX] = Character.toString(partida.piezas[pieza].nombre.charAt(0));
		else
			partida.tablero[partida.nuevaY][partida.nuevaX] = "*"+partida.piezas[pieza].nombre.charAt(0)+"*";
		
		
		return true;
	}
	
	/**Método utilizado para reajustar el tablero al leerlo de archivo porque se escribe mal la matriz String*/
	static String[][] reajustar_tablero(Tablero partida){
		
		for(int x = 0; x<8; x++)
			for(int y = 0; y<8; y++)
				partida.tablero[x][y] = " ";
		
		
		for(int z = 0; z < 32; z++) {
			if(z < 16) {
				partida.tablero[partida.piezas[z].posicionY][partida.piezas[z].posicionX] = Character.toString(partida.piezas[z].nombre.charAt(0));
			}else
				partida.tablero[partida.piezas[z].posicionY][partida.piezas[z].posicionX] = "*"+partida.piezas[z].nombre.charAt(0)+"*";
		}		
		return partida.tablero;
	}
}