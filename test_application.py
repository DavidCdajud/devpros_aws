import unittest
from application import application, db
from model import Blacklist

class BlacklistTestCase(unittest.TestCase):

    def setUp(self):
        # Configurar la aplicación para pruebas
        application.config['TESTING'] = True
        self.app = application.test_client()

        # Crear las tablas de prueba
        with application.app_context():
            db.create_all()

        # Obtener un token JWT válido
        login_response = self.app.post('/login')
        self.token = login_response.json['access_token']

    def tearDown(self):
        # Limpiar la base de datos después de cada prueba
        with application.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_email_to_blacklist(self):
        # Prueba del endpoint POST /blacklists
        response = self.app.post('/blacklists', json={
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam"
        }, headers={'Authorization': f'Bearer {self.token}'})
        
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Email added to blacklist", response.data)

    def test_check_email_in_blacklist(self):
        # Prueba del endpoint GET /blacklists/{email}
        # Agregar un email a la lista negra
        self.app.post('/blacklists', json={
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam"
        }, headers={'Authorization': f'Bearer {self.token}'})

        # Consultar el email
        response = self.app.get('/blacklists/user@example.com', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"true", response.data)

if __name__ == '__main__':
    unittest.main()
