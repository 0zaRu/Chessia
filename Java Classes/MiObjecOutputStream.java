import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.OutputStream;

/**Mi método de escritura sin cabecera*/
class MiObjectOutputStream extends ObjectOutputStream
{
	public MiObjectOutputStream(OutputStream out) throws IOException
	{
		super(out);
	}
	
	protected MiObjectOutputStream() throws IOException, SecurityException
	{
		super();
	}
	
	protected void writeStreamHeader() throws IOException
	{
	}
}