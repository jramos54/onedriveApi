import pymssql

try:
    conn = pymssql.connect(server='CCAZR-ORIG01\\ORIG_PLATAFORMA', port='1433', user='RPAUsr.sql', password='H4y40M1y4z4k!24', database='MonitorISCAM')
    
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print("Error al conectar:", e)
