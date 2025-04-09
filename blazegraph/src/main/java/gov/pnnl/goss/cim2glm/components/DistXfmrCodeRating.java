package gov.pnnl.goss.cim2glm.components;
//	----------------------------------------------------------
//	Copyright (c) 2017, Battelle Memorial Institute
//	All rights reserved.
//	----------------------------------------------------------

import org.apache.jena.query.*;
import java.util.HashMap;
import org.apache.commons.math3.complex.Complex;

public class DistXfmrCodeRating extends DistComponent {
	public static final String szQUERY = 
		"SELECT DISTINCT ?pname ?tname ?enum ?ratedS ?ratedU ?conn ?ang ?res ?id WHERE {"+
		" ?fdr c:IdentifiedObject.mRID ?fdrid."+
		" ?xft c:TransformerTank.PowerTransformer ?eq."+
		" ?eq c:Equipment.EquipmentContainer ?fdr."+
		" ?asset c:Asset.PowerSystemResources ?xft."+
		" ?asset c:Asset.AssetInfo ?t."+
		" ?p r:type c:PowerTransformerInfo."+
		" ?t c:TransformerTankInfo.PowerTransformerInfo ?p."+
		" ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
		" ?p c:IdentifiedObject.name ?pname."+
		" ?t c:IdentifiedObject.name ?tname."+
		" bind(strafter(str(?t),\"#\") as ?id)."+
		" ?e c:TransformerEndInfo.endNumber ?enum."+
		" ?e c:TransformerEndInfo.ratedS ?ratedS."+
		" ?e c:TransformerEndInfo.ratedU ?ratedU."+
		" ?e c:TransformerEndInfo.r ?res."+
		" ?e c:TransformerEndInfo.phaseAngleClock ?ang."+
		" ?e c:TransformerEndInfo.connectionKind ?connraw."+
		"       		bind(strafter(str(?connraw),\"WindingConnection.\") as ?conn)"+
		"} ORDER BY ?pname ?tname ?enum";

	public static final String szCountQUERY =
		"SELECT ?key (count(?enum) as ?count) WHERE {"+
		" SELECT DISTINCT ?key ?enum WHERE {"+
		" ?fdr c:IdentifiedObject.mRID ?fdrid."+
		" ?xft c:TransformerTank.PowerTransformer ?eq."+
		" ?eq c:Equipment.EquipmentContainer ?fdr."+
		" ?asset c:Asset.PowerSystemResources ?xft."+
		" ?asset c:Asset.AssetInfo ?t."+
		" ?p r:type c:PowerTransformerInfo."+
		" ?p c:IdentifiedObject.name ?pname."+
		" ?t c:TransformerTankInfo.PowerTransformerInfo ?p."+
		" ?t c:IdentifiedObject.name ?key."+
		" ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
		" ?e c:TransformerEndInfo.endNumber ?enum."+
		"}} GROUP BY ?key ORDER BY ?key";

	public String pname;
	public String tname;
	public String id;
	public int[] wdg;
	public String[] conn;
	public int[] ang;
	public double[] ratedS; 
	public double[] ratedU;
	public double[] r;
	public int size;

	public boolean glmUsed;

	public String GetJSONEntry () {
		StringBuilder buf = new StringBuilder ();

		buf.append ("{\"name\":\"" + pname +"\"");
		buf.append (",\"mRID\":\"" + id +"\"");
		buf.append ("}");
		return buf.toString();
	}

	private void SetSize (int val) {
		size = val;
		wdg = new int[size];
		conn = new String[size];
		ang = new int[size];
		ratedS = new double[size];
		ratedU = new double[size];
		r = new double[size];
	}

	public DistXfmrCodeRating (ResultSet results, HashMap<String,Integer> map) {
		if (results.hasNext()) {
			QuerySolution soln = results.next();
			String p = soln.get("?pname").toString();
			String t = soln.get("?tname").toString();
			pname = SafeName (p);
			tname = SafeName (t);
			id = soln.get("?id").toString();
			SetSize (map.get(tname));
			for (int i = 0; i < size; i++) {
				wdg[i] = Integer.parseInt (soln.get("?enum").toString());
				conn[i] = soln.get("?conn").toString();
				ang[i] = Integer.parseInt (soln.get("?ang").toString());
				ratedS[i] = Double.parseDouble (soln.get("?ratedS").toString());
				ratedU[i] = Double.parseDouble (soln.get("?ratedU").toString());
				r[i] = Double.parseDouble (soln.get("?res").toString());
				if ((i + 1) < size) {
					soln = results.next();
				}
			}
		}		
	}

