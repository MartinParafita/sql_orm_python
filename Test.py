from os import name
import sqlite3

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al menos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)
    Session = sessionmaker(bind=engine)
    session = Session()
    tutores = Tutor(name=name)
    session.add(tutores)
    session.commit()

    tutor1 = Tutor(name='Marcelo')
    tutor2 = Tutor(name='Gabriel')
    session.add(tutor1, tutor2)
    session.commit()
    print(tutor1, tutor2)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)
    estudiante1 = Estudiante(name='Lucas', age=18, grade=4, tutor=tutor2)
    session.add(estudiante1)
    estudiante2 = Estudiante(name='Tato', age=23, grade=6, tutor=tutor1)
    session.add(estudiante2)
    estudiante3 = Estudiante(name='Nacho', age=17, grade=2, tutor=tutor2)       #INTENTE HACERLO EN MODO DE LISTA A LOS ESTUDIANTES Y NO ME DEJABA
    session.add(estudiante3)
    estudiante4 = Estudiante(name='Tute', age=16, grade=3, tutor=tutor1)        #INTENTE TAMBIEN HACER EL SESSION.ADD CON TODOS LOS ESTUDIANTES JUNTOS, Y NO QUISO TAMPOCO
    session.add(estudiante4)
    estudiante5 = Estudiante(name='Micaela', age=20, grade=5, tutor=tutor1)         
    session.add(estudiante5)
    session.commit()


    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.


def fetch():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creaods de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
    Session = sessionmaker(bind=engine)
    session = Session()
    
    query = session.query(Estudiante)
    estudiantes = query.all()
    for estudiante in estudiantes:
        print(estudiante)

def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)
    for i in query:
        print(i)
    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name
    
    


def modify(id, nuevo_tutor):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Tutor).filter(Tutor.name == nuevo_tutor)
    tutorname = query.first()
    
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    query = session.query(Estudiante).filter(Estudiante.id == id)
    alumno = query.first()
    
    alumno.tutor = tutorname
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos
    
    session.add(alumno)
    session.commit()
    
        
    print("Estudiante con id {} fue actualizado, el nuevo tutor es {}".format(id, nuevo_tutor))
    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality


def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado
    Session = sessionmaker(bind=engine)
    session = Session()
    resultado = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print('La cantidad de cursantes del grado {} son: '.format(grade),resultado)
    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    # fill()
    fill()
    # fetch()
    fetch()
    tutor = 'Marcelo'
    # search_by_tutor(tutor)
    search_by_tutor(tutor)
    
    nuevo_tutor = 'Gabriel'
    id = 2
    # modify(id, nuevo_tutor)
    modify(id, nuevo_tutor)

    grade = 2
    # count_grade(grade)
    count_grade(grade)