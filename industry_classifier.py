import os
import re
import json
import csv
import geturls
# import get_url_industry
import pprint
import get_info
import topia_keyword_extractor
from py2neo import authenticate, Graph, Path,Node,Relationship
authenticate("localhost:7474","neo4j",",./")
graph = Graph()
#csvfile1 = open('new.csv', 'r')
#fieldnames1 = ("Sector","Industry","Keyword")
#reader1 = csv.DictReader( csvfile1, fieldnames1)

import math
import blog_crawler

fil=re.compile('.*\.json')
count=0
filename_industry={}

def get_fil_ind_dict():
	with open('url_industry_list.json',"r") as file1:
		filename_industry=json.load(file1)
		file1.close()
		return filename_industry


def files_keywords_industry(filename,key_len,level,create=0):
	with open('/home/gggopi/company data/'+filename) as currfile:
		try:
			d=json.load(currfile)
			if level==1:
				try:

					if len(d["meta_data"]["keywords"].split(','))>key_len or len(d['meta_data']['description'])>20:
						#print str(d["meta_data"]["keywords"])
						#count=count+1
						print filename
						filename=re.sub('\.json','',filename)
						filename1=re.compile(filename,re.IGNORECASE)
						level1_keywords=topia_keyword_extractor.getkeywords(str((' '.join((d["meta_data"]["keywords"].split(',')))+' '+d["meta_data"]["description"]).encode('utf-8')),1)#.split(',')
						for k in level1_keywords:
							if filename1.match(k):
								print k,'removed'
								level1_keywords.remove(k)
						indus="n/a"
						if create:
							filename_industry=get_fil_ind_dict()
							if filename in filename_industry:
								print filename_industry[filename],'mmmmmmmmmmmmmmmm'
								if not filename_industry[filename]=='n/a':
									indus= filename_industry[filename]
								else:
									return level1_keywords,"n/a"
							else:
								print "ERROR: file = " + filename+".json is not present!!"
								return "n/a","n/a"
						return level1_keywords,indus
					else:
						print "keyword len <8"
						return "n/a","n/a"
				except:
					print "aaaa"
			else:
				if len(d["about"])>key_len:
					print filename
					filename=re.sub('\.json','',filename)
					filename1=re.compile(filename,re.IGNORECASE)
					# try:
					#print str(d["about"].encode('utf-8'))
					level2_keywords=topia_keyword_extractor.getkeywords(str(d["about"].encode('utf-8')),1)
					# except UnicodeEncodeError:
					# 	pass
					for k in level2_keywords:
						if filename1.match(k):
							print k,'removed'
							level2_keywords.remove(k)
					indus='n/a'
					if create: 
						filename_industry=get_fil_ind_dict()
						if filename in filename_industry:
							if not filename_industry[filename]=='n/a':
								indus= filename_industry[filename]
							else:
								return level2_keywords,"n/a"
						else:
							print "ERROR: file = " + filename+".json is not present!!"
							return "n/a","n/a"
					return level2_keywords,indus
				else:
					print "about len < 20"
					return "n/a","n/a"
		except:
		 	print "ERROR with "+filename
		 	return 'n/a','n/a'

def create_sector__industry_graph(): 	##### To create the Sector-industry Graph.. NOTE: I have used only the sector nodes for Broad Classification. 
	fil=open('file123.json','r')
	sec_ind=json.load(fil)
	for sec in sec_ind:
		tx = graph.cypher.begin()
		tx.append("Create (n:Sector{name:'%s'})"%sec)
		tx.commit()
		for industry in sec_ind[sec]:
			try:
				print "Match (n1:Sector{name:'%s'}) Create (m:Industry{name:'%s'})-[r:`is a Subsector of`]->(n1)"%(sec,industry)
				tx = graph.cypher.begin()
				tx.append("Match (n1:Sector{name:'%s'}) Create (m:Industry{name:'%s'})-[r:`is a Subsector of`]->(n1)"%(sec,industry))
				tx.commit()
			except:
				print "Exception part:"
				print "Match (n1:Sector{name:'%s'}),(m1:Industry{name:'%s'}) Create (m1)-[r:`is a Subsector of`]->(n1)"%(sec,industry)
				tx = graph.cypher.begin()
				tx.append("Match (n1:Sector{name:'%s'}),(m1:Industry{name:'%s'}) Create (m1)-[r:`is a Subsector of`]->(n1)"%(sec,industry))
				tx.commit()


