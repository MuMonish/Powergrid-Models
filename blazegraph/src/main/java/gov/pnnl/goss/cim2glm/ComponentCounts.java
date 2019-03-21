package gov.pnnl.goss.cim2glm;
import gov.pnnl.goss.cim2glm.components.*;
import org.apache.jena.query.*;
import org.apache.jena.rdf.model.Literal;
import java.util.Dictionary;
import java.util.Enumeration;
import java.util.Hashtable;

/**
 * <p>This class executes count queries against Blazegraph for each DistComponent subclass that contains a SPARQL query</p>
 *
 * <p>Invoke as a console-mode program</p>
 *
 * @see EndpointTest#main
 *
 * @author Erik Lee
 * @version 1.0
 *
 */
public class ComponentCounts {

    static final String szEND = "http://localhost:9999/blazegraph/namespace/kb/sparql";
    static final String nsCIM = "http://iec.ch/TC57/2012/CIM-schema-cim17#";
    static final String nsRDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
    static final String countPrefix = "SELECT (COUNT(*) as ?count) WHERE { ";

    public static void main (String args[]) {
        String qPrefix = "PREFIX r: <" + nsRDF + "> PREFIX c: <" + nsCIM + "> ";
        Dictionary<String, String> compName_query = new Hashtable<>();
        compName_query.put("DistBaseVoltage", qPrefix + countPrefix + DistBaseVoltage.szQUERY + "}");
        compName_query.put("DistBreaker", qPrefix + countPrefix + DistBreaker.szQUERY + "}");
        compName_query.put("DistCapacitor", qPrefix + countPrefix + DistCapacitor.szQUERY + "}");
        compName_query.put("DistCoordinates", qPrefix + countPrefix + DistCoordinates.szQUERY + "}");
        compName_query.put("DistConcentricNeutralCable", qPrefix + countPrefix + DistConcentricNeutralCable.szQUERY + "}");
        compName_query.put("DistDisconnector", qPrefix + countPrefix + DistDisconnector.szQUERY + "}");
        compName_query.put("DistFeeder", qPrefix + countPrefix + DistFeeder.szQUERY + "}");
        compName_query.put("DistFuse", qPrefix + countPrefix + DistFuse.szQUERY + "}");
        compName_query.put("DistGroundDisconnector", qPrefix + countPrefix + DistGroundDisconnector.szQUERY + "}");
        compName_query.put("DistHouse", qPrefix + countPrefix + DistHouse.szQUERY + "}");
        compName_query.put("DistJumper", qPrefix + countPrefix + DistJumper.szQUERY + "}");
        compName_query.put("DistLinesCodeZ", qPrefix + countPrefix + DistLinesCodeZ.szQUERY + "}");
        compName_query.put("DistLinesInstanceZ", qPrefix + countPrefix + DistLinesInstanceZ.szQUERY + "}");
        compName_query.put("DistLineSpacing", qPrefix + countPrefix + DistLineSpacing.szQUERY + "}");
        compName_query.put("DistLinesSpacingZ", qPrefix + countPrefix + DistLinesSpacingZ.szQUERY + "}");
        compName_query.put("DistLoad", qPrefix + countPrefix + DistLoad.szQUERY + "}");
        compName_query.put("DistLoadBreakSwitch", qPrefix + countPrefix + DistLoadBreakSwitch.szQUERY + "}");
        compName_query.put("DistMeasurement", qPrefix + countPrefix + DistMeasurement.szQUERY + "}");
        compName_query.put("DistOverheadWire", qPrefix + countPrefix + DistOverheadWire.szQUERY + "}");
        compName_query.put("DistPowerXfmrCore", qPrefix + countPrefix + DistPowerXfmrCore.szQUERY + "}");
        compName_query.put("DistPowerXfmrMesh", qPrefix + countPrefix + DistPowerXfmrMesh.szQUERY + "}");
        compName_query.put("DistPowerXfmrWinding", qPrefix + countPrefix + DistPowerXfmrWinding.szQUERY + "}");
        compName_query.put("DistRecloser", qPrefix + countPrefix + DistRecloser.szQUERY + "}");
        compName_query.put("DistRegulator", qPrefix + countPrefix + DistRegulator.szQUERY + "}");
        compName_query.put("DistSectionaliser", qPrefix + countPrefix + DistSectionaliser.szQUERY + "}");
        compName_query.put("DistSequenceMatrix", qPrefix + countPrefix + DistSequenceMatrix.szQUERY + "}");
        compName_query.put("DistSolar", qPrefix + countPrefix + DistSolar.szQUERY + "}");
        compName_query.put("DistStorage", qPrefix + countPrefix + DistStorage.szQUERY + "}");
        compName_query.put("DistSubstation", qPrefix + countPrefix + DistSubstation.szQUERY + "}");
        compName_query.put("DistSyncMachine", qPrefix + countPrefix + DistSyncMachine.szQUERY + "}");
        compName_query.put("DistTapeShieldCable", qPrefix + countPrefix + DistTapeShieldCable.szQUERY + "}");
        compName_query.put("DistThermostat", qPrefix + countPrefix + DistThermostat.szQUERY + "}");
        compName_query.put("DistXfmrBank", qPrefix + countPrefix + DistXfmrBank.szQUERY + "}");
        compName_query.put("DistXfmrCodeOCTest", qPrefix + countPrefix + DistXfmrCodeOCTest.szQUERY + "}");
        compName_query.put("DistXfmrCodeRating", qPrefix + countPrefix + DistXfmrCodeRating.szQUERY + "}");
        compName_query.put("DistXfmrCodeSCTest", qPrefix + countPrefix + DistXfmrCodeSCTest.szQUERY + "}");
        compName_query.put("DistXfmrTank", qPrefix + countPrefix + DistXfmrTank.szQUERY + "}");

        for(Enumeration key  = compName_query.keys(); key.hasMoreElements();) {
            String compName = key.nextElement().toString();
            String queryStr = compName_query.get(compName);

            try {
                Query query = QueryFactory.create(queryStr);
                QueryExecution qexec = QueryExecutionFactory.sparqlService(szEND, query);
                ResultSet results = qexec.execSelect();

                while (results.hasNext()) {
                    QuerySolution soln = results.next();
                    Literal node = (Literal) soln.get("?count");
                    System.out.format(compName + "  [%d]\r\n", node.getInt());
                }
            } catch (Exception e) {
                System.out.printf("Exception running query from " + compName + ": \r\n");
                System.out.printf("\t" + e.getMessage() + "\r\n");
                System.out.printf(queryStr + "\r\n");
            }
        }
    }
}
