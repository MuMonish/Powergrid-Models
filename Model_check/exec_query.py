# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:29:19 2020

@author: mukh915
"""

from SPARQLWrapper import SPARQLWrapper2#, JSON
import sys
# constants.py is used for configuring blazegraph.
import constant
import json

sparql = SPARQLWrapper2(constant.blazegraph_url)

###############################################################################    
############################  Line_segment ####################################
###############################################################################

def query_line_segment(feeder_mrid):
              
    qstr_ACLineSegment = constant.prefix + """SELECT ?name ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?id (group_concat(distinct ?phs;separator="") as ?phases) WHERE {
      SELECT ?name ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?phs ?id WHERE {
     VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?s r:type c:ACLineSegment.
     ?s c:Equipment.EquipmentContainer ?fdr.
     ?s c:IdentifiedObject.name ?name.
     ?s c:IdentifiedObject.mRID ?id.
     ?s c:ConductingEquipment.BaseVoltage  ?bv .
     ?bv c:BaseVoltage.nominalVoltage  ?basev .
     ?s c:PowerSystemResource.Location ?loc .
     ?t1 c:Terminal.ConductingEquipment ?s.
     ?t1 c:ACDCTerminal.sequenceNumber "1".
     ?t1 c:Terminal.ConnectivityNode ?cn1. 
     ?pt1 c:PositionPoint.Location ?loc ;
          c:PositionPoint.sequenceNumber "1" ;
    	  c:PositionPoint.xPosition ?bus1x ;
    	  c:PositionPoint.yPosition ?bus1y .         
     ?cn1 c:IdentifiedObject.name ?bus1.
     ?t2 c:Terminal.ConductingEquipment ?s.
     ?t2 c:ACDCTerminal.sequenceNumber "2". 
     ?t2 c:Terminal.ConnectivityNode ?cn2.
     ?pt2 c:PositionPoint.Location ?loc ;
          c:PositionPoint.sequenceNumber "2" ;
    	  c:PositionPoint.xPosition ?bus2x ;
    	  c:PositionPoint.yPosition ?bus2y .
     ?cn2 c:IdentifiedObject.name ?bus2
    	OPTIONAL {?acp c:ACLineSegmentPhase.ACLineSegment ?s.
     	?acp c:ACLineSegmentPhase.phase ?phsraw.
       	bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) }
     } ORDER BY ?name ?phs
    }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?id
    ORDER BY ?name
    """
    sparql.setQuery(qstr_ACLineSegment)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
############################  Line Spacing ####################################
###############################################################################
    
def query_line_spacing(feeder_mrid):
              
    qstr_ACLineSegment = constant.prefix + """SELECT  ?name ?id ?basev ?bus1 ?bus2 ?fdrid ?len ?spacing ?wname ?wclass (GROUP_CONCAT(DISTINCT ?phs ; separator='') AS ?phases) (GROUP_CONCAT(DISTINCT ?phname ; separator='') AS ?phwires) (GROUP_CONCAT(DISTINCT ?phclass ; separator='') AS ?phclasses)
    WHERE
      { SELECT  ?name ?id ?basev ?bus1 ?bus2 ?fdrid ?len ?spacing ?wname ?wclass ?phs ?phname ?phclass
        WHERE
          { 
          VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
          ?s    r:type                c:ACLineSegment ;
                  c:Equipment.EquipmentContainer  ?fdr .
            ?fdr  c:IdentifiedObject.mRID  ?fdrid .
            ?s    c:IdentifiedObject.name  ?name
            BIND(strafter(str(?s), "#") AS ?id)
            ?s      c:ConductingEquipment.BaseVoltage  ?bv .
            ?bv     c:BaseVoltage.nominalVoltage  ?basev .
            ?s      c:Conductor.length    ?len .
            ?asset  c:Asset.PowerSystemResources  ?s ;
                    c:Asset.AssetInfo     ?inf .
            ?inf    c:IdentifiedObject.name  ?spacing ;
                    r:type                c:WireSpacingInfo
            OPTIONAL
              { ?wasset  c:Asset.PowerSystemResources  ?s ;
                         c:Asset.AssetInfo     ?winf .
                ?winf    c:WireInfo.radius     ?rad ;
                         c:IdentifiedObject.name  ?wname ;
                         r:type                ?classraw
                BIND(strafter(str(?classraw), "cim17#") AS ?wclass)
              }
            ?t1   c:Terminal.ConductingEquipment  ?s ;
                  c:Terminal.ConnectivityNode  ?cn1 ;
                  c:ACDCTerminal.sequenceNumber  "1" .
            ?cn1  c:IdentifiedObject.name  ?bus1 .
            ?t2   c:Terminal.ConductingEquipment  ?s ;
                  c:Terminal.ConnectivityNode  ?cn2 ;
                  c:ACDCTerminal.sequenceNumber  "2" .
            ?cn2  c:IdentifiedObject.name  ?bus2
            OPTIONAL
              { ?acp  c:ACLineSegmentPhase.ACLineSegment  ?s ;
                      c:ACLineSegmentPhase.phase  ?phsraw
                BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
                OPTIONAL
                  { ?phasset  c:Asset.PowerSystemResources  ?acp ;
                              c:Asset.AssetInfo     ?phinf .
                    ?phinf    c:WireInfo.radius     ?phrad ;
                              c:IdentifiedObject.name  ?phname ;
                              r:type                ?phclassraw
                    BIND(strafter(str(?phclassraw), "cim17#") AS ?phclass)
                  }
              }
          }
        ORDER BY ?name ?phs
      }
    GROUP BY ?name ?id ?basev ?bus1 ?bus2 ?fdrid ?len ?spacing ?wname ?wclass
    ORDER BY ?name
    """
    sparql.setQuery(qstr_ACLineSegment)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
################################ Load #########################################
###############################################################################
    
def query_load(feeder_mrid):
    
    qstr_distributed_load = constant.prefix + """SELECT  ?name ?bus ?basev ?p ?q ?conn ?pz ?qz ?pi ?qi ?pp ?qp ?pe ?qe ?id ?fdrid (GROUP_CONCAT(DISTINCT ?phs ; separator='') AS ?phases)
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
      ?s    r:type                c:EnergyConsumer ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:EnergyConsumer.pfixed  ?p ;
              c:EnergyConsumer.qfixed  ?q ;
              c:EnergyConsumer.phaseConnection  ?connraw
        BIND(strafter(str(?connraw), "PhaseShuntConnectionKind.") AS ?conn)
        ?s   c:EnergyConsumer.LoadResponse  ?lr .
        ?lr  c:LoadResponseCharacteristic.pConstantImpedance  ?pz ;
             c:LoadResponseCharacteristic.qConstantImpedance  ?qz ;
             c:LoadResponseCharacteristic.pConstantCurrent  ?pi ;
             c:LoadResponseCharacteristic.qConstantCurrent  ?qi ;
             c:LoadResponseCharacteristic.pConstantPower  ?pp ;
             c:LoadResponseCharacteristic.qConstantPower  ?qp ;
             c:LoadResponseCharacteristic.pVoltageExponent  ?pe ;
             c:LoadResponseCharacteristic.qVoltageExponent  ?qe
        OPTIONAL
          { ?ecp  c:EnergyConsumerPhase.EnergyConsumer  ?s ;
                  c:EnergyConsumerPhase.phase  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
        BIND(strafter(str(?s), "#") AS ?id)
        ?t   c:Terminal.ConductingEquipment  ?s ;
             c:Terminal.ConnectivityNode  ?cn .
        ?cn  c:IdentifiedObject.name  ?bus
      }
    GROUP BY ?name ?bus ?basev ?p ?q ?conn ?pz ?qz ?pi ?qi ?pp ?qp ?pe ?qe ?id ?fdrid
    ORDER BY ?name
    """
    sparql.setQuery(qstr_distributed_load)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property


###############################################################################    
######################### Transformer Vector Group ############################
###############################################################################
    
def query_xfmr_vector_group():
    
    qstr_xfmr_vector_group = constant.prefix + """SELECT  ?pname ?vgrp ?tname ?fdrid
    WHERE
      { ?p    r:type                c:PowerTransformer ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?p    c:IdentifiedObject.name  ?pname ;
              c:PowerTransformer.vectorGroup  ?vgrp .
        ?t    c:TransformerTank.PowerTransformer  ?p ;
              c:IdentifiedObject.name  ?tname
      }
    ORDER BY ?pname ?tname
    """
    sparql.setQuery(qstr_xfmr_vector_group)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'pname' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
####################### Transformer Tank Information ##########################
###############################################################################
    
def query_transformer(feeder_mrid):
    
    qstr_transformer = constant.prefix + """SELECT  ?pname ?tname ?xfmrcode ?vgrp ?bus1 ?bus1x ?bus1y ?phs1 ?basev1 ?bus2 ?bus2x ?bus2y ?phs2 ?basev2
      { 
        VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
        ?p      r:type                c:PowerTransformer ;
                c:Equipment.EquipmentContainer  ?fdr .
        ?fdr    c:IdentifiedObject.mRID  ?fdrid .
        ?p      c:IdentifiedObject.name  ?pname ;
                c:PowerTransformer.vectorGroup  ?vgrp .
        ?p      c:PowerSystemResource.Location ?loc .
        ?t      c:TransformerTank.PowerTransformer  ?p ;
                c:IdentifiedObject.name  ?tname .
        ?asset  c:Asset.PowerSystemResources  ?t ;
                c:Asset.AssetInfo     ?inf .
        ?inf    c:IdentifiedObject.name  ?xfmrcode .
        ?end1   c:TransformerTankEnd.TransformerTank  ?t ;
                c:TransformerEnd.endNumber  "1" ;
                c:TransformerTankEnd.phases  ?phsraw1
        BIND(strafter(str(?phsraw1), "PhaseCode.") AS ?phs1)
        ?end1   c:TransformerEnd.BaseVoltage  ?bv1 .
        ?bv1    c:BaseVoltage.nominalVoltage  ?basev1 .
        ?end1   c:TransformerEnd.Terminal  ?trm1 .
        ?trm1   c:Terminal.ConnectivityNode  ?cn1 .
        ?pt1    c:PositionPoint.Location ?loc ;
                c:PositionPoint.sequenceNumber "1" ;
    	        c:PositionPoint.xPosition ?bus1x ;
    	        c:PositionPoint.yPosition ?bus1y . 
        ?cn1    c:IdentifiedObject.name  ?bus1 .
        ?end2   c:TransformerTankEnd.TransformerTank  ?t ;
                c:TransformerEnd.endNumber  "2" ;
                c:TransformerTankEnd.phases  ?phsraw2
        BIND(strafter(str(?phsraw2), "PhaseCode.") AS ?phs2)
        ?end2   c:TransformerEnd.BaseVoltage  ?bv2 .
        ?bv2    c:BaseVoltage.nominalVoltage  ?basev2 .
        ?end2   c:TransformerEnd.Terminal  ?trm2 .
        ?trm2   c:Terminal.ConnectivityNode  ?cn2 .
        ?pt2    c:PositionPoint.Location ?loc ;
                c:PositionPoint.sequenceNumber "2" ;
    	        c:PositionPoint.xPosition ?bus2x ;
    	        c:PositionPoint.yPosition ?bus2y .
        ?cn2    c:IdentifiedObject.name  ?bus2 .     
      }
    ORDER BY ?pname ?tname ?enum ?bus1 ?bus1x ?bus1y ?bus2 ?bus2 ?bus2x ?bus2y 
    """
    sparql.setQuery(qstr_transformer)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'pname' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property


###############################################################################    
####################### Transformer Tank Information ##########################
###############################################################################

def query_transformer_code_rating(feeder_mrid):
    
    qstr_transformer = constant.prefix + """SELECT DISTINCT  ?pname ?tname ?enum ?ratedS ?ratedU ?conn ?ang ?res ?id
    WHERE
      {
        VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
               ?fdr    c:IdentifiedObject.mRID  ?fdrid .
        ?xft    c:TransformerTank.PowerTransformer  ?eq .
        ?eq     c:Equipment.EquipmentContainer  ?fdr .
        ?asset  c:Asset.PowerSystemResources  ?xft ;
                c:Asset.AssetInfo     ?t .
        ?p      r:type                c:PowerTransformerInfo .
        ?t      c:TransformerTankInfo.PowerTransformerInfo  ?p .
        ?e      c:TransformerEndInfo.TransformerTankInfo  ?t .
        ?p      c:IdentifiedObject.name  ?pname .
        ?t      c:IdentifiedObject.name  ?tname
        BIND(strafter(str(?t), "#") AS ?id)
        ?e  c:TransformerEndInfo.endNumber  ?enum ;
            c:TransformerEndInfo.ratedS  ?ratedS ;
            c:TransformerEndInfo.ratedU  ?ratedU ;
            c:TransformerEndInfo.r  ?res ;
            c:TransformerEndInfo.phaseAngleClock  ?ang ;
            c:TransformerEndInfo.connectionKind  ?connraw
        BIND(strafter(str(?connraw), "WindingConnection.") AS ?conn)
      }
    ORDER BY ?pname ?tname ?enum
    """
    sparql.setQuery(qstr_transformer)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'pname' in keys:
                object_name = b[keys].value + '_end_number_' + b['enum'].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
############################## Load Break Switch ##############################
###############################################################################
    
def query_load_break_switch(feeder_mrid):
    
     qstr_load_break_switch = constant.prefix + """SELECT  ?name ?id ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?rated ?breaking (GROUP_CONCAT(DISTINCT ?phs ; separator='\\n') AS ?phases) ?open ?fdrid
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
      ?s    r:type                c:LoadBreakSwitch ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?s    c:PowerSystemResource.Location ?loc .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:Switch.normalOpen   ?open
        OPTIONAL
          { ?s  c:Switch.ratedCurrent  ?rated }
        OPTIONAL
          { ?s  c:ProtectedSwitch.breakingCapacity  ?breaking }
        ?t1   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn1 ;
              c:ACDCTerminal.sequenceNumber  "1" .
        ?pt1 c:PositionPoint.Location ?loc ;
             c:PositionPoint.sequenceNumber "1" ;
    	     c:PositionPoint.xPosition ?bus1x ;
    	     c:PositionPoint.yPosition ?bus1y .  
        ?cn1  c:IdentifiedObject.name  ?bus1 .
        ?t2   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn2 ;
              c:ACDCTerminal.sequenceNumber  "2" .
        ?pt2 c:PositionPoint.Location ?loc ;
             c:PositionPoint.sequenceNumber "2" ;
    	     c:PositionPoint.xPosition ?bus2x ;
    	     c:PositionPoint.yPosition ?bus2y .
        ?cn2  c:IdentifiedObject.name  ?bus2
        BIND(strafter(str(?s), "#") AS ?id)
        OPTIONAL
          { ?swp  c:SwitchPhase.Switch  ?s ;
                  c:SwitchPhase.phaseSide1  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
      }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?rated ?breaking ?open ?id ?fdrid
    ORDER BY ?name
    """
     sparql.setQuery(qstr_load_break_switch)
     ret = sparql.query()
     Property = {}
     for b in ret.bindings:
         for keys in b:
             if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
             else:
                Property[object_name][keys] =  b[keys].value
     return Property

###############################################################################    
################################## Jumpers ####################################
###############################################################################

def query_jumpers(feeder_mrid):    
    
    qstr_jumpers = constant.prefix + """SELECT  ?name ?id ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?rated ?breaking (GROUP_CONCAT(DISTINCT ?phs ; separator='\\n') AS ?phases) ?open ?fdrid
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
      ?s    r:type                c:Jumper ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?s    c:PowerSystemResource.Location ?loc .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:Switch.normalOpen   ?open
        OPTIONAL
          { ?s  c:Switch.ratedCurrent  ?rated }
        OPTIONAL
          { ?s  c:ProtectedSwitch.breakingCapacity  ?breaking }
        ?t1   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn1 ;
              c:ACDCTerminal.sequenceNumber  "1" .
        ?pt1  c:PositionPoint.Location ?loc ;
          	  c:PositionPoint.sequenceNumber "1" ;
    	  	  c:PositionPoint.xPosition ?bus1x ;
    	  	  c:PositionPoint.yPosition ?bus1y . 
        ?cn1   c:IdentifiedObject.name  ?bus1 .
        ?t2   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn2 ;
              c:ACDCTerminal.sequenceNumber  "2" .
        ?pt2  c:PositionPoint.Location ?loc ;
          	  c:PositionPoint.sequenceNumber "2" ;
    	      c:PositionPoint.xPosition ?bus2x ;
    	      c:PositionPoint.yPosition ?bus2y .
        ?cn2  c:IdentifiedObject.name  ?bus2
        BIND(strafter(str(?s), "#") AS ?id)
        OPTIONAL
          { ?swp  c:SwitchPhase.Switch  ?s ;
                  c:SwitchPhase.phaseSide1  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
      }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?rated ?breaking ?open ?id ?fdrid
    ORDER BY ?name
    """
    sparql.setQuery(qstr_jumpers)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
################################ Reclosers ####################################
###############################################################################
    
def query_reclosers(feeder_mrid):    
    
    qstr_reclosers = constant.prefix + """SELECT  ?name ?id ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?rated ?breaking (GROUP_CONCAT(DISTINCT ?phs ; separator='\\n') AS ?phases) ?open ?fdrid
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
       ?s    r:type                c:Recloser ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?s    c:PowerSystemResource.Location ?loc .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:Switch.normalOpen   ?open
        OPTIONAL
          { ?s  c:Switch.ratedCurrent  ?rated }
        OPTIONAL
          { ?s  c:ProtectedSwitch.breakingCapacity  ?breaking }
        ?t1   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn1 ;
              c:ACDCTerminal.sequenceNumber  "1" .
        ?pt1  c:PositionPoint.Location ?loc ;
              c:PositionPoint.sequenceNumber "1" ;
    	      c:PositionPoint.xPosition ?bus1x ;
    	      c:PositionPoint.yPosition ?bus1y . 
        ?cn1  c:IdentifiedObject.name  ?bus1 .
        ?t2   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn2 ;
              c:ACDCTerminal.sequenceNumber  "2" .
        ?pt2  c:PositionPoint.Location ?loc ;
              c:PositionPoint.sequenceNumber "2" ;
    	      c:PositionPoint.xPosition ?bus2x ;
              c:PositionPoint.yPosition ?bus2y .
        ?cn2  c:IdentifiedObject.name  ?bus2
        BIND(strafter(str(?s), "#") AS ?id)
        OPTIONAL
          { ?swp  c:SwitchPhase.Switch  ?s ;
                  c:SwitchPhase.phaseSide1  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
      }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?rated ?breaking ?open ?id ?fdrid
    ORDER BY ?name
    """
    sparql.setQuery(qstr_reclosers)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
################################ Breakers #####################################
###############################################################################
    
def query_breakers(feeder_mrid):    
    
    qstr_breakers = constant.prefix + """SELECT  ?name ?id ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?rated ?breaking (GROUP_CONCAT(DISTINCT ?phs ; separator='\\n') AS ?phases) ?open ?fdrid
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
      ?s    r:type                c:Breaker ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:Switch.normalOpen   ?open
        OPTIONAL
          { ?s  c:Switch.ratedCurrent  ?rated }
        OPTIONAL
          { ?s  c:ProtectedSwitch.breakingCapacity  ?breaking }
        ?t1   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn1 ;
              c:ACDCTerminal.sequenceNumber  "1" .
        ?cn1  c:IdentifiedObject.name  ?bus1 .
        ?t2   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn2 ;
              c:ACDCTerminal.sequenceNumber  "2" .
        ?cn2  c:IdentifiedObject.name  ?bus2
        BIND(strafter(str(?s), "#") AS ?id)
        OPTIONAL
          { ?swp  c:SwitchPhase.Switch  ?s ;
                  c:SwitchPhase.phaseSide1  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
      }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?rated ?breaking ?open ?id ?fdrid
    ORDER BY ?name
    """
    sparql.setQuery(qstr_breakers)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property

###############################################################################    
################################## Fuses ######################################
###############################################################################
    
def query_fuses(feeder_mrid):
    
    qstr_fuses = constant.prefix + """SELECT  ?name ?id ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?rated ?breaking (GROUP_CONCAT(DISTINCT ?phs ; separator='\\n') AS ?phases) ?open ?fdrid
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
      ?s    r:type                c:Fuse ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?s    c:PowerSystemResource.Location ?loc .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:Switch.normalOpen   ?open
        OPTIONAL
          { ?s  c:Switch.ratedCurrent  ?rated }
        OPTIONAL
          { ?s  c:ProtectedSwitch.breakingCapacity  ?breaking }
        ?t1   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn1 ;
              c:ACDCTerminal.sequenceNumber  "1" .
     	?pt1  c:PositionPoint.Location ?loc ;
              c:PositionPoint.sequenceNumber "1" ;
    	      c:PositionPoint.xPosition ?bus1x ;
    	      c:PositionPoint.yPosition ?bus1y .  
        ?cn1  c:IdentifiedObject.name  ?bus1 .
        ?cn1  c:IdentifiedObject.name  ?bus1 .
        ?t2   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn2 ;
              c:ACDCTerminal.sequenceNumber  "2" .
        ?pt2  c:PositionPoint.Location ?loc ;
              c:PositionPoint.sequenceNumber "2" ;
    	      c:PositionPoint.xPosition ?bus2x ;
    	      c:PositionPoint.yPosition ?bus2y .
        ?cn2  c:IdentifiedObject.name  ?bus2
        BIND(strafter(str(?s), "#") AS ?id)
        OPTIONAL
          { ?swp  c:SwitchPhase.Switch  ?s ;
                  c:SwitchPhase.phaseSide1  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
      }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?rated ?breaking ?open ?id ?fdrid
    ORDER BY ?name
    """
    sparql.setQuery(qstr_fuses)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property
    
###############################################################################    
############################## Disconnectors ##################################
###############################################################################  

def query_disconnectors(feeder_mrid):
    
    qstr_disconnectors = constant.prefix + """SELECT  ?name ?id ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?basev ?rated ?breaking (GROUP_CONCAT(DISTINCT ?phs ; separator='\\n') AS ?phases) ?open ?fdrid
    WHERE
      { 
      VALUES ?fdrid """  +'{"' + str(feeder_mrid) +'"}'+"""
      ?s    r:type                c:Disconnector ;
              c:Equipment.EquipmentContainer  ?fdr .
        ?fdr  c:IdentifiedObject.mRID  ?fdrid .
        ?s    c:IdentifiedObject.name  ?name ;
              c:ConductingEquipment.BaseVoltage  ?bv .
        ?s c:PowerSystemResource.Location ?loc .
        ?bv   c:BaseVoltage.nominalVoltage  ?basev .
        ?s    c:Switch.normalOpen   ?open
        OPTIONAL
          { ?s  c:Switch.ratedCurrent  ?rated }
        OPTIONAL
          { ?s  c:ProtectedSwitch.breakingCapacity  ?breaking }
        ?t1   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn1 ;
              c:ACDCTerminal.sequenceNumber  "1" .
        ?pt1  c:PositionPoint.Location ?loc ;
              c:PositionPoint.sequenceNumber "1" ;
    	      c:PositionPoint.xPosition ?bus1x ;
    	      c:PositionPoint.yPosition ?bus1y .  
        ?cn1  c:IdentifiedObject.name  ?bus1 .
        ?t2   c:Terminal.ConductingEquipment  ?s ;
              c:Terminal.ConnectivityNode  ?cn2 ;
              c:ACDCTerminal.sequenceNumber  "2" .
        ?pt2  c:PositionPoint.Location ?loc ;
              c:PositionPoint.sequenceNumber "2" ;
    	      c:PositionPoint.xPosition ?bus2x ;
    	      c:PositionPoint.yPosition ?bus2y .
        ?cn2  c:IdentifiedObject.name  ?bus2
        BIND(strafter(str(?s), "#") AS ?id)
        OPTIONAL
          { ?swp  c:SwitchPhase.Switch  ?s ;
                  c:SwitchPhase.phaseSide1  ?phsraw
            BIND(strafter(str(?phsraw), "SinglePhaseKind.") AS ?phs)
          }
      }
    GROUP BY ?name ?basev ?bus1 ?bus1x ?bus1y ?bus2 ?bus2x ?bus2y ?rated ?breaking ?open ?id ?fdrid
    ORDER BY ?name
    """
    sparql.setQuery(qstr_disconnectors)
    ret = sparql.query()
    Property = {}
    for b in ret.bindings:
        for keys in b:
            if 'name' in keys:
                object_name = b[keys].value
                Property[object_name] =  {}
            else:
                Property[object_name][keys] =  b[keys].value
    
    return Property
    
    