def insert_keywords_graph():		### insert keywords from 70 websites for every sector which HAS metadata 
	##### URLS FOR TRAINING  #######################################

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&industry=Capital+Goods&pagesize=500')
	
	####### Capital Goods
	#urls=['http://www.avhomesinc.com', 'http://www.aaon.com', 'http://www.aarcorp.com', 'http://www.abaxis.com', 'http://www.acceleratediagnostics.com', 'http://www.acmeunited.com', 'http://ir.wms.com', 'http://www.advancedenergy.com', 'http://www.aehr.com', 'http://www.aepinc.com', 'http://www.avinc.com', 'http://www.affymetrix.com', 'http://www.agcocorp.com', 'http://www.agilent.com', 'http://www.airindmc.com', 'http://www.airgas.com', 'http://www.alamo-group.com', 'http://www.alcoa.com', 'http://www.alliedmotion.com', 'http://www.allisontransmission.com', 'http://www.altramotion.com', 'http://www.aam.com', 'http://www.americanrailcar.com', 'http://www.ampcopittsburgh.com', 'http://www.amphenol.com', 'http://www.analogic.com', 'http://www.apog.com', 'http://www.arcgroupworldwide.com', 'http://www.arcticcat.com', 'http://www.artsway-mfg.com', 'http://www.astecindustries.com', 'http://www.astronics.com', 'http://www.spacehab.com', 'http://www.atrmholdings.com', 'http://www.avxcorp.com', 'http://www.badgermeter.com', 'http://www.bginc.com', 'http://www.beazer.com', 'http://www.belfuse.com', 'http://www.bio-rad.com', 'http://www.blount.com', 'http://www.bluelinxco.com', 'http://www.boeing.com', 'http://www.borgwarner.com', 'http://www.breeze-eastern.com', 'http://www.broadwindenergy.com', 'http://www.bruker.com', 'http://www.carboceramics.com', 'http://www.cascademicrotech.com', 'http://www.caterpillar.com', 'http://www.cecoenviro.com', 'http://www.cemex.com', 'http://www.cemtrex.com', 'http://www.centurycommunities.com', 'http://www.cepheid.com', 'http://www.cescatherapeutics.com', 'http://www.chart-ind.com', 'http://www.circor.com', 'http://www.clarcor.com', 'http://www.cdti.com', 'http://www.clearsigncombustion.com', 'http://www.coastdistribution.com', 'http://www.cognex.com', 'http://www.coherent.com', 'http://www.cohu.com', 'http://www.colfaxcorp.com', 'http://www.cmworks.com', 'http://www.combimatrix.com', 'http://www.comfortsystemsusa.com', 'http://www.cvgrp.com', 'http://www.compasstrust.com', 'http://www.compx.com', 'http://www.comstockhomes.com', 'http://www.continental-materials.com', 'http://www.control4.com', 'http://www.cpiaero.com', 'http://www.alsic.com', 'http://www.craneco.com', 'http://www.cubic.com', 'http://www.cyberoptics.com', 'http://www.drhorton.com', 'http://www.dana.com', 'http://www.danaher.com', 'http://www.dataio.com', 'http://www.deere.com', 'http://www.digipwr.com', 'http://www.donaldson.com', 'http://www.dormanproducts.com', 'http://www.douglasdynamics.com', 'http://www.drewindustries.com', 'http://www.ducommun.com', 'http://www.dxpe.com', 'http://www.dynamicmaterials.com', 'http://www.dynasil.com', 'http://www.expedit-group.com', 'http://www.easterncompany.com', 'http://www.electrosensors.com', 'http://www.emcorgroup.com', 'http://www.encorewire.com', 'http://www.ericksonaviation.com', 'http://www.espey.com', 'http://www.esterline.com', 'http://www.exfo.com', 'http://www.faro.com', 'http://www.federalsignal.com', 'http://www.federalmogul.com', 'http://www.feic.com', 'http://www.flir.com', 'http://www.flowserve.com', 'http://www.fluidigm.com', 'http://www.ford.com', 'http://www.freightcaramerica.com', 'http://www.freqelec.com', 'http://www.friedmanindustries.com', 'http://www.fuelsystemssolutions.com', 'http://www.ftek.com', 'http://www.gencor.com', 'http://www.generaldynamics.com', 'http://www.gentex.com', 'http://www.gentherm.com', 'http://www.genpt.com', 'http://www.geospace.com', 'http://www.gibraltar1.com', 'http://www.gigatronics.com', 'http://www.gbcholdings.com', 'http://www.globalpower.com', 'http://www.glbsm.com', 'http://www.gormanrupp.com', 'http://www.graco.com', 'http://www.greenbrickpartners.com', 'http://www.gbrx.com', 'http://www.griffoncorp.com', 'http://www.gulfisland.com', 'http://www.hardinge.com', 'http://www.harris.com', 'http://www.harsco.com', 'http://www.harvardbioscience.com', 'http://www.haynesintl.com', 'http://www.heico.com', 'http://www.honeywell.com', 'http://www.horseheadcorp.com', 'http://www.khov.com', 'http://www.htgmolecular.com', 'http://www.hurco.com', 'http://www.htch.com', 'http://www.hyster-yale.com', 'http://www.idexcorp.com', 'http://www.ii-vi.com', 'http://www.illumina.com', 'http://www.imagesensing.com', 'http://www.insteel.com', 'http://www.integralife.com', 'http://www.ies-co.com', 'http://www.intelsys.com', 'http://www.intest.com', 'http://www.intricon.com', 'http://www.itron.com', 'http://www.itt.com', 'http://www.ixiacom.com', 'http://www.kaiseraluminum.com', 'http://www.kbhome.com', 'http://www.kelsotech.com', 'http://www.kemet.com', 'http://www.kennametal.com', 'http://www.kewaunee.com', 'http://www.keysight.com', 'http://www.kla-tencor.com', 'http://www.beaerospace.com', 'http://www.kratosdefense.com', 'http://www.starrett.com', 'http://www.landauerinc.com', 'http://www.lear.com', 'http://www.lennoxinternational.com', 'http://www.lgihomes.com', 'http://www.lglgroup.com', 'http://www.libbey.com', 'http://www.lifetimebrands.com', 'http://www.lindsay.com', 'http://www.lmiaerospace.com', 'http://www.lockheedmartin.com', 'http://www.lydall.com', 'http://www.richmondamerican.com', 'http://www.mihomes.com', 'http://www.magna.com', 'http://www.magnetek.com', 'http://www.malibuboats.com', 'http://www.manitowoc.com', 'http://www.marineproductscorp.com', 'http://www.materion.com', 'http://www.matw.com', 'http://www.mcdermott.com', 'http://www.mrcy.com', 'http://www.meritagehomes.com', 'http://www.meritor.com', 'http://www.mesalabs.com', 'http://www.maguirepartners.com', 'http://www.methode.com', 'http://www.mfri.com', 'http://www.micronet-enertec.com', 'http://www.mvis.com', 'http://www.millerind.com', 'http://www.misonix.com', 'http://www.mksinst.com', 'http://www.mobilemini.com', 'http://www.mocon.com', 'http://www.modine.com', 'http://www.motorcarparts.com', 'http://www.mrcglobal.com', 'http://www.mscdirect.com', 'http://www.mts.com', 'http://www.muellerindustries.com', 'http://www.muellerwaterproducts.com', 'http://www.nanometrics.com', 'http://www.gopresto.com', 'http://www.navistar.com', 'http://www.ncilp.com', 'http://www.newport.com', 'http://www.nnbr.com', 'http://www.nordson.com', 'http://www.norsat.com', 'http://www.nortechsys.com', 'http://www.ntic.com', 'http://www.northropgrumman.com', 'http://www.nvrinc.com', 'http://www.omegaflex.com', 'http://www.orbitalatk.com', 'http://www.oshkoshcorporation.com', 'http://www.owenscorning.com', 'http://www.paccar.com', 'http://www.pacificbiosciences.com', 'http://www.pall.com', 'http://www.phstock.com', 'http://www.pkoh.com', 'http://www.perceptron.com', 'http://www.perkinelmer.com', 'http://www.pgtindustries.com', 'http://www.planar.com', 'http://www.peerlessmfg.com', 'http://www.polaris.com', 'http://www.protolabs.com', 'http://www.psivida.com', 'http://www.pultegroupinc.com', 'http://www.quanex.com', 'http://www.quantaservices.com', 'http://www.qtww.com', 'http://www.ravenind.com', 'http://www.raytheon.com', 'http://www.rbcbearings.com', 'http://www.remyinc.com', 'http://www.rfindustries.com', 'http://www.rockwellautomation.com', 'http://www.rockwellcollins.com', 'http://www.rokabio.com', 'http://www.roperind.com', 'http://www.rtiintl.com', 'http://www.rudolphtech.com', 'http://www.ryland.com', 'http://www.schmitt-ind.com', 'http://www.sequenom.com', 'http://www.servotronics.com', 'http://www.shiloh.com' ]

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&industry=Finance&pagesize=500')
	
	####### Finance
	#urls=['http://www.1347capital.com', 'http://www.1347pih.com', 'http://www.1stcenturybank.com', 'http://www.1stconstitution.com', 'http://www.1stsource.com', 'http://www.abm.com', 'http://www.accessnationalbank.com', 'http://www.acnb.com', 'http://www.amg.com', 'http://www.aflac.com', 'http://www.alexanderbaldwin.com', 'http://www.alleghany.com', 'http://www.allianceanytime.com', 'http://www.alliancecapital.com', 'http://www.allianzinvestors.com', 'http://www.allstate.com', 'http://www.ally.com', 'http://www.altisourceamc.com', 'http://www.altisourceresi.com', 'http://www.ambac.com', 'http://www.ameriana.com', 'http://www.ataxfund.com', 'http://www.americanapparel.net', 'http://www.american-equity.com', 'http://www.americanexpress.com', 'http://www.afginc.com', 'http://www.americanindependencecorp.com', 'http://www.aig.com', 'http://www.amnb.com', 'http://www.anico.com', 'http://www.amrealtytrust.com', 'http://www.ameriprise.com', 'http://www.amerisafe.com', 'http://www.amesnational.com', 'http://www.amtrustgroup.com', 'http://www.anchornetbank.com', 'http://www.anchorbank.com', 'http://www.aon.com', 'http://www.acptrust.com', 'http://www.arcapitalacquisitioncorp.com', 'http://www.arlingtonasset.com', 'http://www.armadahoffler.com', 'http://www.arrowfinancial.com', 'http://www.ajg.com', 'http://www.artisanpartners.com', 'http://www.ashevillesavingsbank.com', 'http://www.associatedbank.com', 'http://www.assurant.com', 'http://www.astafunding.com', 'http://www.astoriabank.com', 'http://www.athensfederal.com', 'http://www.atlam.com', 'http://www.atlanticcoastbank.net', 'http://www.atlanticus.com', 'http://www.atlas-fin.com', 'http://www.auburnbank.com', 'http://www.avenuenashville.com', 'http://www.baldwinandlyons.com', 'http://www.bancfirst.com', 'http://www.bonj.net', 'http://www.bancorpsouth.com', 'http://www.bankmutualcorp.com', 'http://www.bankofamerica.com', 'http://www.bankofcommerceholdings.com', 'http://www.boh.com', 'http://www.bankofmarin.com', 'http://www.bankofny.com', 'http://www.scotiabank.ca', 'http://www.banksc.com', 'http://www.bankofthejames.com', 'http://www.bankozarks.com', 'http://www.bankfinancial.com', 'http://www.bankofnewcanaan.com', 'http://www.banrbank.com', 'http://www.bhbt.com', 'http://www.baybankmd.com', 'http://www.baylake.com', 'http://www.bbandt.com', 'http://www.bbcnbank.com', 'http://www.bbxcapital.com', 'http://www.bcbbancorp.com', 'http://www.ffbh.com', 'http://www.berkshirebank.com', 'http://www.bgcpartners.com', 'http://www.blackhawknetwork.com', 'http://www.blackrock.com', 'http://www.bncbancorp.com', 'http://www.bofiholding.com', 'http://www.bokf.com', 'http://www.bostonprivate.com', 'http://www.broadwayfed.com', 'http://www.bbinsurance.com', 'http://www.bmtc.com', 'http://www.belmontsavings.com', 'http://www.cffc.com', 'http://www.c1bank.com', 'http://www.calamos.com', 'http://www.calfirstbancorp.com', 'http://www.cambridgecapital.com', 'http://www.camdennational.com', 'http://www.campuscrest.com', 'http://www.cibc.com', 'http://www.capesb.com', 'http://www.ccbg.com', 'http://www.capitalone.com', 'http://www.capfed.com', 'http://www.cardinalbank.com', 'http://www.carolinabank.com', 'http://www.carverbank.com', 'http://www.botc.com', 'http://www.catamaranrx.com', 'http://www.cathaybank.com', 'http://www.cboe.com', 'http://www.cbre.com', 'http://www.centerstatebank.com', 'http://www.cfbankonline.com', 'http://www.cvcb.com', 'http://www.centurybank.com', 'http://www.charterbank.net', 'http://www.chemicalbankmi.com', 'http://www.cheviotsavings.com', 'http://www.chicopeesavings.com', 'http://www.chubb.com', 'http://www.cifc.com', 'http://www.cit.com', 'http://www.ccf.us', 'http://www.citizensbank.com', 'http://www.citizensfirstbank.com', 'http://www.citizensholdingcompany.com', 'http://www.citizensinc.com', 'http://www.cnb.com', 'http://www.fcza.com', 'http://www.cliftonsavings.com', 'http://www.cmegroup.com', 'http://www.cna.com', 'http://www.bankcnb.com', 'http://www.cnoinc.com', 'http://www.cobizbank.com', 'http://www.peoplesbanknet.com', 'http://www.cohenandsteers.com', 'http://www.firstservice.com', 'http://www.colonybankcorp.com', 'http://www.columbiabank.com', 'http://www.comerica.com', 'http://www.commercebank.com', 'http://www.communitybankna.com', 'http://www.cbtrustcorp.com', 'http://www.ctbi.com', 'http://www.communitywest.com', 'http://www.community1.com', 'http://www.consolidatedtomoka.com', 'http://www.consumerportfolio.com', 'http://www.corvel.com', 'http://www.cowen.com', 'http://www.centralpacificbank.com']

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Energy')
	##### Energy
	#urls=['http://www.abraxaspetroleum.com', 'http://www.adamsresources.com', 'http://www.advantageog.com', 'http://www.ahgp.com', 'http://www.arlp.com', 'http://www.alonusa.com', 'http://www.alonpartners.com', 'http://www.alphanr.com', 'http://www.americandg.com', 'http://www.aeti.com', 'http://www.anadarko.com', 'http://www.apachecorp.com', 'http://www.approachresources.com', 'http://www.archcoal.com', 'http://www.atlasamerica.com', 'http://www.atlasresourcepartners.com', 'http://www.atwd.com', 'http://www.bakerhughes.com', 'http://www.ballard.com', 'http://www.brninc.com', 'http://www.basware.com', 'http://www.bellatrixexploration.com', 'http://www.billbarrettcorp.com', 'http://www.bkep.com', 'http://www.bonanzacrk.com', 'http://www.bnymellon.com', 'http://www.breitburn.com', 'http://www.briggsandstratton.com', 'http://www.brunswick.com', 'http://www.buckeye.com', 'http://www.cjenergy.com', 'http://www.cabotog.com', 'http://www.callon.com', 'http://www.calumetspecialty.com', 'http://www.c-a-m.com', 'http://www.cnrl.com', 'http://www.capstoneturbine.com', 'http://www.crzo.net', 'http://www.cenovus.com', 'http://www.chk.com', 'http://www.chkgranitewashtrust.com', 'http://www.chevron.com', 'http://www.cimarex.com', 'http://www.ckxlands.com', 'http://www.claytonwilliams.com', 'http://www.cloudpeakenergy.com', 'http://www.cobaltintl.com', 'http://www.comstockresources.com', 'http://www.conchoresources.com', 'http://www.conocophillips.com', 'http://www.consolenergy.com', 'http://www.contango.com', 'http://www.contres.com', 'http://www.crosstimberstrust.com', 'http://www.crossamericapartners.com', 'http://www.compressco.com', 'http://www.cummins.com', 'http://www.coffeyvillegroup.com', 'http://www.cvrrefining.com', 'http://www.dakotaplains.com', 'http://www.dawson3d.com', 'http://www.dejour.com', 'http://www.deleklogistics.com', 'http://www.mapcoexpress.com', 'http://www.denbury.com', 'http://www.devonenergy.com', 'http://www.diamondoffshore.com', 'http://www.diamondbackenergy.com', 'http://www.dom-dominion.com', 'http://www.dmlp.net', 'http://www.dril-quip.com', 'http://www.eaglerockenergy.com', 'http://www.earthstoneenergy.com', 'http://www.eclipseresources.com', 'http://www.ecostim-es.com', 'http://www.emeraldoil.com', 'http://www.emergelp.com', 'http://www.emerson.com', 'http://www.enbridgemanagement.com', 'http://www.enbridge.com', 'http://www.encana.com', 'http://www.enduroroyaltytrust.com', 'http://www.energen.com', 'http://www.enerjex.com', 'http://www.enerplus.com', 'http://www.enservco.com', 'http://www.eogresources.com', 'http://www.enterprisegp.com', 'http://www.eqt.com', 'http://www.erinenergy.com', 'http://www.escaleraresources.com', 'http://www.evenergypartners.com', 'http://www.evolutionpetroleum.com', 'http://www.exxonmobil.com', 'http://www.fppcorp.com', 'http://www.fmctechnologies.com', 'http://www.forbesenergyservices.com', 'http://www.foresight.com', 'http://www.f-e-t.com', 'http://www.fxenergy.com', 'http://www.gastar.com', 'http://www.ge.com', 'http://www.genesisenergy.com', 'http://www.globalp.com', 'http://www.glorienergy.com', 'http://www.goodrichpetroleum.com', 'http://www.graftech.com', 'http://www.grantierra.com', 'http://www.gulfmark.com', 'http://www.gulfportenergy.com', 'http://www.halconresources.com', 'http://www.halladorenergy.com', 'http://www.halliburton.com', 'http://www.harvestnr.com', 'http://www.helixesg.com', 'http://www.hpinc.com', 'http://www.herculesoffshore.com', 'http://www.hess.com', 'http://www.hollyenergy.com', 'http://www.hollyfrontier.com', 'http://www.houstonamericanenergy.com', 'http://www.hugotontrust.com', 'http://www.ielp.com', 'http://www.idealpower.com', 'http://www.imperialoil.ca', 'http://www.iongeo.com', 'http://www.isramcousa.com', 'http://www.jonesenergy.com', 'http://www.jpenergypartners.com', 'http://www.keyenergy.com', 'http://www.laredopetro.com', 'http://www.legacylp.com', 'http://www.lilisenergy.com', 'http://www.linnco.com', 'http://www.linnenergy.com', 'http://www.lrrenergy.com', 'http://www.lucasenergy.com', 'http://www.macquarie.com', 'http://www.magellanlp.com', 'http://www.magellanpetroleum.com', 'http://www.magnumhunterresources.com', 'http://www.marathonoil.com', 'http://www.marathonpetroleum.com', 'http://www.marps-marinepetroleumtrust.com', 'http://www.markwest.com', 'http://www.martinmidstream.com', 'http://www.matadorresources.com', 'http://www.memorialpp.com', 'http://www.memorialrd.com', 'http://www.mexcoenergy.com', 'http://www.mgeenergy.com', 'http://www.midconenergypartners.com', 'http://www.midstatespetroleum.com', 'http://www.millerenergyresources.com', 'http://www.mplx.com', 'http://www.murphyoilcorp.com', 'http://www.nov.com', 'http://www.ngsgi.com', 'http://www.nrplp.com', 'http://www.newconceptenergy.com', 'http://www.newsource.com', 'http://www.newfld.com', 'http://www.newpark.com', 'http://www.nglenergypartners.com', 'http://www.nobleenergyinc.com', 'http://www.nacg.ca', 'http://www.neort.com', 'http://www.northernoil.com', 'http://www.ntenergy.com', 'http://www.nustarenergy.com', 'http://www.nustargpholdings.com', 'http://www.nuverra.com', 'http://www.oasispetroleum.com', 'http://www.oxy.com', 'http://www.oceaneering.com', 'http://www.oilstatesintl.com', 'http://www.pacificcoastoiltrust.com', 'http://www.panhandleoilandgas.com', 'http://www.par-petro.com', 'http://www.paragonoffshore.com', 'http://www.parkerdrilling.com', 'http://www.patenergy.com', 'http://www.pbfenergy.com', 'http://www.pdce.com', 'http://www.peabodyenergy.com', 'http://www.pacificenergydevelopment.com', 'http://www.pengrowth.com', 'http://www.pennvirginia.com', 'http://www.pbt-permianbasintrust.com', 'http://www.phillips66.com', 'http://www.phillips66partners.com', 'http://www.pioneeres.com', 'http://www.pxd.com', 'http://www.paalp.com', 'http://www.plugpower.com', 'http://www.pstr.com', 'http://www.psiengines.com', 'http://www.precisiondrilling.com', 'http://www.primeenergy.com', 'http://www.profireenergy.com', 'http://www.qepres.com', 'http://www.rangeresources.com', 'http://www.resoluteenergy.com', 'http://www.rexenergy.com', 'http://www.rhinolp.com', 'http://www.ringenergy.com', 'http://www.rrmidstream.com', 'http://www.rosettaresources.com', 'http://www.rowancompanies.com', 'http://www.royl.com', 'http://www.rpc.net', 'http://www.sbr-sabineroyalty.com', 'http://www.saexploration.com', 'http://www.samsonoilandgas.com', 'http://www.sjbrt.com', 'http://www.sanchezenergycorp.com', 'http://www.sanchezproductionpartners.com', 'http://www.sandridgeenergy.com', 'http://www.perotsystems.com', 'http://www.sevcon.com', 'http://www.77nrg.com', 'http://www.shellmidstreampartners.com', 'http://www.sm-energy.com', 'http://www.swn.com', 'http://www.stoneenergy.com', 'http://www.suncor.com', 'http://www.sunocologistics.com', 'http://www.sunocolp.com', 'http://www.superiorenergy.com', 'http://www.swiftenergy.com', 'http://www.syrginfo.com', 'http://www.tengasco.com', 'http://www.tescocorp.com', 'http://www.tesoropetroleum.com', 'http://www.tesorologistics.com', 'http://www.tetratec.com', 'http://www.tpltrust.com', 'http://www.thermon.com', 'http://www.torchlightenergy.com', 'http://www.trans-globe.com', 'http://www.transmontaignepartners.com.', 'http://www.trecora.com', 'http://www.trianglepetroleum.com', 'http://www.usnrg.com', 'http://www.ultrapetroleum.com', 'http://www.unitcorp.com', 'http://www.vaalco.com', 'http://www.valero.com', 'http://www.vnrllc.com', 'http://www.vantagedrilling.com', 'http://www.vermilionenergy.com', 'http://www.vertexenergy.com', 'http://www.viperenergy.com', 'http://www.wtoffshore.com', 'http://www.walterenergy.com', 'http://www.warrenresources.com', 'http://www.wnr.com', 'http://www.westmoreland.com', 'http://www.westport.com', 'http://www.whiting.com', 'http://www.willbros.com', 'http://www.woodward.com', 'http://www.wfscorp.com', 'http://www.wpxenergy.com', 'http://www.yumaenergyinc.com', 'http://www.zazaenergy.com', 'http://www.zionoil.com']

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Health+Care')
	#### Health Care
	#urls=['http://www.3m.com', 'http://www.americanaddictioncenters.com', 'http://www.abbott.com', 'http://www.abbvie.com', 'http://www.plasmatechbio.com', 'http://www.abiomed.com', 'http://www.acadiahealthcare.com', 'http://www.acadia-pharm.com', 'http://www.acastipharma.com', 'http://www.acceleronpharma.com', 'http://www.accuray.com', 'http://www.acelrx.com', 'http://www.aceto.com', 'http://www.achaogen.com', 'http://www.achillion.com', 'http://www.acorda.com', 'http://www.actiniumpharmaceuticals.com', 'http://www.acurapharm.com', 'http://www.adamaspharma.com', 'http://www.adamispharmaceuticals.com', 'http://www.adcarehealth.com', 'http://www.addus.com', 'http://www.adhc.com', 'http://www.admabiologics.com', 'http://www.aduro.com', 'http://www.advaxis.com', 'http://www.aegerion.com', 'http://www.aeriepharma.com', 'http://www.aezsinc.com', 'http://www.aetna.com', 'http://www.agenusbio.com', 'http://www.agiletherapeutics.com', 'http://www.agios.com', 'http://www.akebia.com', 'http://www.akersbiosciences.com', 'http://www.akorn.com', 'http://www.amriglobal.com', 'http://www.alderbio.com', 'http://www.aldeyra.com', 'http://www.alere.com', 'http://www.alexionpharm.com', 'http://www.alexza.com', 'http://www.aligntech.com', 'http://www.alimerasciences.com', 'http://www.actavis.com', 'http://www.allianceimaging.com', 'http://www.alliedhpi.com', 'http://www.alliqua.com', 'http://www.almostfamily.com', 'http://www.alnylam.com', 'http://www.alphaprotech.com', 'http://www.alphatecspine.com', 'http://www.amagpharma.com', 'http://www.amedica.com', 'http://www.amedisys.com', 'http://www.americancaresource.com', 'http://www.as-e.com', 'http://www.ashs.com', 'http://www.amerisourcebergen.net', 'http://www.amgen.com', 'http://www.amicusrx.com', 'http://www.amphastar.com', 'http://www.ampiopharma.com', 'http://www.amsurg.com', 'http://www.anacor.com', 'http://www.angiodynamics.com', 'http://www.anipharmaceuticals.com', 'http://www.anikatherapeutics.com', 'http://www.antarespharma.com', 'http://www.wellpoint.com', 'http://www.acunetx.com', 'http://www.anthera.com', 'http://www.aoxingpharma.com', 'http://www.agtc.com', 'http://www.apricusbio.com', 'http://www.aptose.com', 'http://www.aqxpharma.com', 'http://www.aradigm.com', 'http://www.aratana.com', 'http://www.arcabiopharma.com', 'http://www.ardelyx.com', 'http://www.arenapharm.com', 'http://www.argostherapeutics.com', 'http://www.ariad.com', 'http://www.arqule.com', 'http://www.arraybiopharma.com', 'http://www.arthrt.com', 'http://www.arrowheadresearch.com', 'http://www.assemblybio.com', 'http://asteriasbiotherapeutics.com', 'http://www.atarabio.com', 'http://www.athersys.com', 'http://www.atossagenetics.com', 'http://www.atricure.com', 'http://www.atrioncorp.com', 'http://www.atyrpharma.com', 'http://www.auriniapharma.com', 'http://www.avalanchebiotech.com', 'http://www.aveooncology.com', 'http://www.avinger.com', 'http://www.axogeninc.com', 'http://www.baxter.com', 'http://www.bd.com', 'http://www.bellerophon.com', 'http://www.bellicum.com', 'http://www.bg-medicine.com', 'http://www.bindtherapeutics.com', 'http://www.basinc.com', 'http://www.biocept.com', 'http://www.biocryst.com', 'http://www.biodel.com', 'http://www.bdsi.com', 'http://www.biogenidec.com', 'http://www.biolase.com', 'http://www.biolifesolutions.com', 'http://www.bmrn.com', 'http://www.bioreference.com', 'http://www.bioscrip.com', 'http://www.biospecifics.com', 'http://www.biotapharma.com', 'http://www.bio-techne.com', 'http://www.biotelinc.com', 'http://www.biotimeinc.com', 'http://www.perfectteeth.com', 'http://www.bluebirdbio.com', 'http://www.blueprintmedicines.com/', 'http://www.bostonscientific.com', 'http://www.boviemedical.com', 'http://www.brainstorm-cell.com', 'http://www.bms.com', 'http://www.brookdale.com', 'http://www.crbard.com', 'http://www.caladrius.com', 'http://www.calithera.com', 'http://www.cambrex.com', 'http://www.cancergenetics.com', 'http://www.cantelmedical.com', 'http://www.capitalsenior.com', 'http://www.capnia.com', 'http://capricor.com', 'http://www.caratherapeutics.com', 'http://www.carbylan.com', 'http://www.cardica.com', 'http://www.cardinal.com', 'http://www.cardiome.com', 'http://www.csi360.com', 'http://www.xdx.com', 'http://www.casmed.com', 'http://www.casipharmaceuticals.com', 'http://www.catabasis.com', 'http://www.catalent.com', 'http://www.catalystpharma.com', 'http://www.celatorpharma.com', 'http://www.celgene.com', 'http://www.celladon.net', 'http://www.celldex.com', 'http://www.cellectar.com', 'http://www.cellbiomedgroup.com', 'http://www.cel-sci.com', 'http://www.celsion.com', 'http://www.celsustx.com', 'http://www.cempra.com', 'http://www.centene.com', 'http://www.ceruleanrx.com', 'http://www.cerus.com', 'http://www.criver.com', 'http://www.chembio.com', 'http://www.chemed.com', 'http://www.chemocentryx.com', 'http://www.chimerix.com', 'http://www.cidara.com', 'http://www.cigna.com', 'http://www.cipherpharma.com', 'http://www.thementornetwork.com', 'http://www.cbiolabs.com', 'http://www.clovisoncology.com', 'http://www.cogentixmedical.com', 'http://www.coherus.com', 'http://collegiumpharma.com', 'http://www.colucid.com']


	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Technology')
	######  Technology
	#urls=['http://www.2u.com', 'http://www.aaronrents.com', 'http://www.aciworldwide.com', 'http://www.activisionblizzard.com', 'http://www.actua.com', 'http://www.actuant.com', 'http://www.acxiom.com', 'http://www.adept.com', 'http://www.adobe.com', 'http://www.amd.com', 'http://www.advent.com', 'http://www.aerocentury.com', 'http://www.wellsgardner.com', 'http://www.agilysys.com', 'http://www.airleasecorp.com', 'http://www.aircastle.com', 'http://www.alarm.com', 'http://www.afop.com', 'http://www.allscripts.com', 'http://www.altera.com', 'http://www.amaya.com', 'http://www.ambarella.com', 'http://www.amsoftware.com', 'http://www.amkor.com', 'http://www.amnhealthcare.com', 'http://www.amtechsystems.com', 'http://www.anadigics.com', 'http://www.analog.com', 'http://www.ansys.com', 'http://www.apitech.com', 'http://www.apigee.com', 'http://www.appfolioinc.com', 'http://www.apple.com', 'http://www.appliedmaterials.com', 'http://www.apm.com', 'http://www.ao-inc.com', 'http://www.arinet.com', 'http://www.arrisi.com', 'http://www.ascentsolar.com', 'http://www.aspentech.com', 'http://www.astro-medinc.com', 'http://www.asuresoftware.com', 'http://www.atmel.com', 'http://www.authentidate.com', 'http://www.autobytel.com', 'http://www.autodesk.com', 'http://www.adp.com', 'http://www.aviatnetworks.com', 'http://www.aware.com', 'http://www.axcelis.com', 'http://www.axt.com', 'http://www.barrettbusiness.com', 'http://www.bazaarvoice.com', 'http://www.bench.com', 'http://www.benefitfocus.com', 'http://www.bgstaffing.com', 'http://www.blackbox.com', 'http://www.blackbaud.com', 'http://www.blondertongue.com', 'http://www.blucora.com', 'http://www.bottomline.com', 'http://www.seacubecontainer.com', 'http://www.bridgelinesw.com', 'http://www.brightcove.com', 'http://www.broadcom.com', 'http://www.broadsoft.com', 'http://www.broadvision.com', 'http://www.brocade.com', 'http://www.brooks.com', 'http://www.ca.com', 'http://www.cabotcmp.com', 'http://www.caci.com', 'http://www.cadence.com', 'http://www.capps.com', 'http://www.calamp.com', 'http://www.callidussoftware.com', 'http://www.carbonite.com', 'http://www.cavium.com', 'http://www.cdicorp.com', 'http://www.celestica.com', 'http://www.cerner.com', 'http://www.ceva-dsp.com', 'http://www.channeladvisor.com', 'http://www.chicagorivet.com', 'http://www.ciber.com', 'http://www.cirrus.com', 'http://www.cisco.com', 'http://www.citrix.com', 'http://www.cogentco.com', 'http://www.cognizant.com', 'http://www.collabrx.com', 'http://www.commscope.com', 'http://www.commvault.com', 'http://www.cpsinet.com', 'http://www.csc.com', 'http://www.ctg.com', 'http://www.comtechtel.com', 'http://www.ccur.com', 'http://www.connecture.com', 'http://www.constantcontact.com', 'http://www.convergys.com', 'http://www.corelogic.com', 'http://www.cornerstoneondemand.com', 'http://www.counterpath.com', 'http://www.covisint.com', 'http://www.cray.com', 'http://www.cree.com', 'http://www.crossroads.com', 'http://www.csgi.com', 'http://www.cspi.com', 'http://www.ctscorp.com', 'http://www.curtisswright.com', 'http://www.cvdequipment.com', 'http://www.cyaninc.com', 'http://www.cypress.com', 'http://www.cyren.com', 'http://www.daegis.com', 'http://www.datalink.com', 'http://www.dataram.com', 'http://www.datawatch.com', 'http://www.dealertrack.com', 'http://www.demandmedia.com', 'http://www.demandware.com', 'http://www.digi.com', 'http://www.digimarc.com', 'http://www.digitalallyinc.com', 'http://www.diodes.com', 'http://www.dlhcorp.com', 'http://www.documentsecurity.com', 'http://www.dolby.com', 'http://www.dothill.com', 'http://www.dovercorporation.com', 'http://www.dspg.com', 'http://www.dstsystems.com', 'http://www.earthlink.net']

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Public+Utilities')
	######### Public Utilities
	#urls=['http://www.8point3energypartners.com', 'http://www.8x8.com', 'http://www.activepower.com', 'http://www.adtran.com', 'http://www.alaskacommunications.com', 'http://www.allete.com', 'http://www.alliantenergy.com', 'http://www.wvtc.com', 'http://www.americamovil.com', 'http://www.aep.com', 'http://www.americanmidstream.com', 'http://www.aswater.com', 'http://www.amwater.com', 'http://www.americangreetings.com', 'http://www.artesianwater.com', 'http://www.att.com', 'http://www.atni.com', 'http://www.atmosenergy.com', 'http://www.avalonholdings.com', 'http://www.avistacorp.com', 'http://www.marlinmidstream.com', 'http://www.bce.ca', 'http://www.blackhillscorp.com', 'http://www.blackberry.com', 'http://www.blueearthinc.com', 'http://www.bwpmlp.com', 'http://www.cadizinc.com', 'http://www.casella.com', 'http://www.centerpointenergy.com', 'http://www.centurylink.com', 'http://www.cheniereenergypartners.com', 'http://www.cheniere.com', 'http://www.chpk.com', 'http://www.ciena.com', 'http://www.cincinnatibell.com', 'http://www.cleanenergyfuels.com', 'http://www.clearfieldconnection.com', 'http://www.clearone.com', 'http://www.cleco.com', 'http://www.cmsenergy.com', 'http://www.commsystems.com', 'http://www.conemidstream.com', 'http://www.ctwater.com', 'http://www.conedison.com', 'http://www.dcppartners.com', 'http://www.deltagas.com', 'http://www.dommidstream.com', 'http://www.dom.com', 'http://www.dragonwaveinc.com', 'http://www.dteenergy.com', 'http://www.duke-energy.com', 'http://www.dynegy.com', 'http://www.edison.com', 'http://www.epelectric.com', 'http://www.elephanttalk.com', 'http://www.empiredistrict.com', 'http://www.energytransfer.com', 'http://www.enlink.com', 'http://www.entergy.com', 'http://www.epplp.com', 'http://www.eqtmidstreampartners.com', 'http://www.equinix.com', 'http://www.exeloncorp.com', 'http://www.exterran.com', 'http://www.fairpoint.com', 'http://www.firstenergycorp.com', 'http://www.frontier.com', 'http://www.fusiontel.com', 'http://www.ewst.com', 'http://www.gci.com', 'http://www.genie.com', 'http://www.glowpoint.com', 'http://www.gtt.net', 'http://www.hei.com', 'http://www.hc2.com', 'http://www.idacorpinc.com', 'http://www.idt.net', 'http://www.ikanos.com', 'http://www.crestwoodlp.com', 'http://www.infinera.com', 'http://www.inteliquent.com', 'http://www.inventergy.com', 'http://www.itc-holdings.com', 'http://www.kne.com', 'http://www.thelacledegroup.com', 'http://www.level3.com', 'http://www.lumosnetworks.com', 'http://www.middlesexwater.com', 'http://www.netgear.com', 'http://www.njresources.com', 'http://www.nexteraenergypartners.com', 'http://www.nexteraenergy.com', 'http://www.niskapartners.com', 'http://www.nisource.com', 'http://www.northwesternenergy.com', 'http://www.nrgyield.com', 'http://www.ntelos.com', 'http://www.oceanpowertechnologies.com', 'http://www.oge.com', 'http://www.oneokpartners.com', 'http://www.oneok.com', 'http://www.ormat.com', 'http://www.otelcoinc.com', 'http://www.ottertail.com', 'http://www.pdvcorp.com', 'http://www.pgecorp.com', 'http://www.patternenergy.com', 'http://www.penntex.com', 'http://www.pepcoholdings.com', 'http://www.piedmontng.com', 'http://www.pinnaclewest.com', 'http://www.plantronics.com', 'http://www.pnmresources.com', 'http://www.polycom.com', 'http://www.pplweb.com', 'http://www.pseg.com', 'http://www.purecyclewater.com', 'http://www.questar.com', 'http://www.commscope.com', 'http://www.centex.com', 'http://www.citycon.fi', 'http://www.republicservices.com', 'http://www.rgcresources.com', 'http://www.scana.com', 'http://www.sempra.com', 'http://www.shentel.com', 'http://www.shoretel.com', 'http://www.sjwater.com', 'http://www.solar3d.com', 'http://www.sjindustries.com', 'http://www.stanleyassociates.com', 'http://www.southerncompany.com', 'http://www.swgas.com', 'http://www.sparkenergy.com', 'http://www.spectraenergy.com', 'http://www.spectraenergypartners.com', 'http://www.spok.com', 'http://www.sprint.com', 'http://spathinc.com', 'http://www.summitmidstream.com', 'http://www.tallgrassenergy.com', 'http://www.targaresources.com', 'http://www.tecoenergy.com', 'http://www.tdsinc.com', 'http://www.telus.com', 'http://www.tva.gov', 'http://www.terraform.com', 'http://www.yorkwater.com', 'http://www.t-mobile.com', 'http://www.transalta.com', 'http://www.transcanada.com', 'http://www.usgeothermal.com', 'http://www.ugicorp.com', 'http://www.uil.com', 'http://www.uscellular.com', 'http://www.unitil.com', 'http://www.usecology.com', 'http://www.usacpartners.com', 'http://www.vectren.com', 'http://www.verizon.com', 'http://www.vonage.com', 'http://www.wasteconnections.com', 'http://www.wm.com', 'http://www.wisconsinenergy.com', 'http://www.westell.com', 'http://www.westerngas.com', 'http://www.wglholdings.com', 'http://www.williams.com', 'http://co.williams.com', 'http://www.windstream.com', 'http://www.xcelenergy.com', 'http://www.zbbenergy.com', 'http://www.zhone.com']

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Consumer+Services')
	###### Consumer Services
	#urls=['http://www.1800flowers.com', 'http://www.6dglobal.com', 'http://www.ahbelo.com', 'http://www.abercrombie.com', 'http://www.acadiarealty.com', 'http://www.acornenergy.com', 'http://www.acrerealtyinvestors.com', 'http://www.addvantagetech.com', 'http://www.adt.com', 'http://www.advanceautoparts.com', 'http://www.aecom.com', 'http://www.aeropostale.com', 'http://www.agreerealty.com', 'http://www.alx-inc.com', 'http://www.labspace.com', 'http://www.allegion.com', 'http://www.aointl.com', 'http://www.amazon.com', 'http://www.ambassadorsgroup.com', 'http://www.amcnetworks.com', 'http://www.amerco.com', 'http://www.americanassetstrust.com', 'http://www.americancampus.com', 'http://www.agnc.com', 'http://www.mtge.com', 'http://www.ae.com', 'http://www.americanpubliceducation.com', 'http://www.arcpreit.com', 'http://www.americanresidentialproperties.com', 'http://www.americantower.com', 'http://www.amerigas.com', 'http://www.amrepcorp.com', 'http://www.angieslist.com', 'http://www.anncareers.com', 'http://www.annaly.com', 'http://www.anworth.com', 'http://www.aimco.com', 'http://www.apolloreit.com', 'http://www.apollogrp.edu', 'http://www.apolloresidentialmortgage.com', 'http://www.arcainc.com', 'http://www.adnas.com', 'http://www.arborrealtytrust.com', 'http://www.e-arc.com', 'http://www.arescre.com', 'http://www.arkrestaurants.com', 'http://www.armourreit.com', 'http://www.dressbarn.com', 'http://www.ascentcapitalgroupinc.com', 'http://www.ahpreit.com', 'http://www.ahtreit.com', 'http://www.ashfordinc.com', 'http://www.aerogel.com', 'http://www.associatedestates.com', 'http://www.autozone.com', 'http://www.avalonbay.com', 'http://www.avisbudgetgroup.com', 'http://www.barnesandnobleinc.com', 'http://www.beaconroofingsupply.com', 'http://www.bbgi.com', 'http://www.bedbathandbeyond.com', 'http://www.bestbuy.com', 'http://www.big5sportinggoods.com', 'http://www.biglots.com', 'http://www.biglariholdings.com', 'http://www.biomedrealty.com', 'http://www.biopathholdings.com', 'http://www.birksgroup.com', 'http://www.bjsbrewhouse.com', 'http://www.bloominbrands.com', 'http://www.bluenile.com', 'http://www.bobevans.com', 'http://www.boingo.com', 'http://www.bc.com', 'http://www.bojangles.com', 'http://www.booksamillioninc.com', 'http://www.lacrossefootwear.com', 'http://www.boozallen.com', 'http://www.bostonproperties.com', 'http://www.boydgaming.com', 'http://www.brandywinerealty.com', 'http://www.bbrg.com', 'http://www.bridgepointeducation.com', 'http://www.brinker.com', 'http://www.brookfield.com', 'http://www.brookfieldproperties.com', 'http://www.brtrealty.com', 'http://www.buckle.com', 'http://www.buffalowildwings.com', 'http://www.buildabear.com', 'http://www.bldr.com', 'http://www.cabelas.com', 'http://www.cablevision.com', 'http://www.caesarsacquisitioncompany.com', 'http://www.caesars.com', 'http://www.cafepress.com', 'http://www.calix.com', 'http://www.cambiumlearning.com', 'http://www.camdenliving.com', 'http://www.canterburypark.com', 'http://www.capellauniversity.com', 'http://www.capitolacquisition.com', 'http://www.capstead.com', 'http://www.careered.com', 'http://www.caretrustreit.com', 'http://www.carmike.com', 'http://www.carnivalcorp.com', 'http://www.carnivalplc.com', 'http://www.carriageservices.com', 'http://www.carrols.com', 'http://www.cartesian.com', 'http://www.cashamerica.com', 'http://www.catchmark.com', 'http://www.catocorp.com', 'http://www.cblproperties.com', 'http://www.cbscorporation.com', 'http://www.cdw.com', 'http://www.executiveboard.com', 'http://www.cedarfair.com', 'http://www.cedarrealtytrust.com', 'http://www.centurycasinos.com', 'http://www.cgi.com', 'http://www.chambersstreet.com', 'http://www.chanticleerholdings.com', 'http://www.charter.com', 'http://www.chathamlodgingtrust.com', 'http://www.chesapeakelodgingtrust.com', 'http://www.chicosfas.com', 'http://www.childrensplace.com', 'http://www.chimerareit.com', 'http://www.chipotle.com', 'http://www.choicehotels.com', 'http://www.christopherandbanks.com', 'http://www.chsinc.com', 'http://www.churchilldowns.com', 'http://www.chuys.com', 'http://www.pmctrust.com', 'http://www.cinemark.com', 'http://www.cititrends.com', 'http://www.clearchanneloutdoor.com', 'http://www.colonyinc.com', 'http://www.cexpgroup.com', 'http://www.comcast.com', 'http://www.commandsecurity.com', 'http://cslreit.com', 'http://www.conns.com', 'http://corenergy.corridortrust.com', 'http://www.coresite.com', 'http://www.copt.com', 'http://www.cca.com', 'http://www.getcosi.com', 'http://www.costco.com', 'http://www.cousinsproperties.com', 'http://www.crackerbarrel.com', 'http://www.crestwoodlp.com', 'http://www.crowncastle.com', 'http://www.hallmarkchannel.com', 'http://www.cssindustries.com', 'http://www.cubesmart.com', 'http://www.cumulus.com', 'http://www.cvsl.us.com', 'http://www.cyrusone.com', 'http://www.cysinv.com', 'http://www.dailyjournal.com', 'http://www.darden.com', 'http://www.daveandbusters.com', 'http://www.dctindustrial.com', 'http://www.ddr.com', 'http://www.dfrg.com', 'http://www.dennys.com', 'http://www.destinationmaternitycorp.com', 'http://www.destinationxl.com', 'http://www.devryinc.com', 'http://www.dexmedia.com', 'http://www.dgsecompanies.com', 'http://www.diamondresorts.com', 'http://www.drhc.com', 'http://www.dickssportinggoods.com', 'http://www.digitalrealtytrust.com', 'http://www.digitalglobe.com', 'http://www.dillards.com', 'http://www.dineequity.com', 'http://www.directv.com', 'http://www.corporate.discovery.com', 'http://www.dish.com', 'http://www.diversifiedrestaurantholdings.com', 'http://www.dollargeneral.com', 'http://www.dollartree.com', 'http://www.douglasemmett.com', 'http://www.doverdowns.com', 'http://www.dovermotorsports.com', 'http://www.dreamworksanimation.com', 'http://www.dswinc.com', 'http://www.dukerealty.com', 'http://www.dunkinbrands.com', 'http://www.dynexcapital.com', 'http://www.scripps.com', 'http://www.eastgroup.net', 'http://www.ene.com', 'http://www.edrtrust.com', 'http://www.elpolloloco.com', 'http://www.eldoradoresorts.com', 'http://www.earnreit.com', 'http://www.emmis.com', 'http://www.empireresorts.com', 'http://www.empirestaterealtytrust.com', 'http://www.engilitycorp.com', 'http://www.englobal.com', 'http://www.ennis.com', 'http://www.entercom.com', 'http://www.entravision.com', 'http://www.envirostarinc.com', 'http://www.eprkc.com', 'http://www.cwhreit.com', 'http://www.equitylifestyle.com', 'http://www.equityone.net', 'http://www.eqr.com', 'http://www.unitedstationers.com', 'http://www.essexpropertytrust.com', 'http://www.shophq.com', 'http://www.exceltrust.com', 'http://www.expedia.com', 'http://www.exponent.com', 'http://www.express.com', 'http://www.extendedstayamerica.com', 'http://www.extraspace.com', 'http://www.ezcorp.com', 'http://www.fairwaymarket.com', 'http://www.familydollar.com', 'http://www.famousdaves.com', 'http://www.fastenal.com', 'http://www.federalrealty.com', 'http://www.felcor.com', 'http://www.fenixparts.com', 'http://www.ferrellgas.com', 'http://www.frgi.com', 'http://www.firstcash.com', 'http://www.firstindustrial.com', 'http://www.first-potomac.com', 'http://www.fivebelow.com', 'http://www.fiveoaksinvestment.com', 'http://www.flanigans.net', 'http://www.fogodechao.com', 'http://www.footlocker-inc.com', 'http://www.forrester.com', 'http://www.francescas.com', 'http://www.franklincovey.com', 'http://www.franklinstreetproperties.com', 'http://www.fredsinc.com', 'http://www.frischs.com', 'http://www.ftd.com', 'http://www.fticonsulting.com', 'http://www.fullhouseresorts.com', 'http://www.gkservices.com', 'http://www.gaiam.com', 'http://www.gamestop.com', 'http://www.glpropinc.com', 'http://www.gapinc.com', 'http://www.gartner.com', 'http://www.gatx.com', 'http://www.geek.net', 'http://www.generalfinance.com', 'http://www.ggp.com', 'http://www.genesco.com', 'http://www.geogroup.com', 'http://www.gladstonecommercial.com', 'http://www.gladstoneland.com', 'http://www.globaleagleent.com', 'http://www.globalstar.com', 'http://www.gogoair.com', 'http://www.goodtimesburgers.com', 'http://www.gordmans.com', 'http://www.gpstrategies.com', 'http://www.ghco.com', 'http://www.gptreit.com', 'http://www.gcu.edu', 'http://www.gray.tv', 'http://www.great-ajax.com', 'http://www.televisa.com', 'http://www.gyrodyne.com', 'http://www.hrblock.com', 'http://www.hanes.com', 'http://www.hannonarmstrong.com', 'http://www.hatfin.com', 'http://www.havertys.com', 'http://www.hawaiiantel.com', 'http://www.hcpi.com', 'http://www.hdsupply.com', 'http://www.hcreit.com', 'http://www.healthcarerealty.com', 'http://www.htareit.com', 'http://www.hmny.com', 'http://www.hemispheretv.com', 'http://www.hersha.com', 'http://www.hertz.com', 'http://www.hfflp.com', 'http://www.hhgregg.com', 'http://www.hibbett.com', 'http://www.highwoods.com', 'http://www.hillintl.com', 'http://www.hmgcourtland.com', 'http://www.homedepot.com', 'http://www.homeproperties.com', 'http://www.hornbeckoffshore.com', 'http://www.hptreit.com', 'http://www.hosthotels.com', 'http://www.hmhco.com', 'http://www.howardhughes.com', 'http://www.hsni.com', 'http://www.huronconsultinggroup.com', 'http://www.huttig.com', 'http://www.hyatt.com', 'http://www.iac.com', 'http://www.icfi.com', 'http://www.igniterestaurants.com', 'http://www.impaccompanies.com', 'http://www.incomeopp-realty.com', 'http://www.irtreit.com', 'http://www.isg-one.com', 'http://www.ingles-markets.com', 'http://www.inlandrealestate.com', 'http://www.innsuitestrust.com', 'http://www.insight.com', 'http://www.insigniasystems.com', 'http://www.igt.com', 'http://www.internationalspeedwaycorporation.com', 'http://www.inuvo.com', 'http://www.invescomortgagecapital.com', 'http://www.iret.com', 'http://www.ironmountain.com', 'http://www.isleofcapricasinos.com', 'http://www.starentnetworks.com', 'http://www.ittesi.com', 'http://www.jwmays.com', 'http://www.jcpenney.com', 'http://www.jackinthebox.com', 'http://www.jambajuice.com', 'http://www.javelin.com', 'http://www.jewettcameron.com', 'http://www.k12.com', 'http://www.kilroyrealty.com', 'http://www.kimcorealty.com', 'http://www.kirbycorp.com', 'http://www.kirklands.com', 'http://www.kiterealty.com', 'http://www.kohls.com', 'http://www.konagrill.com', 'http://www.kroger.com', 'http://www.labarge.com', 'http://www.lakesentertainment.com', 'http://www.lamar.com', 'http://www.landmarkmlp.com', 'http://www.landsend.com', 'http://www.lasvegassands.com', 'http://www.lasallehotels.com', 'http://www.learningtree.com', 'http://www.lee.net', 'http://www.lxp.com', 'http://ir.libertybroadband.com', 'http://www.libertyinteractive.com', 'http://www.libertymedia.com', 'http://www.libertyproperty.com', 'http://www.ltbridge.com', 'http://www.lincolneducationalservices.com', 'http://www.lionsgatefilms.com', 'http://www.livenationentertainment.com', 'http://www.lkqcorp.com', 'http://www.lowes.com', 'http://www.ltcproperties.com', 'http://www.lubys.com', 'http://www.landleisure.dk', 'http://www.macerich.com', 'http://www.mack-cali.com', 'http://www.macysinc.com', 'http://www.manhattanbridgecapital.com', 'http://www.mantech.com', 'http://www.marcuscorp.com', 'http://www.marinemax.com', 'http://www.marriott.com', 'http://www.marthastewart.com', 'http://www.mastech.com', 'http://www.matson.com', 'http://www.mattersight.com', 'http://www.mattressfirm.com', 'http://www.mcclatchy.com', 'http://www.aboutmcdonalds.com', 'http://www.mediageneral.com', 'http://www.medicalpropertiestrust.com', 'http://www.meetmecorp.com', 'http://www.menswearhouse.com', 'http://www.meredith.com', 'http://www.mfafinancial.com', 'http://www.mgmmirage.com', 'http://www.maac.com', 'http://www.mistrasgroup.com', 'http://www.monarchcasino.com', 'http://www.monogramres.com', 'http://www.monro.com', 'http://www.morganshotelgroup.com', 'http://www.nathansfamous.com', 'http://www.national.edu', 'http://www.ncm.com', 'http://www.nhireit.com', 'http://www.nnnreit.com', 'http://www.naturalgrocers.com', 'http://www.navigantconsulting.com', 'http://www.netflix.com', 'http://www.neustar.biz', 'http://www.nevadagold.com', 'http://www.thehamiltoncompany.com', 'http://www.newresi.com', 'http://www.sunairhf.com', 'http://www.nyandcompany.com', 'http://www.nymtrust.com', 'http://www.nytco.com', 'http://www.newcastleinv.com', 'http://www.newscorp.com', 'http://www.nexstar.tv', 'http://www.egov.com', 'http://www.noodles.com', 'http://www.nordstrom.com', 'http://www.nrfc.com', 'http://www.ncl.com', 'http://www.buzztime.com', 'http://www.nutrisystem.com', 'http://www.nv5.com', 'http://www.nxt-id.com', 'http://www.shipwreck.net', 'http://www.officedepot.com', 'http://www.omegahealthcare.com', 'http://www.onelibertyproperties.com', 'http://www.orbcomm.com', 'http://www.orbitz.com', 'http://www.orchidislandcapital.com', 'http://www.oreillyauto.com', 'http://www.outerwall.com', 'http://www.overstock.com', 'http://www.owensmortgage.com', 'http://www.pacsun.com', 'http://www.pandora.com', 'http://www.panerabread.com', 'http://www.bulkcommercialservices.com', 'http://www.papajohns.com', 'http://www.papamurphys.com', 'http://www.paramount-group.com', 'http://www.pky.com']

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Transportation')
	##### Transportation
	#urls=['http://www.airmethods.com', 'http://www.airt.net', 'http://www.atsginc.com', 'http://www.alk-abello.com', 'http://www.allegiantair.com', 'http://www.aa.com', 'http://www.arkbest.com', 'http://www.atlasair.com', 'http://www.baltictrading.com', 'http://www.brinks.com', 'http://www.bristowgroup.com', 'http://www.chrobinson.com', 'http://www.cn.ca', 'http://www.cpr.ca', 'http://www.celadontrucking.com', 'http://www.ctginvestor.com', 'http://www.csx.com', 'http://www.delta.com', 'http://www.eagleships.com', 'http://www.echo.com', 'http://www.eragroupinc.com', 'http://www.expeditors.com', 'http://www.fedex.com', 'http://www.forwardair.com', 'http://www.patriottrans.com', 'http://www.gwrr.com', 'http://www.oma.aero', 'http://www.aeropuertosgap.com.mx', 'http://www.asur.com.mx', 'http://www.hawaiianair.com', 'http://www.heartlandexpress.com', 'http://www.hubgroup.com', 'http://www.intship.com', 'http://www.jbhunt.com', 'http://www.jetblue.com', 'http://www.kcsouthern.com', 'http://www.knighttransportation.com', 'http://www.landstar.com', 'http://www.marten.com', 'http://www.nscorp.com', 'http://www.odfl.com', 'http://www.osg.com', 'http://www.pamt.com', 'http://www.phihelico.com', 'http://www.pwrr.com', 'http://www.qualitydistribution.com', 'http://www.radiantdelivers.com', 'http://www.republicairways.com', 'http://www.rrts.com', 'http://www.saia.com', 'http://www.seacorholdings.com', 'http://www.sino-global.com', 'http://www.skywest.com', 'http://www.southwest.com', 'http://www.spirit.com', 'http://www.ridesta.com', 'http://www.swifttrans.com', 'http://www.up.com', 'http://www.unitedcontinentalholdings.com', 'http://www.ups.com', 'http://www.goutsi.com', 'http://www.usa-truck.com', 'http://www.usdpartners.com', 'http://www.go2uti.com', 'http://www.werner.com', 'http://www.yrcw.com']

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&industry=Basic+Industries&pagesize=300')
	############# Basic Industries
	#urls=['http://www.aschulman.com', 'http://www.aegion.com', 'http://www.aemetis.com', 'http://www.gencorp.com', 'http://www.agnico-eagle.com', 'http://www.agrium.com', 'http://www.airproducts.com', 'http://www.aksteel.com', 'http://www.albint.com', 'http://www.albemarle.com', 'http://www.alderonironore.com', 'http://www.alexcoresource.com', 'http://www.alleghenytechnologies.com', 'http://www.almadenminerals.com', 'http://www.amark.com', 'http://www.ameresco.com', 'http://www.american-vanguard.com', 'http://www.americanwoodmark.com', 'http://www.amyris.com', 'http://www.arcadiabio.com', 'http://www.arganinc.com', 'http://www.asanko.com', 'http://www.atlatsaresources.co.za', 'http://www.avalonventures.com', 'http://www.avino.com', 'http://www.axaltacs.com', 'http://www.axiall.com', 'http://www.b2gold.com', 'http://www.balchem.com', 'http://www.banro.com', 'http://www.barrick.com', 'http://www.belden.com', 'http://www.bio-amber.com', 'http://www.biopharmx.com', 'http://www.cabot-corp.com', 'http://www.calgoncarbon.com', 'http://www.cameco.com', 'http://www.carlisle.com', 'http://www.cartech.com', 'http://www.amcastle.com', 'http://www.cavco.com', 'http://www.celanese.com', 'http://www.centrusenergy.com', 'http://www.centuryaluminum.com', 'http://www.cfindustries.com', 'http://www.chemtura.com', 'http://www.churchdwight.com', 'http://www.cleanharbors.com', 'http://www.clearwaterpaper.com', 'http://www.cliffsnaturalresources.com', 'http://www.codexis.com', 'http://www.coeur.com', 'http://www.compassminerals.com', 'http://www.comstockmining.com', 'http://www.corning.com', 'http://www.covantaenergy.com', 'http://www.crowncrafts.com', 'http://www.ctiindustries.com', 'http://www.culpinc.com', 'http://www.cvrpartners.com', 'http://www.cytec.com', 'http://www.deltic.com', 'http://www.denisonmines.com', 'http://www.ddcorp.ca', 'http://www.domtar.com', 'http://www.dow.com', 'http://www.dycomind.com', 'http://www.dupont.com', 'http://www.eastman.com', 'http://www.ecolab.com', 'http://www.eldoradogold.com', 'http://www.empireresources.com', 'http://www.ica.com.mx', 'http://www.edrsilver.com', 'http://www.enproindustries.com', 'http://www.entreegold.com', 'http://www.eurasianminerals.com', 'http://www.exeterresource.com', 'http://www.femalehealth.com', 'http://www.ferro.com', 'http://www.flexiblesolutions.com', 'http://www.flotekind.com', 'http://www.fluor.com', 'http://www.fmc.com', 'http://www.fairmountsantrol.com', 'http://www.fbhs.com', 'http://www.franco-nevada.com', 'http://www.fcx.com', 'http://www.furmanite.com', 'http://www.generalcable.com', 'http://www.generalmoly.com', 'http://www.gevo.com', 'http://www.glatfelter.com', 'http://www.goldresourcecorp.com', 'http://www.goldstandardv.com', 'http://www.goldcorp.com', 'http://www.goldenminerals.com', 'http://www.gsr.com', 'http://www.goldfieldcorp.com', 'http://www.graniteconstruction.com', 'http://www.gldd.com', 'http://www.greatpanther.com', 'http://www.greenplainspartners.com', 'http://www.gpreinc.com', 'http://www.greenhunterenergy.com', 'http://www.gsimec.com.mx', 'http://www.hbfuller.com', 'http://www.hecla-mining.com', 'http://www.crystal-clean.com', 'http://www.hexcel.com', 'http://www.hicrushpartners.com', 'http://www.hudbayminerals.com', 'http://www.huntsman.com', 'http://www.hydrogenics.com', 'http://www.iamgold.com', 'http://www.indiaglobalcap.com', 'http://www.isa-inc.com', 'http://www.innospecinc.com', 'http://www.iff.com', 'http://www.internationalpaper.com', 'http://www.ithmines.com', 'http://www.intrepidpotash.com', 'http://www.jacobs.com', 'http://www.kapstonepaper.com', 'http://www.kbr.com', 'http://www.kinross.com', 'http://www.koppers.com', 'http://www.kraton.com', 'http://www.kronostio2.com', 'http://www.lbfoster.com', 'http://www.lsgold.com', 'http://www.landec.com', 'http://www.layne.com', 'http://www.lennar.com', 'http://www.lime-energy.com', 'http://www.lpcorp.com', 'http://www.lsbindustries.com', 'http://www.magsilver.com', 'http://www.marronebioinnovations.com', 'http://www.martinmarietta.com', 'http://www.masco.com', 'http://www.masonite.com', 'http://www.mastec.com', 'http://www.matrixservice.com', 'http://www.mcewenmining.com', 'http://www.mdu.com', 'http://www.mercerint.com', 'http://www.mesabi-trust.com', 'http://www.metabolix.com', 'http://www.metalico.com', 'http://www.methanex.com', 'http://www.methes.com', 'http://www.mincomining.com', 'http://www.mineralstech.com', 'http://www.minesmanagement.com', 'http://www.monsanto.com', 'http://www.mosaicco.com', 'http://www.mountainprovince.com', 'http://www.myrgroup.com', 'http://www.neenah.com', 'http://www.nevsun.com', 'http://www.newgold.com', 'http://www.newmarket.com', 'http://www.newmont.com', 'http://www.nl-ind.com', 'http://www.norandaaluminum.com', 'http://www.northerndynastyminerals.com', 'http://www.nwpipe.com', 'http://www.novacopper.com', 'http://www.novagold.com', 'http://www.nucor.com', 'http://www.olin.com', 'http://www.olysteel.com', 'http://www.omnova.com', 'http://www.occfiber.com', 'http://www.orchidspaper.com', 'http://www.orion.fi', 'http://www.pacificbooker.bc.ca', 'http://www.pacificethanol.net', 'http://www.panamericansilver.com', 'http://www.paramountgold.com', 'http://www.patrickind.com', 'http://www.perma-fix.com', 'http://www.pershinggold.com', 'http://www.platformspecialtyproducts.com', 'http://www.platinumgroupmetals.net', 'http://www.plygem.com', 'http://www.polymetmining.com', 'http://www.polyone.com', 'http://www.polypore.net', 'http://www.potashcorp.com', 'http://www.ppg.com', 'http://www.praxair.com', 'http://www.precast.com', 'http://www.preformed.com', 'http://www.pennvirginia.com', 'http://www.primoriscorp.com', 'http://www.pg.com', 'http://www.quakerchem.com', 'http://www.rareelementresources.com', 'http://www.rayonieram.com', 'http://rgsenergy.com', 'http://www.rsac.com', 'http://www.regi.com', 'http://www.rentechnitrogen.com', 'http://www.rentechinc.com', 'http://www.resolutefp.com', 'http://www.richmont-mines.com', 'http://www.rogerscorp.com', 'http://www.royalgold.com', 'http://www.rpminc.com', 'http://www.rubiconminerals.com', 'http://www.ryerson.com', 'http://www.sandstormgold.com', 'http://www.swmintl.com', 'http://www.scotts.com', 'http://www.seabridgegold.net', 'http://www.sealedair.com', 'http://www.sensient.com', 'http://www.sharpsinc.com', 'http://www.silverstandard.com', 'http://www.silverwheaton.com', 'http://www.silvercorpmetals.com', 'http://www.silvercrestmines.com', 'http://www.skylinecorp.com', 'http://www.solarcity.com', 'http://www.solazyme.com', 'http://www.solitarioxr.com', 'http://www.southerncoppercorp.com', 'http://www.steeldynamics.com', 'http://www.stepan.com', 'http://www.stericycle.com', 'http://www.strlco.com', 'http://www.stillwatermining.com', 'http://www.sxcpartners.com', 'http://www.suncoke.com', 'http://www.swisherhygiene.com', 'http://www.synalloy.com', 'http://www.synthesisenergy.com', 'http://www.tahoeresourcesinc.com', 'http://www.tasekomines.com', 'http://www.tasmanmetals.com', 'http://www.teck.com', 'http://www.aes.com', 'http://www.thompsoncreekmetals.com', 'http://www.timberline-resources.com', 'http://www.timkensteel.com', 'http://www.timminsgold.com', 'http://www.titan-intl.com', 'http://www.baldwintech.com', 'http://www.torminerals.com', 'http://www.trcsolutions.com', 'http://www.trex.com', 'http://www.tronox.com', 'http://www.turquoisehill.com', 'http://www.tutorperini.com', 'http://www.ussilica.com', 'http://www.uslm.com', 'http://www.ussteel.com', 'http://www.ufpi.com', 'http://www.univstainless.com', 'http://www.ur-energy.com', 'http://www.uraniumenergy.com', 'http://www.uraniumresources.com', 'http://www.valhi.net', 'http://www.valsparglobal.com', 'http://www.vistagold.com', 'http://www.vulcanmaterials.com', 'http://www.grace.com', 'http://www.wd40.com', 'http://www.westpharma.com', 'http://www.westerncopperandgold.com', 'http://www.westlake.com', 'http://www.xerium.com', 'http://www.yamana.com']

	count=0
	count1=0
	for url in urls:
		count1=count1+1
		if count<70:	
			filname=url.replace('http://','')
			filname=filname.replace( 'https://','')
			filname=filname.replace('www.','')
			filname=re.sub('\..*|\/.*','',filname)
			#print filname
			filename=filname+'.json'
			if filename not in os.listdir('/home/gggopi/company data/'): 		### Point to a folder where all the company are located
				get_info.get_about(url)
			keywords,indus=files_keywords_industry(filename,2,1,1)	
			if keywords=='n/a' or not keywords:
				print "prob : "+filename
				#print keywords,indus
			else:
				print keywords
				print indus
				count = count +1
				print "Total files used which had proper META DATA : count= ",count
				print 'Total files read : count= ',count1,'\n\n'
				# Sector='Basic Industries' 				##### Change this accordingly
				# for key in keywords:
				# 	try:
				# 		tx=graph.cypher.begin()
				# 		tx.append("Match (i:Sector{name:'%s'}) Create (k:Keyword1{value:'%s'})-[r:`Belongs to`]->(i)"%(Sector,key))
				# 		tx.commit()
				# 	except:
				# 		print 'Something went wrong!! U must never reach here'
			