	public String DisplayString() {
		StringBuilder buf = new StringBuilder ("");
		buf.append (pname + ":" + tname);
		for (int i = 0; i < size; i++) {
			buf.append ("\n  wdg=" + Integer.toString(wdg[i]) + " conn=" + conn[i] + " ang=" + Integer.toString(ang[i]));
			buf.append (" U=" + df4.format(ratedU[i]) + " S=" + df4.format(ratedS[i]) + " r=" + df4.format(r[i]));
		}
		return buf.toString();
	}

	public String GetGLM (DistXfmrCodeSCTest sct, DistXfmrCodeOCTest oct) {
		StringBuilder buf = new StringBuilder("object transformer_configuration {\n");

		double rpu = 0.0;
		double zpu = 0.0;
		double zbase1 = ratedU[0] * ratedU[0] / ratedS[0];
		double zbase2 = ratedU[1] * ratedU[1] / ratedS[1];
		if ((sct.ll[0] > 0.0) && (size < 3)) {
			rpu = 1000.0 * sct.ll[0] / ratedS[0];
		} else {
			// hard-wired for SINGLE_PHASE_CENTER_TAPPED,
			// which is the only three-winding case that GridLAB-D supports
			rpu = (r[0] / zbase1) + 0.5 * (r[1] / zbase2);
		}
		if (rpu <= 0.000001) {
			rpu = 0.000001; // GridLAB-D doesn't like zero
		}
		if (sct.fwdg[0] == 1) {
			zpu = sct.z[0] / zbase1;
		} else if (sct.fwdg[0] == 2) {
			zpu = sct.z[0] / zbase2;
		}
		double xpu = zpu;
		if (zpu >= rpu) {
//			xpu = Math.sqrt (zpu * zpu - rpu * rpu);  // TODO: this adjustment is correct, but was not done in RC1
		}

		String sConnect = GetGldTransformerConnection (conn, size);
		String sKVA = df3.format (ratedS[0] * 0.001);
		buf.append ("  name \"xcon_" + tname + "\";\n");
		buf.append ("  power_rating " + sKVA + ";\n");
		if (sConnect.equals("SINGLE_PHASE_CENTER_TAPPED")) {
			if (tname.contains ("_as_")) { // TODO - this is hard-wired to PNNL taxonomy feeder import
				buf.append ("  powerA_rating " + sKVA + ";\n");
				buf.append ("  powerB_rating 0.0;\n");
				buf.append ("  powerC_rating 0.0;\n");
			} else if (tname.contains ("_bs_")) {
				buf.append ("  powerA_rating 0.0;\n");
				buf.append ("  powerB_rating " + sKVA + ";\n");
				buf.append ("  powerC_rating 0.0;\n");
			} else if (tname.contains ("_cs_")) {
				buf.append ("  powerA_rating 0.0;\n");
				buf.append ("  powerB_rating 0.0;\n");
				buf.append ("  powerC_rating " + sKVA + ";\n");
			}
			//buf.append ("  primary_voltage " + df3.format (ratedU[0]) + ";\n");
			buf.append ("  primary_voltage " + df3.format (ratedU[0] / Math.sqrt(3.0)) + ";\n");// Edits MuMonish : Secondary Voltage Consistency //
			buf.append ("  secondary_voltage " + df3.format (ratedU[1]) + ";\n");
		} else if (sConnect.equals("SINGLE_PHASE")) {
			if (tname.contains ("_an_")) { // TODO - this is hard-wired to PNNL taxonomy feeder import
				buf.append ("  powerA_rating " + sKVA + ";\n");
				buf.append ("  powerB_rating 0.0;\n");
				buf.append ("  powerC_rating 0.0;\n");
				sConnect = "WYE_WYE";
			} else if (tname.contains ("_bn_")) {
				buf.append ("  powerA_rating 0.0;\n");
				buf.append ("  powerB_rating " + sKVA + ";\n");
				buf.append ("  powerC_rating 0.0;\n");
				sConnect = "WYE_WYE";
			} else if (tname.contains ("_cn_")) {
				buf.append ("  powerA_rating 0.0;\n");
				buf.append ("  powerB_rating 0.0;\n");
				buf.append ("  powerC_rating " + sKVA + ";\n");
				sConnect = "WYE_WYE";
			}
			buf.append ("  primary_voltage " + df3.format (ratedU[0] * Math.sqrt(3.0)) + ";\n");
			buf.append ("  secondary_voltage " + df3.format (ratedU[1] * Math.sqrt(3.0)) + ";\n");
		} else {
			buf.append ("  primary_voltage " + df3.format (ratedU[0] / Math.sqrt(3.0)) + ";\n");
			//buf.append ("  secondary_voltage " + df3.format (ratedU[1] / Math.sqrt(3.0)) + ";\n");
			buf.append ("  secondary_voltage " + df3.format (ratedU[1]) + ";\n");// Edits MuMonish : Secondary Voltage Consistency //
		}
		if (sConnect.equals ("Y_D")) {
			buf.append("  connect_type WYE_WYE; // should be Y_D\n");
		} else {
			buf.append("  connect_type " + sConnect + ";\n");
		}
		if (sConnect.equals ("SINGLE_PHASE_CENTER_TAPPED")) {
			String impedance = CFormat (new Complex (0.5 * rpu, 0.8 * xpu));
			String impedance1 = CFormat (new Complex (rpu, 0.4 * xpu));
			String impedance2 = CFormat (new Complex (rpu, 0.4 * xpu));
			buf.append ("  impedance " + impedance + ";\n");
			buf.append ("  impedance1 " + impedance1 + ";\n");
			buf.append ("  impedance2 " + impedance2 + ";\n");
		} else {
			buf.append ("  resistance " + df6.format (rpu) + ";\n");
			buf.append ("  reactance " + df6.format (xpu) + ";\n");
		}
		if (oct.iexc > 0.0) {
			buf.append ("  shunt_reactance " + df6.format (100.0 / oct.iexc) + ";\n");
		}
		if (oct.nll > 0.0) {
			buf.append ("  shunt_resistance " + df6.format (ratedS[0] / oct.nll / 1000.0) + ";\n");
		}
		buf.append("}\n");
		return buf.toString();
	}

