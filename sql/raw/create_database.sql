SELECT 'CREATE DATABASE social_network'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'social_network')\gexec
