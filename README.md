# OAuth2 OIDC PKCE

A full-stack demonstration of OAuth2 authorization code flow with PKCE (Proof Key for Code Exchange) support. This project includes both a Django-based OAuth2 provider server and a React-based client application.

## Features

- OAuth2 Authorization Code Flow with PKCE
- OpenID Connect (OIDC) support
- JWT Access Tokens
- Refresh Token support
- User authentication and registration
- Token introspection and revocation
- Modern UI with Tailwind CSS and shadcn/ui components

## Tech Stack

### Backend

- Django 5.1
- Django OAuth Toolkit
- Django REST Framework
- PostgreSQL
- JWT for token signing

### Frontend

- React 18
- TypeScript
- Vite
- TanStack Query
- Tailwind CSS
- shadcn/ui components

## Prerequisites

- Python 3.8+
- Node.js 16+
- pnpm
- PostgreSQL

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/rezashahnazar/oauth2-pkce-demo.git
cd oauth2-pkce-demo
```

2. Set up the backend:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with required variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

3. Set up the frontend:

```bash
cd frontend

# Install dependencies
pnpm install

# Start the development server
pnpm dev
```

4. Create an OAuth2 application:
   - Visit `http://localhost:8000/admin`
   - Log in with your superuser credentials
   - Navigate to OAuth2 Provider > Applications
   - Create a new application with:
     - Client Type: Public
     - Authorization Grant Type: Authorization code
     - Redirect URIs: http://localhost:5173/callback

## Environment Variables

### Backend (.env)

```plaintext
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Frontend (.env)

```plaintext
VITE_OAUTH_CLIENT_ID=your-client-id
VITE_OAUTH_REDIRECT_URI=http://localhost:5173/callback
VITE_OAUTH_AUTHORITY=http://localhost:8000
```

## API Endpoints

### OAuth2 Endpoints

- Authorization: `/o/authorize/`
- Token: `/o/token/`
- Revoke Token: `/o/revoke/`
- Introspect Token: `/o/introspect/`
- UserInfo (OIDC): `/o/userinfo/`

### Account Management

- Sign Up: `/accounts/signup/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`

## Security Considerations

- PKCE is enforced for all authorization code flows
- JWT tokens are signed using RSA keys
- Access tokens expire after 1 hour
- Refresh tokens expire after 24 hours
- CORS is configured for local development
- SSL/TLS should be enabled in production

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Reza Shahnazar - [GitHub](https://github.com/rezashahnazar) - [Email](mailto:reza.shahnazar@gmail.com)
