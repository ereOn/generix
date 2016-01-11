#pragma once

namespace {{ namespace }} {
    class {{ class.name }} {
        public:
            {{ class.name }}();

        private:
            {%- for field in class.fields.private %}
            {{ field.type }} m_{{ field.name }};
            {%- endfor %}
    };
}
