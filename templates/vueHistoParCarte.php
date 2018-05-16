<html DOCTYPE!>
{% include "vueEntete.html" %}
{% include "vueEnteteGestionnaire.html" %}
	<body>
		
		 <form role="form" action="/gestionnaire/histoParCarte/lister" method="GET">
        <input type="numeric" name="numeroCarte">
        </form>
		
		<center>
		<table  class="table">
				{% for i in range(taille2) %}
					{{dates[i]}}</br>
					
				{% endfor %}
		</table>
		</center>

	</body>
{% include "vuePied.html" %}
</html>

