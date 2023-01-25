# MAIL CONFIRMATION SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Utilisation de GMAIL
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'matthieu.portelli@gmail.com'
EMAIL_HOST_USER = 'matthieu.portelli@gmail.com'
EMAIL_HOST_PASSWORD = 'krdioyckvjcgopuz'
EMAIL_PORT = 587
# Indique si une connexion TLS (sécurisée) doit être utilisée pour le dialogue avec le serveur SMTP
EMAIL_USE_TLS = True
# Délai avant expiration du token
PASSWORD_RESET_TIMEOUT = 14400
