package gov.pnnl.goss.cim2glm.components;
//	----------------------------------------------------------
//	Copyright (c) 2018, Battelle Memorial Institute
//	All rights reserved.
//	----------------------------------------------------------

import org.apache.jena.query.*;
import java.util.HashMap;

public class DistJumper extends DistSwitch {
	public static final String szQUERY = szSELECT + " ?s r:type c:Jumper." + szWHERE;

	public DistJumper (ResultSet results) {
		super (results);
	}

	public String CIMClass() {
		return "Jumper";
	}

	public String GetGLM () {
		StringBuilder buf = new StringBuilder ("object fuse {\n");

		buf.append ("  name \"jump_" + name + "\";\n");
		buf.append ("  from \"" + bus1 + "\";\n");
		buf.append ("  to \"" + bus2 + "\";\n");
		buf.append ("  phases " + glm_phases + ";\n");
		if ( rated == 0.0){
			rated = 900.0;
		}
		buf.append ("  current_limit " + df2.format (rated) + ";\n");
		if (open) {
			buf.append ("  status OPEN;\n");
		} else {
			buf.append ("  status CLOSED;\n");
		}
		buf.append ("  mean_replacement_time 3600;\n");
		buf.append("}\n");
		return buf.toString();
	}
}


