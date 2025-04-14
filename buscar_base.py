from mongo_con import collection

def buscar(usuario, password):
    todos_users = collection.find()
    for user in todos_users:
        if user["user"] == usuario and user["password"] == password:
            print(f"{user["user"]} == {usuario}, {user["password"]} == {password}")
            return "Correcto"
    return "Incorrecto"