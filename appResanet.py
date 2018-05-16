#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from modeles import modeleResanet
from technique import datesResanet


app = Flask( __name__ )
app.secret_key = 'resanet'


@app.route( '/' , methods = [ 'GET' ] )
def index() :
	return render_template( 'vueAccueil.html' )

@app.route( '/usager/session/choisir' , methods = [ 'GET' ] )
def choisirSessionUsager() :
	return render_template( 'vueConnexionUsager.html' , carteBloquee = False , echecConnexion = False , saisieIncomplete = False )

@app.route( '/usager/seConnecter' , methods = [ 'POST' ] )
def seConnecterUsager() :
	numeroCarte = request.form[ 'numeroCarte' ]
	mdp = request.form[ 'mdp' ]

	if numeroCarte != '' and mdp != '' :
		usager = modeleResanet.seConnecterUsager( numeroCarte , mdp )
		if len(usager) != 0 :
			if usager[ 'activee' ] == True :
				session[ 'numeroCarte' ] = usager[ 'numeroCarte' ]
				session[ 'nom' ] = usager[ 'nom' ]
				session[ 'prenom' ] = usager[ 'prenom' ]
				session[ 'mdp' ] = mdp
				
				return redirect( '/usager/reservations/lister' )
				
			else :
				return render_template('vueConnexionUsager.html', carteBloquee = True , echecConnexion = False , saisieIncomplete = False )
		else :
			return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = True , saisieIncomplete = False )
	else :
		return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = False , saisieIncomplete = True)


@app.route( '/usager/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterUsager() :
	session.pop( 'numeroCarte' , None )
	session.pop( 'nom' , None )
	session.pop( 'prenom' , None )
	return redirect( '/' )


@app.route( '/usager/reservations/lister' , methods = [ 'GET' ] )
def listerReservations() :
	tarifRepas = modeleResanet.getTarifRepas( session[ 'numeroCarte' ] )
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	
	solde = '%.2f' % ( soldeCarte , )

	aujourdhui = datesResanet.getDateAujourdhuiISO()

	datesPeriodeISO = datesResanet.getDatesPeriodeCouranteISO()
	
	datesResas = modeleResanet.getReservationsCarte( session[ 'numeroCarte' ] , datesPeriodeISO[ 0 ] , datesPeriodeISO[ -1 ] )
	
	joursF = modeleResanet.getJoursFeries()
	
	dates = []

	for uneDateISO in datesPeriodeISO :
		uneDate = {}
		uneDate[ 'iso' ] = uneDateISO
		uneDate[ 'fr' ] = datesResanet.convertirDateISOversFR( uneDateISO )
		
		if uneDateISO <= aujourdhui :
			uneDate[ 'verrouillee' ] = True
		else :
			uneDate[ 'verrouillee' ] = False

		if uneDateISO in datesResas :
			uneDate[ 'reservee' ] = True
		else :
			uneDate[ 'reservee' ] = False
			
		if soldeCarte < tarifRepas and uneDate[ 'reservee' ] == False :
			uneDate[ 'verrouillee' ] = True
		
		if uneDateISO in joursF :
			uneDate[ 'verrouillee' ] = True
			
		if uneDateISO[5:10] in joursF:
			uneDate[ 'verrouillee' ] = True
			
		dates.append( uneDate )
	
	if soldeCarte < tarifRepas :
		soldeInsuffisant = True
	else :
		soldeInsuffisant = False
		
	
	return render_template( 'vueListeReservations.html' , joursF = joursF, laSession = session , leSolde = solde , lesDates = dates , soldeInsuffisant = soldeInsuffisant )

	
@app.route( '/usager/reservations/annuler/<dateISO>' , methods = [ 'GET' ] )
def annulerReservation( dateISO ) :
	modeleResanet.annulerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.crediterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )
	
@app.route( '/usager/reservations/enregistrer/<dateISO>' , methods = [ 'GET' ] )
def enregistrerReservation( dateISO ) :
	modeleResanet.enregistrerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.debiterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )

@app.route( '/usager/mdp/modification/choisir' , methods = [ 'GET' ] )
def choisirModifierMdpUsager() :
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )	
	return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = '' )

@app.route( '/usager/mdp/modification/appliquer' , methods = [ 'POST' ] )
def modifierMdpUsager() :
	ancienMdp = request.form[ 'ancienMDP' ]
	nouveauMdp = request.form[ 'nouveauMDP' ]
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	if ancienMdp != session[ 'mdp' ] or nouveauMdp == '' :
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Nok' )
		
	else :
		modeleResanet.modifierMdpUsager( session[ 'numeroCarte' ] , nouveauMdp )
		session[ 'mdp' ] = nouveauMdp
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Ok' )


@app.route( '/gestionnaire/session/choisir' , methods = [ 'GET' ] )
def choisirSessionGestionnaire() :
	return render_template( 'vueConnexionGestionnaire.html' , echecConnexion = False , saisieIncomplete = False )

