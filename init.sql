SELECT 'CREATE DATABASE apiwarehousedb' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'apiwarehousedb')\gexec