#csvfile1 = open('tfkeys.csv', 'r')

def kw_count():		### to create a dict with count of every keyword in that particular sector and save it in a csv file
	csvfile2 = open('export.csv', 'r')
	fieldnames2 = ("Sector","Keyword")

	reader1 = csv.DictReader( csvfile2, fieldnames2)
	count=0
	mydict={}

	writer=csv.writer(open('tfkeys_1.csv','w'))
	for row in reader1 :
			row['Keyword']=row['Keyword'].lower()
			if row['Sector'] in mydict:
				if row['Keyword'] in mydict[row['Sector']]:
					mydict[row['Sector']][row['Keyword']]=mydict[row['Sector']][row['Keyword']]+1
				else:
					mydict[row['Sector']][row['Keyword']]=1
			else:
				mydict[row['Sector']]={}
	for i in mydict:
		print i
		print mydict[i]
		for j in mydict[i]:
			row={"industry":i,"Keyword":j,"count":mydict[i][j]}
			writer.writerow(row.values())
		print "\n"	



def tfidf():				#### to add tf-idf to each keyword from the csv file created in kw_count()
	csvf=open('tfkeys_1.csv','r')
	writer=csv.writer(open('tfkeys_2.csv','w'))
	fieldnam=("count","Sector","Keyword")
	reader=csv.DictReader(csvf,fieldnam)
	for row in reader:
		if len(row['Keyword'])>3:
			count_sector=0.00000
			csvf1=open('tfkeys_1.csv','r')
			fieldnam1=("count","Sector","Keyword")			
			reader1=csv.DictReader(csvf1,fieldnam1)
			l=0
			for row1 in reader1:
				if row1['Keyword']==row['Keyword'] and row['Sector']!=row1['Sector']:
					l=l+1
				if row['Sector']==row1['Sector']:
					count_sector=count_sector+1
			csvf1.close()
			print l , row['Keyword'],count_sector
			row['tfidf']=(int(row['count'])/count_sector)*math.log(9/(1+l))
			row['tfidf']=int(row['tfidf']*10000) / 100.00

			print row
			writer.writerow(row.values())
	csvf.close()

