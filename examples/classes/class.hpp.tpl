/**
 * \file {{ class.name | snake_case }}.hpp
 */

#pragma once

#include <string>

class {{ class.name | pascal_case }} {
public:
    {{ class.name | pascal_case }}({% for field in class.fields %}{{ field.type }} {{ field.name | snake_case }}{% if not loop.last %}, {% endif %}{% endfor %}){% if class.fields %} :
{%- for field in class.fields %}
        m_{{ field.name | snake_case }}({{ field.name | snake_case }}){% if not loop.last %},{% endif %}
{%- endfor %}
{%- endif %}
    {}
{% if class.fields %}
{%- for field in class.fields %}
    {{ field.type }} get{{ field.name | pascal_case }}() const {
        return m_{{ field.name | snake_case }};
    }

    void set{{ field.name | pascal_case }}({{ field.type }} {{ field.name | snake_case }}) {
        m_{{ field.name | snake_case }} = {{ field.name | snake_case }};
    }

{%- endfor %}

private:
{%- for field in class.fields %}
    {{ field.type }} m_{{ field.name | snake_case }};
{%- endfor %}
{%- endif %}
};
