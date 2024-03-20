import java.io.EOFException;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

/**Clase orientada a la configuración visual del juego para que se pueda utilizar desde cualquier entorno*/

class Config implements Serializable{

	private static final long serialVersionUID = 030512;
	String nombre = "";

	char supIzq, supDer, infIzq, infDer;
	
	char arist, aristSup, aristInf, aristIzq, aristDer;

	char lineaHor, lineaVer;

	String rojo;
	String blanco;

	/**Se establece la configuración visual default del programa*/
	static Config cDefault(Config con){

		con.supIzq = (char)9556;
		con.lineaHor = (char)9552;
		con.aristSup = (char)9574;
		con.supDer = (char)9559;

		con.lineaVer = (char)9553;

		con.aristIzq = (char)9568;
		con.arist = (char)9580;
		con.aristDer = (char)9571;

		con.infIzq = (char)9562;
		con.aristInf = (char)9577;
		con.infDer = (char)9565;

		con.rojo = "\u001B[31m ";
		con.blanco = "\u001B[37m ";

		return con;
	}
	
	/**Se genera una configuración visual personalizada por el usuario y se almacena con el método guarda si el usuario quiere*/
	static void creaConfig(Config con, String archivo){

		System.out.println("Vamos a crear una configuración visual acorde a tus posibilidades y preferencias. ");
		System.out.print("\u001B[31m¿Ves este texto en rojo?\u001B[37m  (S/N): ");
		char opcion = Ajedrez.kb.nextLine().charAt(0);

		if(Character.toUpperCase(opcion) == 'S' ){
			con.rojo = "\u001B[31m ";
			con.blanco = "\u001B[37m ";
		
		}else{
			con.rojo = "*";
			con.blanco = "*";
		}

		System.out.print("\n\n\""+(char)9562+"\"\nEntre las comillas, ¿ves una L o una interrogación? (L/?): ");
		opcion = Ajedrez.kb.nextLine().charAt(0);

		if(Character.toUpperCase(opcion) == 'L'){
			
			con.supIzq = (char)9556;
			con.lineaHor = (char)9552;
			con.aristSup = (char)9574;
			con.supDer = (char)9559;

			con.lineaVer = (char)9553;

			con.aristIzq = (char)9568;
			con.arist = (char)9580;
			con.aristDer = (char)9571;

			con.infIzq = (char)9562;
			con.aristInf = (char)9577;
			con.infDer = (char)9565;
		
		}else{

			con.supIzq = con.aristSup = con.supDer = con.aristIzq = con.arist = con.aristDer = con.infIzq = con.aristInf = con.infDer = '+';
			
			con.lineaHor = '-';
			con.lineaVer = '|';
		}

		System.out.print("\n\n¿Quieres guardar la configuración en un fichero? (S/N): ");
		opcion = Ajedrez.kb.nextLine().charAt(0);

		if(Character.toUpperCase(opcion) == 'S')
			if(Config.guarda(con, archivo))
				System.out.println("Se ha guardado con éxito");
			else
				System.out.println("Hubo un problema al guardar la configuración.");

		System.out.println("\nPulse enter para continuar ...");
		Ajedrez.kb.nextLine();

	}
	
	/**Se guarda en el archivo pasado por args[1] una configuración visual especificada por el usuario*/
	static boolean guarda(Config con, String archivo){
		System.out.println("Nombre de la configuración: ");
		con.nombre = Ajedrez.kb.nextLine();

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
				oos = new ObjectOutputStream(new FileOutputStream(ruta));
				oos.writeObject(con);
				
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
				moos.writeObject(con);
		
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				valido = false;
				
			} catch (IOException e) {
				e.printStackTrace();
				valido = false;
			}
		}

		if(!valido) return false;

		return true;
	}

	/**Se carga una configuración visual desde el archivo pasado por args[1]*/
	static Config carga(Config con, String archivo){
		Ajedrez.limpiar_pantalla();
		int cont = 1;
		boolean valido = true;
		ObjectInputStream ois = null;
		Config temporal = null;
		File ruta = new File(archivo);
		
		if(ruta.length() == 0){
			System.out.println("No hay configuraciones guardadas");
			return null;
		}
		
			try {

				System.out.println("CONFIGURACIONES GUARDADAS:");
				System.out.println("====================================");
				ois = new ObjectInputStream(new FileInputStream(ruta));
				
				while((temporal = (Config)ois.readObject()) != null){
					
					System.out.println("\t"+(cont++) +". "+temporal.nombre);	
				}
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
			int posicion = Ajedrez.kb.nextInt();
			
			cont = 1;
			boolean seguir = true;

			try {
				ois = new ObjectInputStream(new FileInputStream(ruta));
				
				while(seguir && ((temporal = (Config)ois.readObject()) != null)){
					
					if(cont == posicion){
						con = temporal;
						seguir = false;
					}
					cont++;
				}
	
			} catch (EOFException e) {
			} catch (ClassCastException e){
				System.out.println("Configuración no encontrada");
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
					con = null;
			}

		return con;
	}
}