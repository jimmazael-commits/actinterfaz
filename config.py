import os
DB_CFG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'JIMMazae213#18'),
    'database': os.getenv('DB_NAME', 'punto_venta')
}
