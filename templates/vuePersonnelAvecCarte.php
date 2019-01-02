<html DOCTYPE!>
{% include "vueEntete.html" %}
{% include "vueEnteteGestionnaire.html" %}
	<h3>Liste du personnel avec carte</h3>
	<table class="table">
		<thead class="thead-light">
			<tr>
				<th scope="col">N° Carte</th>
				<th scope="col">Solde</th>
				<th scope="col">Matricule</th>
				<th scope="col">Nom</th>
				<th scope="col">Prénom</th>
				<th scope="col">Service</th>
			</tr>
		</thead>
		<tbody>	
			{% for i in range(oui) %}
			<tr>
				<td>{{avecCarte[i]['numeroCarte']}}</td>
				<td>{{avecCarte[i]['solde']}}</td>
				<td>{{avecCarte[i]['matricule']}}</td>
				<td>{{avecCarte[i]['nom']}}</td>
				<td>{{avecCarte[i]['prenom']}}</td>
				<td>{{avecCarte[i]['nomService']}}</td>
				{% if avecCarte[i]['activee'] == 1 %}
					<td>
						<form  role="form" action="/gestionnaire/crediterCarte" method="POST">
							<button  name="numeroCarte" onclick="return alert ('Compte crédité')" type="numeric" value="{{avecCarte[i]['numeroCarte']}}"  >Créditer</button>
							<input id="number" type="number" name="somme" step="0.1"min="0">
						</form>
					</td>
					<td>
						<form id="bloquer" role="form" action="/gestionnaire/bloquerCarte" method="POST">
							<button type="numeric"  name="numeroCarte" id="bloquer" value="{{avecCarte[i]['matricule']}}" onclick="return alert('Carte bloquée')">Bloquer</button>
						</form>
					</td>
					<td>
						<form id="reset" role="form" action="/gestionnaire/initMdp" method="POST">
							<button type="numeric" name="numeroCarte" id="credit" value="{{avecCarte[i]['matricule']}}" onclick="return alert('Mot de passe réinitialisé')">init.MDP</button>
						</form>
					</td>
					<td>
						<form id="historique" role="form" action="/gestionnaire/historique" method="POST">
							<button type="numeric" name="numeroCarte" id="historique" value="{{avecCarte[i]['matricule']}}">Historique</button>
						</form>
					</td>
				{% else %}
					<td></td>
					<td>
						<form id="activer" role="form" action="/gestionnaire/activerCarte" method="POST">
							<button type="numeric" name="numeroCarte" id="activer" value="{{avecCarte[i]['matricule']}}" onclick="return alert('Carte activé')">Activer</button>
						</form>
					</td>
					<td></td>
					<td>
						<form id="historique" role="form" action="/gestionnaire/historique" method="POST">
							<button type="numeric" name="numeroCarte" id="historique" value="{{avecCarte[i]['matricule']}}">Historique</button>
						</form>
					</td>
				{% endif %}
			</tr>
			{% endfor %}
			</tbody>
	</table>
{% include "vuePied.html" %}
</html>