def tfidf_to_graph():		#### to create the graph with keyword and its weight(tf-idf)
							#### this func matches the Sectors and then creates the keyword nodes with a relationship to it!!
	
	### Before running this, Create the Sector nodes with unique value constraint
	
	## csvf=open('tfkeys_2.csv','r')
	## fieldnam=("count","Sector","tfidf","Keyword")

	csvf=open('final_keywords_list.csv','r')
	fieldnam=("Sector","Keyword","tfidf")
	reader=csv.DictReader(csvf,fieldnam)
	for row in reader:
		if(row['tfidf']!=-99):
			try:
				print "Match (n1:Sector{name:'%s'}) Create (k:Keyword2{value:'%s',wt:'%s'})-[r:`Belongs to`]->(n1)"%(row['Sector'],row['Keyword'],row['tfidf'])
				tx = graph.cypher.begin()
				tx.append("Match (n1:Sector{name:'%s'}) Create (k:Keyword2{value:'%s',wt:'%s'})-[r:`Belongs to`]->(n1)"%(row['Sector'],row['Keyword'],row['tfidf']))
				tx.commit()
				print 'done'
			except:
				print "Exception part:"
				# print "Match (n1:Sector{name:'%s'}),(m1:Industry{name:'%s'}) Create (m1)-[r:`is a Subsector of`]->(n1)"%(sec,industry)
				# tx = graph.cypher.begin()
				# tx.append("Match (n1:Sector{name:'%s'}),(m1:Industry{name:'%s'}) Create (m1)-[r:`is a Subsector of`]->(n1)"%(sec,industry))
				# tx.commit()

