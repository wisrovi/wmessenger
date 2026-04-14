from wauth import WAuth

from wconnect import WFile, WMessage, Wtelegram

with Wtelegram(auth_instance=WAuth(db_path="./my_secrets.db")) as producer:
    producer.send(to="USER_ID", message="✅ Operación completada con éxito")

    # Enviar desde una ruta local
    producer.send_image(
        to="USER_ID", path="./reports/graph.png", caption="Gráfico de ClickHouse"
    )

    # Enviar desde una URL
    producer.send_image(to="USER_ID", url="https://wisrovi.dev/logo.png")

    # Enviar un reporte generado
    producer.send_document(
        to="USER_ID",
        path="./exports/data_lts.zip",
        caption="📦 Aquí tienes el backup solicitado",
    )

    data_bytes = b"col1,col2\nval1,val2\nval3,val4"
    my_file = WFile(content=data_bytes, name="report.csv")
    producer.send_document(to="USER_ID", file=my_file)
