import os

from wauth import WAuth

from wconnect import WFile, Wtelegram

USER_ID = "6586101740"  # Reemplaza con tu ID de usuario de Telegram

with Wtelegram(auth_instance=WAuth(db_path="./my_secrets.db")) as producer:
    ok = producer.send(to=USER_ID, message="✅ Operación completada con éxito")
    print(
        f"Envío de mensaje: {'Éxito' if ok else 'Fallido (verifique token y USER_ID)'}"
    )

    # Enviar desde una ruta local (si existe el archivo)
    if os.path.exists("./reports/graph.png"):
        producer.send_image(
            to=USER_ID, path="./reports/graph.png", caption="Gráfico de ClickHouse"
        )

    # Enviar desde una URL
    ok_img = producer.send_image(to=USER_ID, url="https://httpbin.org/image/png")
    print(f"Envío de imagen: {'Éxito' if ok_img else 'Fallido'}")

    # Enviar un reporte generado (si existe el archivo)
    if os.path.exists("./exports/data_lts.zip"):
        producer.send_document(
            to=USER_ID,
            path="./exports/data_lts.zip",
            caption="📦 Aquí tienes el backup solicitado",
        )

    data_bytes = b"col1,col2\nval1,val2\nval3,val4"
    my_file = WFile(content=data_bytes, name="report.csv")
    ok_doc = producer.send_document(to=USER_ID, file=my_file)
    print(f"Envío de documento: {'Éxito' if ok_doc else 'Fallido'}")
