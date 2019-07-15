package gov.pnnl.goss.cim2glm.components;
//	----------------------------------------------------------
//	Copyright (c) 2017, Battelle Memorial Institute
//	All rights reserved.
//	----------------------------------------------------------

import org.apache.jena.query.*;
import java.util.HashMap;

public class DistDisconnector extends DistSwitch {
	public static final String szQUERY = szSELECT + " ?s r:type c:Disconnector." + szWHERE;

	public DistDisconnector (ResultSet results) {
		super (results);
	}

	public String CIMClass() {
		return "Disconnector";
	}

	public String GetGLM () {
		StringBuilder buf = new StringBuilder ("object switch {\n");

		buf.append ("  name \"discon_" + name + "\";\n");
		buf.append ("  from \"" + bus1 + "\";\n");
		buf.append ("  to \"" + bus2 + "\";\n");
		buf.append ("  phases " + glm_phases + ";\n");
		if (open) {
			buf.append ("  status OPEN;\n");
		} else {
			buf.append ("  status CLOSED;\n");
		}
		buf.append("}\n");
		return buf.toString();
	}
}