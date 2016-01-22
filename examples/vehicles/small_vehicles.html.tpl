<html>
  <head>
    <title>Small vehicles</title>
  </head>
  <body>
    <h1>Small vehicles</h1>
    <ul>
{% for vehicle in vehicles %}
  {% if vehicle.weight <= 500 %}
      <li>{{ vehicle.name }}</li>
  {% endif %}
{% endfor %}
  </ul>
  </body>
</html>
