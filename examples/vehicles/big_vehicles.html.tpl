<html>
  <head>
    <title>Big vehicles</title>
  </head>
  <body>
    <h1>Big vehicles</h1>
    <ul>
{% for vehicle in vehicles %}
  {% if vehicle.weight > 500 %}
      <li>{{ vehicle.name }}</li>
  {% endif %}
{% endfor %}
  </ul>
  </body>
</html>
