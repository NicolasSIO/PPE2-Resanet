<html DOCTYPE!>
{% include "vueEntete.html" %}
{% include "vueEnteteGestionnaire.html" %}
	<body>
		
		 <form role="form" action="/gestionnaire/resaDate/lister" method="GET">
        <input type="date" name="date">
        </form>
		
		<center>
		<table  class="table">
				<tr>
					<th scope="col">N° Carte</th>
					<th scope="col">Nom</th>
					<th scope="col">Prénom</th>
					<th scope="col">Service</th>
				</tr>
				{% for i in range(taille1) %}
					<td>{{resaDate[i]['numeroCarte']}}</td>
					<td>{{resaDate[i]['nom']}}</td>
					<td>{{resaDate[i]['prenom']}}</td>
					<td>{{resaDate[i]['nomService']}}</td>
				{% endfor %}
		</table>
		</center>

	</body>
{% include "vuePied.html" %}
</html>