	// physical ohms to match the short circuit test load losses
	public void SetWindingResistances (DistXfmrCodeSCTest sct) {
		double r12pu, r13pu, r23pu, r1pu, r2pu, r3pu, Sbase;
		Sbase = sct.sbase[0]; // the per-unit manipulations have to be done on this common base
		if (sct.size == 1) {
			r12pu = 1000.0 * sct.ll[0] / Sbase;
			r1pu = 0.5 * r12pu;
			r2pu = r1pu;
			r[0] = r1pu * ratedU[0] * ratedU[0] / Sbase;
			r[1] = r2pu * ratedU[1] * ratedU[1] / Sbase;
		} else if (sct.size == 3) {
			// test resistances on their own base
			r12pu = 1000.0 * sct.ll[0] / sct.sbase[0];
			r13pu = 1000.0 * sct.ll[1] / sct.sbase[1];
			r23pu = 1000.0 * sct.ll[2] / sct.sbase[2];
			// convert r13 and r23 to a common base
			r13pu *= (Sbase / sct.sbase[1]);
			r23pu *= (Sbase / sct.sbase[2]);
			// determine the star equivalent in per-unit
			r1pu = 0.5 * (r12pu + r13pu - r23pu);
			r2pu = 0.5 * (r12pu + r23pu - r13pu);
			r3pu = 0.5 * (r13pu + r23pu - r12pu);
			// convert to ohms from the common Sbase
			r[0] = r1pu * ratedU[0] * ratedU[0] / Sbase;
			r[1] = r2pu * ratedU[1] * ratedU[1] / Sbase;
			r[2] = r3pu * ratedU[2] * ratedU[2] / Sbase;
		}
	}

