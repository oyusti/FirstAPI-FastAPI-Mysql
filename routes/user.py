from fastapi import APIRouter, HTTPException
from config.db import conn
from models.user import users
from schemas.user import User, UserResponse, UserMsgStr
import bcrypt

user = APIRouter()

@user.get("/users", response_model=list[User], tags=["Users"])
def get_users():
    return conn.execute(users.select()).mappings().fetchall()
    
@user.post("/users", response_model=User, tags=["Users"])
def create_user(user:User):
    try:
        # Crear el diccionario del nuevo usuario
        new_user = {"name": user.name, "email": user.email}
        new_user["password"] = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Ejecutar la inserción en la base de datos
        result = conn.execute(users.insert().values(new_user))
    
        #confirmar la transaccion
        conn.commit()

        # Confirmar la inserción
        if result.rowcount == 0:
            raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
        
        user_created = dict(conn.execute(users.select().where(users.c.id == result.lastrowid)).mappings().first())
        
        return{"user": user_created,
                "msg": "Usuario creado correctamente"}

    except Exception as e:
        # Manejar cualquier excepción y devolver un mensaje de error
        raise HTTPException(status_code=500, detail=str(e))

@user.get("/users/{id}", response_model=User, tags=["Users"])
def get_user(id:int):
    result = conn.execute(users.select().where(users.c.id == id)).mappings().first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Convertir el resultado a un diccionario
    user_dict = dict(result)
    return user_dict

@user.delete("/users/{id}", response_model=UserMsgStr, tags=["Users"])
def delete_user(id:int):
    result = conn.execute(users.delete().where(users.c.id == id))
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    conn.commit()
    return {"msg": "Usuario eliminado correctamente"}

@user.put("/users/{id}", response_model=UserResponse, tags=["Users"])
def helloWorld(id:int, user:User):
    try:
        # Crear el diccionario del nuevo usuario
        new_user = {"name": user.name, "email": user.email}
        new_user["password"] = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Ejecutar el update en la base de datos
        result = conn.execute(users.update().where(users.c.id == id).values(new_user))
    
        #confirmar la transaccion
        conn.commit()

        # Confirmar la inserción
        if result.rowcount == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        
        user_updated = dict(conn.execute(users.select().where(users.c.id == id)).mappings().first())
        
        return {"user": user_updated,
                "msg": "Usuario actualizado correctamente"}

    except Exception as e:
        # Manejar cualquier excepción y devolver un mensaje de error
        raise HTTPException(status_code=500, detail=str(e))