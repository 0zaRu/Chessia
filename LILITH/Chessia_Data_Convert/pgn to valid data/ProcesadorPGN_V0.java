import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class ProcesadorPGN_V0 {

    private static final String DIRECTORIO_FUENTE = "Source Data";
    private static final String FICHERO_DESTINO = "Target Data";

    public static void main(String[] args) throws IOException {
        File archivoDestino = new File(FICHERO_DESTINO);
        if (archivoDestino.exists()) 
            archivoDestino.delete();
        
        archivoDestino.createNewFile();

        File directorioFuente = new File(DIRECTORIO_FUENTE);
        
        for (File archivoPGN : directorioFuente.listFiles()) 
            procesarFicheroPGN(archivoPGN, archivoDestino);
    }

    private static void procesarFicheroPGN(File archivoPGN, File archivoDestino) throws IOException {
        BufferedReader lector = new BufferedReader(new FileReader(archivoPGN));
        BufferedWriter escritor = new BufferedWriter(new FileWriter(archivoDestino, true));

        String linea = "";
        String fichero = "";
        while ((linea = lector.readLine()) != null) {
            if (linea.startsWith("[") || linea.isEmpty())
                continue;
            
            if (linea.endsWith("1-0") || linea.endsWith("0-1") || linea.endsWith("1/2-1/2"))
                linea += "\n";
            else
                linea += " ";

            linea = linea.replaceAll("\\d+\\.", "");
            linea = linea.replaceAll("  ", " ");
            fichero += linea;
        }
        
        escritor.write(fichero);

        lector.close();
        escritor.close();
    }
}