@app.route( '/gestionnaire/seConnecter' , methods = [ 'POST' ] )
def seConnecterGestionnaire() :
	login = request.form[ 'login' ]
	mdp = request.form[ 'mdp' ]


	if login != '' and mdp != '' :
		gestionnaire = modeleResanet.seConnecterGestionnaire( login , mdp )
		if len(gestionnaire) != 0 :
			session[ 'login' ] = gestionnaire[ 'login' ]
			session['nom'] = gestionnaire['nom']
			session['prenom'] = gestionnaire['prenom']
			session[ 'mdp' ] = mdp
				
			return redirect( '/gestionnaire/avecCarte/lister')
				
		else :
			return render_template('vueConnexionGestionnaire.html', echecConnexion = True , saisieIncomplete = False )
	else :
		return render_template('vueConnexionGestionnaire.html', echecConnexion = False , saisieIncomplete = True)

@app.route( '/gestionnaire/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterGestionnaire() :
	session.pop( 'login' , None )
	session.pop( 'nom' , None )
	session.pop( 'prenom' , None )
	return redirect( '/' )

@app.route('/gestionnaire/avecCarte/lister' , methods = [ 'GET' ] )
def listerPersonnelAvecCarte():
	avecCarte = modeleResanet.getPersonnelsAvecCarte()
	oui = len(avecCarte)
	return render_template( 'vuePersonnelAvecCarte.php', avecCarte = avecCarte, oui = oui)
	
@app.route('/gestionnaire/sansCarte/lister' , methods = [ 'GET' ] )
def listerPersonnelSansCarte():
	sansCarte = modeleResanet.getPersonnelsSansCarte()
	non = len(sansCarte)
	return render_template( 'vuePersonnelSansCarte.html', sansCarte = sansCarte, non = non)

@app.route('/gestionnaire/bloquerCarte' , methods = [ 'POST' ] )
def bloquerCarte():
	avecCarte = modeleResanet.getPersonnelsAvecCarte()
	numeroCarte=request.form['numeroCarte']
	bloquerCarte = modeleResanet.bloquerCarte(numeroCarte)
	return redirect( '/gestionnaire/avecCarte/lister' )
	
@app.route('/gestionnaire/activerCarte' , methods = [ 'POST' ] )
def activerCarte():
	avecCarte = modeleResanet.getPersonnelsAvecCarte()
	numeroCarte=request.form['numeroCarte']
	activerCarte = modeleResanet.activerCarte(numeroCarte)
	return redirect( '/gestionnaire/avecCarte/lister' )
	
@app.route('/gestionnaire/initMdp' , methods = [ 'POST' ])
def initMdp() :
	avecCarte = modeleResanet.getPersonnelsAvecCarte()
	numeroCarte=request.form['numeroCarte']
	initMdp = modeleResanet.reinitialiserMdp(numeroCarte)
	return redirect( '/gestionnaire/avecCarte/lister' )
	
@app.route('/gestionnaire/creerCompte' , methods = [ 'POST' ])
def creerCompte() :
	matricule=request.form['matricule']
	creerCompte = modeleResanet.creerCarte(matricule)
	return redirect( '/gestionnaire/sansCarte/lister' )
	
@app.route( '/gestionnaire/crediterCarte',methods = [ 'POST' ] )
def crediterCarte() :
    somme =request.form['somme']
    numeroCarte=request.form['numeroCarte']
    CrediterCompte = modeleResanet.crediterCarte( numeroCarte , somme )
    return redirect ('/gestionnaire/avecCarte/lister')
    
@app.route( '/gestionnaire/historique',methods = [ 'POST' ] )
def historique() :
    numeroCarte=request.form['numeroCarte']
    historique = modeleResanet.getHistoriqueReservationsCarte( numeroCarte )
    taille = len(historique)
    dates = []
    for uneDate in historique:
		dates.append(datesResanet.convertirDateISOversFR( uneDate ))	
    return render_template ('vueHistorique.html', taille = taille, dates = dates)
    
@app.route( '/gestionnaire/resaDate/lister',methods = [ 'GET' ] )
def resaDate() :
    date = request.args.get('date','')
    resaDate = modeleResanet.getReservationsDate( date )
    taille1 = len(resaDate)
    return render_template ('vueReservationDate.php', taille1 = taille1, resaDate = resaDate)
    
@app.route( '/gestionnaire/histoParCarte/lister',methods = [ 'GET' ] )
def histoParCarte() :
    numeroCarte = request.args.get('numeroCarte','')
    parCarte = modeleResanet.getHistoriqueReservationsCarte( numeroCarte )
    taille2 = len(parCarte)
    dates = []
    for uneDate in parCarte:
		dates.append(datesResanet.convertirDateISOversFR( uneDate ))	
    return render_template ('vueHistoParCarte.php', taille2 = taille2, parCarte = parCarte, dates = dates)

if __name__ == '__main__' :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )
