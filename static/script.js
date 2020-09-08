const API_ENDPOINT = 'http://localhost:8000/api';
const BASE_URL = 'http://localhost:8000';

$('.logout-btn').click(function (e) {
    e.preventDefault();

    $.get(`${API_ENDPOINT}/logout`);
    window.location.href = `{% url 'frontend:index' %}`
    window.location.reload();
});
