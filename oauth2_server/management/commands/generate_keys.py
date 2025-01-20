from django.core.management.base import BaseCommand
import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class Command(BaseCommand):
    help = 'Generate RSA key pair for JWT signing'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='Force regenerate keys even if they already exist',
        )

    def handle(self, *args, **options):
        base_dir = Path(os.getcwd())
        private_key_path = base_dir / 'private.pem'
        public_key_path = base_dir / 'public.pem'

        # Check if keys already exist
        if private_key_path.exists() or public_key_path.exists():
            if not options['force']:
                self.stdout.write(
                    self.style.WARNING(
                        '\nRSA keys already exist! You have two options:\n'
                        '1. Use --force (-f) flag to regenerate keys\n'
                        '2. Delete existing key files manually\n\n'
                        f'Private key path: {private_key_path}\n'
                        f'Public key path: {public_key_path}\n'
                    )
                )
                return

            # If force flag is used, delete existing keys
            if private_key_path.exists():
                private_key_path.unlink()
                self.stdout.write(self.style.WARNING('Removed existing private key'))
            
            if public_key_path.exists():
                public_key_path.unlink()
                self.stdout.write(self.style.WARNING('Removed existing public key'))

        # Generate private key
        self.stdout.write('Generating RSA key pair...')
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Save private key
        with open(private_key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Save public key
        public_key = private_key.public_key()
        with open(public_key_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        # Set appropriate file permissions
        os.chmod(private_key_path, 0o600)
        os.chmod(public_key_path, 0o644)

        self.stdout.write(self.style.SUCCESS('\nRSA key pair generated successfully!'))
        self.stdout.write(
            self.style.SUCCESS(
                f'\nPrivate key saved to: {private_key_path}\n'
                f'Public key saved to: {public_key_path}\n'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nIMPORTANT: Keep your private key secure and never commit it to version control!'
            )
        ) 