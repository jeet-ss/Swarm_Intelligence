import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

/** 
 * Helper class.
 **/
class Counter {
	private int cnt;
	
	public Counter() {
		super();
		cnt = 0;
	}
	
	public void increment() {
		cnt++;
	}
	
	public int getValue() {
		return cnt;
	}
}

/**
 * DumbXMLParser is able to process an XML file.
 * 
 * @author helwig
 */
public class DumbXMLParser {
	
	protected class MyDefaultHandler extends DefaultHandler {
		
		protected final Counter counter;
		
		/**
		 * Constructs a new MyDefaultHandler.
		 */
		public MyDefaultHandler(Counter counter) {
			super();
			this.counter = counter;
		}
		
		/* (non-Javadoc)
		 * @see org.xml.sax.helpers.DefaultHandler#startElement(java.lang.String, java.lang.String, java.lang.String, org.xml.sax.Attributes)
		 */
		public void startElement(String uri, String localName, String qName, Attributes attributes) {
			if (qName.equals("graph")) {
				System.out.println("Starting to read this graph.");
			} else if (qName.equals("node")) {
				System.out.println("I found a node with id "
						+ attributes.getValue("id") + ", and name "
						+ attributes.getValue("name"));
				
				counter.increment();

			} else if (qName.equals("edge")) {
				System.out.println("There is an edge with id "
						+ attributes.getValue("id") + " from "
						+ attributes.getValue("source") + " to "
						+ attributes.getValue("target"));
			}
		}
		
		/* (non-Javadoc)
		 * @see org.xml.sax.helpers.DefaultHandler#endElement(java.lang.String, java.lang.String, java.lang.String)
		 */
		public void endElement(String uri, String localName, String qName) {
			if (qName.equals("graph")) {
				System.out.println("Finished to read the graph.");
			}
			else if(qName.equals("node")) {
				System.out.println("Finished to read this node.");
			}
			else if(qName.equals("edge")) {
				System.out.println("Finished to read this edge.");

			}
		}
	}

	/**
	 * Constructs a new DumbXMLParser.
	 */
	public DumbXMLParser() {
		super();
	}
	
	/**
	 * Processes XML data.
	 * 
	 * @param path path of input file
	 */
	public void processXMLData(String path, Counter counter) {
		
		try {
            BufferedReader input = new BufferedReader(
                    new InputStreamReader(new FileInputStream(path)));
            SAXParser saxParser = SAXParserFactory.newInstance().newSAXParser();
            MyDefaultHandler myHandler = new MyDefaultHandler(counter);
            saxParser.parse(new InputSource(input), myHandler);
		} catch (ParserConfigurationException e) {
			e.printStackTrace();
			System.exit(1);
		} catch (SAXException e) {
			e.printStackTrace();
			System.exit(1);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			System.exit(1);
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	
	public static void main(String[] args) {
		//String path = new String("data" + System.getProperty("file.separator") + "graph.xml");
		String path = new String("graph.xml");
		Counter myCounter = new Counter();

		DumbXMLParser constructor = new DumbXMLParser();
		constructor.processXMLData(path, myCounter);
		
		System.out.println("\nNumber of counted nodes: " + myCounter.getValue());
	}
	
	

}