def find_indus():
	
	############# URLS FOR TESTING ##########################

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&page=2&industry=Capital+Goods')
	#urls=['http://www.broadwindenergy.com', 'http://www.bruker.com', 'http://www.carboceramics.com', 'http://www.cascademicrotech.com', 'http://www.caterpillar.com', 'http://www.cecoenviro.com', 'http://www.cemex.com', 'http://www.cemtrex.com', 'http://www.centurycommunities.com', 'http://www.cepheid.com', 'http://www.cescatherapeutics.com', 	'http://www.chart-ind.com', 'http://www.circor.com', 	'http://www.clarcor.com', 'http://www.cdti.com', 'http://www.clearsigncombustion.com', 'http://www.coastdistribution.com', 'http://www.cognex.com', 'http://www.coherent.com', 'http://www.cohu.com', 'http://www.colfaxcorp.com', 'http://www.cmworks.com', 'http://www.combimatrix.com', 'http://www.comfortsystemsusa.com', 'http://www.cvgrp.com', 'http://www.compasstrust.com', 'http://www.compx.com','http://www.comstockhomes.com', 'http://www.continental-materials.com','http://www.control4.com', 'http://www.cpiaero.com', 'http://www.alsic.com', 'http://www.craneco.com', 'http://www.cubic.com', 'http://www.cyberoptics.com', 'http://www.drhorton.com', 'http://www.dana.com', 'http://www.danaher.com','http://www.dataio.com', 'http://www.deere.com', 'http://www.digipwr.com', 'http://www.donaldson.com', 'http://www.dormanproducts.com', 'http://www.douglasdynamics.com', 'http://www.drewindustries.com', 'http://www.ducommun.com', 'http://www.dxpe.com', 'http://www.dynamicmaterials.com', 'http://www.dynasil.com']
	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&page=2&industry=Energy')
	#urls=['http://www.ckxlands.com', 'http://www.claytonwilliams.com',	 'http://www.cloudpeakenergy.com', 'http://www.cobaltintl.com',  'http://www.comstockresources.com', 'http://www.conchoresources.com', 'http://www.conocophillips.com', 'http://www.consolenergy.com', 'http://www.contango.com', 'http://www.contres.com', 'http://www.crosstimberstrust.com', 'http://www.crossamericapartners.com', 'http://www.compressco.com', 'http://www.cummins.com', 'http://www.coffeyvillegroup.com', 	 'http://www.cvrrefining.com', 'http://www.dakotaplains.com', 'http://www.dawson3d.com', 'http://www.dejour.com', 'http://www.deleklogistics.com', 'http://www.mapcoexpress.com', 'http://www.denbury.com', 'http://www.devonenergy.com', 'http://www.diamondoffshore.com', 'http://www.diamondbackenergy.com', 'http://www.dom-dominion.com',	  'http://www.dmlp.net', 'http://www.dril-quip.com', 'http://www.eaglerockenergy.com', 'http://www.earthstoneenergy.com', 'http://www.eclipseresources.com', 'http://www.ecostim-es.com', 'http://www.emeraldoil.com', 'http://www.emergelp.com', 'http://www.emerson.com',   'http://www.enbridgemanagement.com', 'http://www.enbridge.com', 'http://www.encana.com', 'http://www.enduroroyaltytrust.com', 'http://www.energen.com', 'http://www.enerjex.com', 'http://www.enerplus.com', 'http://www.enservco.com', 'http://www.eogresources.com', 'http://www.enterprisegp.com', 'http://www.eqt.com'	 ]
	
	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&page=2&industry=Finance')
	#urls=['http://www.anchornetbank.com', 'http://www.anchorbank.com', 'http://www.aon.com', 'http://www.acptrust.com',	 'http://www.arcapitalacquisitioncorp.com', 'http://www.arlingtonasset.com', 'http://www.armadahoffler.com', 	 'http://www.arrowfinancial.com', 'http://www.ajg.com', 'http://www.artisanpartners.com', 'http://www.ashevillesavingsbank.com', 'http://www.associatedbank.com', 'http://www.assurant.com', 'http://www.astafunding.com', 	'http://www.astoriabank.com', 'http://www.athensfederal.com', 'http://www.atlam.com', 'http://www.atlanticcoastbank.net', 	 'http://www.atlanticus.com', 'http://www.atlas-fin.com', 'http://www.auburnbank.com', 'http://www.avenuenashville.com', 'http://www.baldwinandlyons.com', 'http://www.bancfirst.com', 'http://www.bonj.net', 'http://www.bancorpsouth.com', 'http://www.bankmutualcorp.com', 'http://www.bankofamerica.com', 'http://www.bankofcommerceholdings.com', 'http://www.boh.com', 'http://www.bankofmarin.com', 'http://www.bankofny.com', 'http://www.scotiabank.ca', 'http://www.banksc.com', 'http://www.bankofthejames.com', 'http://www.bankozarks.com', 'http://www.bankfinancial.com'	 ]

	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&page=2&industry=Health+Care')
	#urls=['http://www.almostfamily.com', 'http://www.alnylam.com', 'http://www.alphaprotech.com', 'http://www.alphatecspine.com', 'http://www.amagpharma.com', 'http://www.amedica.com', 'http://www.amedisys.com', 'http://www.americancaresource.com', 'http://www.as-e.com', 'http://www.ashs.com', 'http://www.amerisourcebergen.net', 'http://www.amgen.com', 'http://www.amicusrx.com', 'http://www.amphastar.com', 'http://www.ampiopharma.com', 'http://www.amsurg.com', 'http://www.anacor.com', 'http://www.angiodynamics.com', 'http://www.anipharmaceuticals.com', 'http://www.anikatherapeutics.com', 'http://www.antarespharma.com', 'http://www.wellpoint.com', 'http://www.acunetx.com', 'http://www.anthera.com', 'http://www.aoxingpharma.com', 'http://www.agtc.com', 'http://www.apricusbio.com', 'http://www.aptose.com', 'http://www.aqxpharma.com', 'http://www.aradigm.com', 'http://www.aratana.com', 'http://www.arcabiopharma.com', 'http://www.ardelyx.com', 'http://www.arenapharm.com', 'http://www.argostherapeutics.com', 'http://www.ariad.com', 'http://www.arqule.com', 'http://www.arraybiopharma.com', 'http://www.arthrt.com', 'http://www.arrowheadresearch.com', 'http://www.assemblybio.com', 'http://asteriasbiotherapeutics.com', 'http://www.atarabio.com', 'http://www.athersys.com', 'http://www.atossagenetics.com', 'http://www.atricure.com', 'http://www.atrioncorp.com', 'http://www.atyrpharma.com', 'http://www.auriniapharma.com']
	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&page=2&industry=Technology')
	#urls=['http://www.axcelis.com', 'http://www.axt.com', 'http://www.barrettbusiness.com', 'http://www.bazaarvoice.com', 'http://www.bench.com', #'http://www.benefitfocus.com', 'http://www.bgstaffing.com', 'http://www.blackbox.com', 	'http://www.blackbaud.com', 'http://www.blondertongue.com',	 'http://www.blucora.com', 'http://www.bottomline.com', 'http://www.seacubecontainer.com', 	'http://www.bridgelinesw.com', 'http://www.brightcove.com', 'http://www.broadcom.com',	 'http://www.broadsoft.com', 'http://www.broadvision.com', 	'http://www.brocade.com', #'http://www.brooks.com', 'http://www.ca.com', 'http://www.cabotcmp.com', 'http://www.caci.com', 'http://www.cadence.com', 'http://www.capps.com', 'http://www.calamp.com', 'http://www.callidussoftware.com', 'http://www.carbonite.com', 'http://www.cavium.com', 'http://www.cdicorp.com', 'http://www.celestica.com', 'http://www.cerner.com', 'http://www.ceva-dsp.com', 'http://www.channeladvisor.com', 'http://www.chicagorivet.com', 'http://www.ciber.com', 'http://www.cirrus.com', 'http://www.cisco.com', 'http://www.citrix.com', 'http://www.cogentco.com', 'http://www.cognizant.com', 'http://www.collabrx.com', 'http://www.commscope.com', 'http://www.commvault.com', 'http://www.cpsinet.com', 'http://www.csc.com', 'http://www.ctg.com', 'http://www.comtechtel.com'	]
	# urls=[
	# 'http://www.tataatsu.com','https://www.uber.com',	'https://angel.co',
	# 'http://www.icicibank.com','http://www.hdfcbank.com',
	# 'https://www.olacabs.com',
	# 'http://unitedbreweries.com','https://www.leftronic.com','http://doubledutch.me',
	# 'http://www.bhpbilliton.com','http://www.novogen.com','http://www.primabiomed.com.au','http://www.westpac.com.au','http://www.goldmansachs.com'
	# 'http://www.qualcomm.co.in',
	# 'http://www.cyberark.com','http://www.evogene.com',
	# 'https://www.counsyl.com'
	# ]
	#urls=['http://www.tataatsu.com']
	
	#urls=geturls.geturl('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&page=2&industry=Consumer+Services')
	#urls=['http://www.e-arc.com', 'http://www.arescre.com', 'http://www.arkrestaurants.com', 'http://www.armourreit.com', 'http://www.dressbarn.com', 	'http://www.ascentcapitalgroupinc.com', 'http://www.ahpreit.com', 'http://www.ahtreit.com', 'http://www.ashfordinc.com', 'http://www.aerogel.com', 'http://www.associatedestates.com', 'http://www.autozone.com', 'http://www.avalonbay.com', 'http://www.avisbudgetgroup.com', 'http://www.barnesandnobleinc.com', 'http://www.beaconroofingsupply.com', 'http://www.bbgi.com', 'http://www.bedbathandbeyond.com', 'http://www.bestbuy.com', 'http://www.big5sportinggoods.com', 'http://www.biglots.com', 'http://www.biglariholdings.com', 'http://www.biomedrealty.com', 'http://www.biopathholdings.com', 'http://www.birksgroup.com', 'http://www.bjsbrewhouse.com', 'http://www.bloominbrands.com', 'http://www.bluenile.com', 'http://www.bobevans.com', 'http://www.boingo.com', 'http://www.bc.com', 'http://www.bojangles.com', 'http://www.booksamillioninc.com', 'http://www.bootbarn.com', 'http://www.boozallen.com', 'http://www.bostonproperties.com', 'http://www.boydgaming.com', 'http://www.brandywinerealty.com', 'http://www.bbrg.com', 'http://www.bridgepointeducation.com', 'http://www.brinker.com', 'http://www.brookfield.com', 'http://www.brookfieldproperties.com', 'http://www.brtrealty.com', 'http://www.buckle.com', 'http://www.buffalowildwings.com', 'http://www.buildabear.com', 'http://www.bldr.com', 'http://www.cabelas.com']
	#urls=['http://www.adaptly.com', 'http://playdraft.com', 'http://www.graphicly.com',	 'http://appstores.com', 'http://www.evenues.com', 'http://doubledutch.me', 'http://www.backtype.com/', 'http://stipple.com', 'http://www.pinterest.com','http://www.GetSocialize.com', 	 'http://www.styleseat.com',  'http://artsy.net', 'http://stepout.com', 'http://www.misomedia.com', 'http://groundcrew.us/', 'https://www.leftronic.com', 'http://gomiso.com', 'http://www.cardmunch.com', 'http://www.boostmedia.com']

	#urls=['http://getHumanoid.com', 'http://www.breakthrough.com', 'http://appsumo.com', 'http://skillshare.com', 'http://getpantheon.com', 'http://www.internmatch.com', 'http://www.offermatic.com', 'http://massivehealth.com/', 'http://www.wanderfly.com', 'http://www.crowdbooster.com/', 'http://www.storenvy.com', 'http://www.impermium.com', 'http://www.listia.com', 'http://www.ginzametrics.com', 'http://anomalyinnovations.com', 'http://www.punchtab.com', 'http://www.fundly.com', 'http://www.flashsoft.com', 'http://ridemission.com', 'http://www.Proven.com']

	for url in urls:
		filname=url.replace('http://','')
		filname=filname.replace( 'https://','')
		filname=filname.replace('www.','')
		filname=re.sub('\..*|\/.*','',filname)	
		print filname
		print "\n FROM ABOUT description =====================>\n"
		filename=filname+'.json'
		if filename not in os.listdir('/home/gggopi/company data/'):
			get_info.get_about(url)
			#print " file not there in the dir"
		try:
			print 'hello '+filename
			fp=open('/home/gggopi/company data/%s'%filename,'r')
			d=json.load(fp)
			level1_keywords=[]
			level2_keywords=[]
			filename1=re.compile(filname,re.IGNORECASE)
			if len(d["meta_data"]["keywords"].split(','))>1 or len(d['meta_data']['description'])>10:
				level1_keywords=topia_keyword_extractor.getkeywords(str((' '.join((d["meta_data"]["keywords"].split(',')))+' '+d["meta_data"]["description"]).encode('utf-8')),1)#.split(',')
				for k in level1_keywords:
					if filename1.match(k):
						print k,'removed'
						level1_keywords.remove(k)
				print level1_keywords
			if len(d["about"])>100:
					# try:
				level2_keywords=topia_keyword_extractor.getkeywords(str(d["about"].encode('utf-8')),1)
				# except UnicodeEncodeError:
				# 	pass
				for k in level2_keywords:
					if filename1.match(k):
						print k,'removed'
						level2_keywords.remove(k)
				print level2_keywords
			keywords=level1_keywords+level2_keywords
			print keywords
			industry_list={}
			for key in keywords:
				# print key
				# print graph.cypher.execute("Match (n:Keyword2{value:'%s'})--(m:Sector) return m.name, n.wt"%key)
				for rec in graph.cypher.execute("Match (n:Keyword2{value:'%s'})--(m:Sector) return m.name, n.wt"%key):
					if not rec[1]=='-99.0':
						r=float(rec[1])
						if rec[0] in industry_list:
							industry_list[rec[0]]=industry_list[rec[0]]+r
						else:
							industry_list[rec[0]]=r
			print industry_list
			c1=0.0
			c2=0.0
			industry2=''
			industry1=''
			for i in industry_list:
				if c1<=industry_list[i]:
					if c2<=c1:
						c2=c1
						industry2=industry1	
					c1=industry_list[i]
					industry1=i
				elif c2<industry_list[i]:
					c2=industry_list[i]
					industry2=i
				#if c2<c1<industry_list[i]
			print "POSSIBLE SECTORS"
			print "first choice: ",industry1
			print "second choice: ",industry2,'\n\n'
			fp.close()
		except:
			print "some error "+ filename
		
		# print "\n From BLOGS =================>"

		# filename=filname+'_blog.json'
		# try:
		# 	if filename not in os.listdir('/home/gggopi/company data/blogs/'):
		# 		rss.get_blog(url)
		# 	# try:
		# 	keywords=[]
		# 	print 'hello '+filename
		# 	fp=open('/home/gggopi/company data/blogs/%s'%filename,'r')
		# 	blogs=json.load(fp)
		# 	blog_keywords=[]
		# 	for blog in blogs['blogs']:
		# 		if len(blog['description'])>150:
		# 			keywords=topia_keyword_extractor.getkeywords(blog['description'].encode('utf-8'),1)
		# 			blog_keywords.extend(keywords)
		# 		else:
		# 			print blog ," doesn't have enough data in it"
		# 	print blog_keywords
		# 	industry_list={}
		# 	for key in blog_keywords:
		# 		# print key
		# 		# print graph.cypher.execute("Match (n:Keyword2{value:'%s'})--(m:Sector) return m.name, n.wt"%key)
		# 		for rec in graph.cypher.execute("Match (n:Keyword2{value:'%s'})--(m:Sector) return m.name, n.wt"%key):
		# 			if not rec[1]=='-99.0':
		# 				r=float(rec[1])
		# 				if rec[0] in industry_list:
		# 					industry_list[rec[0]]=industry_list[rec[0]]+r
		# 				else:
		# 					industry_list[rec[0]]=r
		# 	print industry_list
		# 	c1=0.0
		# 	c2=0.0
		# 	industry2=''
		# 	industry1=''
		# 	for i in industry_list:
		# 		if c1<=industry_list[i]:
		# 			if c2<=c1:
		# 				c2=c1
		# 				industry2=industry1	
		# 			c1=industry_list[i]
		# 			industry1=i
		# 		elif c2<industry_list[i]:
		# 			c2=industry_list[i]
		# 			industry2=i
		# 	print "POSSIBLE SECTORS"
		# 	print "first choice: ",industry1
		# 	print "second choice: ",industry2,'\n\n'
		# 	fp.close()
		# except:
		# 	print "ERROR: No data in " + filename


#  create_sector__industry_graph()                


########################################################################
# Run this to remove multiple relationships between any two nodes. There must only one relationship between any two nodes 

# print "MATCH (a)-[r]->(b) WITH a,b,type(r) as type, collect(r) as rels FOREACH (r in rels[1..] | DELETE r) "
# tx = graph.cypher.begin()
# tx.append("MATCH (a)-[r]->(b) WITH a,b,type(r) as type, collect(r) as rels FOREACH (r in rels[1..] | DELETE r) ")
# tx.commit()

#########################################################################

insert_keywords_graph()



# kw_count()

# tfidf()

######################################  ::: IMPORTANT ::: 	USE THE "final_keywords_list.csv" instead of running the previous 2 functions but remove the 'count' word from the 'fieldnam' tuple... WHICH has been updated already for u. 

# tfidf_to_graph()

# find_indus()