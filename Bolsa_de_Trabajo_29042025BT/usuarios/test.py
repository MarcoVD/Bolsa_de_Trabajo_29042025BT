# usuarios/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UsuarioTests(TestCase):
    def test_crear_usuario_interesado(self):
        """Prueba la creación de un usuario interesado"""
        data = {
            'username': 'test_interesado',
            'email': 'interesado@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        response = self.client.post(reverse('registro_interesado'), data)

        # Verificar redirección exitosa
        self.assertEqual(response.status_code, 302)

        # Verificar que el usuario fue creado
        self.assertTrue(User.objects.filter(username='test_interesado').exists())

        # Verificar que el rol es correcto
        user = User.objects.get(username='test_interesado')
        self.assertEqual(user.rol, 'interesado')