	public String GetDSS(DistXfmrCodeSCTest sct, DistXfmrCodeOCTest oct) {
		boolean bDelta;
		int phases = 3;
		double zbase, xpct, zpct, rpct, pctloss, pctimag, pctiexc, rescale;
		int fwdg, twdg, i;

		for (i = 0; i < size; i++) {
			if (conn[i].contains("I")) {
				phases = 1;
			}
		}
		StringBuilder buf = new StringBuilder("new Xfmrcode." + tname + " windings=" + Integer.toString(size) +
																					" phases=" + Integer.toString(phases));

		// short circuit tests - valid only up to 3 windings
//		for (i = 0; i < sct.size; i++) {
//			fwdg = sct.fwdg[i];
//			twdg = sct.twdg[i];
//			zbase = ratedU[fwdg-1] * ratedU[fwdg-1] / ratedS[fwdg-1];
//			xpct = 100.0 * sct.z[i] / zbase; // not accounting for ll
//			if ((fwdg == 1 && twdg == 2) || (fwdg == 2 && twdg == 1)) {
//				buf.append(" xhl=" + df6.format(xpct));
//			} else if ((fwdg == 1 && twdg == 3) || (fwdg == 3 && twdg == 1)) {
//				buf.append(" xht=" + df6.format(xpct));
//			} else if ((fwdg == 2 && twdg == 3) || (fwdg == 3 && twdg == 2)) {
//				buf.append(" xlt=" + df6.format(xpct));
//			}
//		}

		// MuMonish: New Edits .....
		// short circuit tests - valid only up to 3 windings; put on the Winding 1 base
		for (i = 0; i < sct.size; i++) {
			fwdg = sct.fwdg[i];
			twdg = sct.twdg[i];
			zbase = ratedU[fwdg-1] * ratedU[fwdg-1] / sct.sbase[i];
			// zbase = ratedU[0] * ratedU[0] / sct.sbase[i]; // MuMonish making the xhl, xht the same
			// xpct = 100.0 * sct.z[i] / zbase; // not accounting for ll
			zpct = 100.0 * sct.z[i] / zbase;
			rpct = 100.0 * sct.ll[i] / sct.sbase[i]; //  MuMonish  * 1000.0
			//xpct = Math.sqrt(zpct*zpct - rpct*rpct);
			// Mumonish ignoring loss where loss is greater than leakage
			if (rpct >  zpct) {
				xpct  = zpct;
			} else {
				xpct = Math.sqrt(zpct*zpct - rpct*rpct);
			}

			// convert rpct, xpct from the test base power to winding 1 base power
			rescale = ratedS[0] / sct.sbase[i];
			rpct *= rescale;
			xpct *= rescale;
			if ((fwdg == 1 && twdg == 2) || (fwdg == 2 && twdg == 1)) {
				buf.append(" xhl=" + df6.format(xpct));
			} else if ((fwdg == 1 && twdg == 3) || (fwdg == 3 && twdg == 1)) {
				buf.append(" xht=" + df6.format(xpct));
			} else if ((fwdg == 2 && twdg == 3) || (fwdg == 3 && twdg == 2)) {
				buf.append(" xlt=" + df6.format(xpct));
			}
		}

		// open circuit test
		pctloss = 100.0 * 1000.0 * oct.nll / ratedS[0];
		pctiexc = oct.iexc * oct.sbase / ratedS[0];
		if ((pctloss > 0.0) && (pctloss <= pctiexc)) {
			pctimag = Math.sqrt(pctiexc * pctiexc - pctloss * pctloss);
		} else {
			pctimag = pctiexc;
		}
		buf.append (" %imag=" + df3.format(pctimag) + " %noloadloss=" + df3.format(pctloss) + "\n");
//		buf.append (" %imag=" + df3.format(oct.iexc) + " %noloadloss=" + df3.format(0.001 * oct.nll / ratedS[0]) + "\n");

		// winding ratings
//		SetWindingResistances (sct);
		for (i = 0; i < size; i++) {
			if (conn[i].contains("D")) {
				bDelta = true;
			} else {
				bDelta = false;
			}
//			zbase = ratedU[i] * ratedU[i] / ratedS[i];
			zbase = ratedU[i] * ratedU[i] / ratedS[0]; // PU impedances always on winding 1's kva base
			buf.append("~ wdg=" + Integer.toString(i + 1) + " conn=" + DSSConn(bDelta) +
								 " kv=" + df3.format(0.001 * ratedU[i]) + " kva=" + df1.format(0.001 * ratedS[i]) +
								 " %r=" + df6.format(100.0 * r[i] / zbase) + "\n");
		}
		return buf.toString();
	}

	public String GetKey() {
		return tname;
	}
}

