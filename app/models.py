from . import db

class Tema(db.Model):
    __tablename__ = 'temas'
    id_tema = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.String(255), nullable=False)

class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.Text, nullable=False)
    id_tema = db.Column(db.Integer, db.ForeignKey('temas.id_tema'))
    fecha_publicacion = db.Column(db.DateTime, server_default=db.func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False) 


class Respuesta(db.Model):
    __tablename__ = 'respuestas'
    id = db.Column(db.Integer, primary_key=True)
    respuesta = db.Column(db.Text, nullable=False)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id'))
    fecha_publicacion = db.Column(db.DateTime, server_default=db.func.now())

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)

class Voto(db.Model):
    __tablename__ = 'votos'
    id_voto = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id'))
    id_respuesta = db.Column(db.Integer, db.ForeignKey('respuestas.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_voto = db.Column(db.DateTime, server_default=db.func.now())
    __table_args__ = (
        db.UniqueConstraint('id_usuario', 'id_pregunta', name='uq_usuario_pregunta'),
    )

class UsuarioPregunta(db.Model):
    __tablename__ = 'usuarios_preguntas'

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id'), primary_key=True)
    fecha_voto = db.Column(db.DateTime, server_default=db.func.now())
