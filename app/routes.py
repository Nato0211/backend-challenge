from flask import Blueprint, request, jsonify
from .models import Pregunta, Respuesta, Tema, Usuario, Voto, UsuarioPregunta
from app import db
from flask import Blueprint, jsonify
main = Blueprint('main', __name__)

@main.route('/add_pregunta', methods=['POST'])
def add_pregunta():
    data = request.get_json()
    id_tema = data.get('id_tema')
    id_usuario = data.get('id_usuario')
    respuestas = data.get('respuestas', [])  

    if not id_tema or not id_usuario:
        return jsonify({'error': 'Faltan datos necesarios para la creación de la pregunta'}), 400

    if len(respuestas) != 4:
        return jsonify({'error': 'Se deben proporcionar exactamente 4 respuestas para la pregunta'}), 400

    nueva_pregunta = Pregunta(pregunta=data['pregunta'], id_tema=id_tema, id_usuario=id_usuario)
    db.session.add(nueva_pregunta)
    db.session.commit()

    for respuesta_texto in respuestas:
        nueva_respuesta = Respuesta(respuesta=respuesta_texto, id_pregunta=nueva_pregunta.id)
        db.session.add(nueva_respuesta)
    db.session.commit()

    return jsonify({'message': 'Pregunta y respuestas creadas exitosamente'}), 201


@main.route('/temas', methods=['GET'])
def get_temas():
    todos_los_temas = Tema.query.all()
    temas = [{'id_tema': tema.id_tema, 'tema': tema.tema} for tema in todos_los_temas]
    return jsonify(temas)

@main.route('/preguntas', methods=['GET'])
def get_preguntas():
    todas_preguntas = Pregunta.query.all()
    preguntas = [{'id': pregunta.id, 'pregunta': pregunta.pregunta} for pregunta in todas_preguntas]
    return jsonify(preguntas)

@main.route('/respuestas/<int:id_pregunta>', methods=['GET'])
def get_respuestas_por_pregunta(id_pregunta):
    pregunta = Pregunta.query.get(id_pregunta)
    if not pregunta:
        return jsonify({'error': 'La pregunta especificada no existe.'}), 404

    respuestas = Respuesta.query.filter_by(id_pregunta=id_pregunta).all()
    if not respuestas:
        return jsonify({'message': 'No se encontraron respuestas para esta pregunta'}), 404

    resultado = []
    for respuesta in respuestas:
        cantidad_votos = Voto.query.filter_by(id_respuesta=respuesta.id).count()
        respuesta_data = {
            'id': respuesta.id,
            'respuesta': respuesta.respuesta,
            'fecha_publicacion': respuesta.fecha_publicacion,
            'cantidad_votos': cantidad_votos  
        }
        resultado.append(respuesta_data)

    return jsonify(resultado)


@main.route('/add_voto', methods=['POST'])
def add_voto():
    data = request.get_json()

    id_pregunta = data.get('id_pregunta')
    id_respuesta = data.get('id_respuesta')
    id_usuario = data.get('id_usuario')

    if not id_pregunta or not id_respuesta or not id_usuario:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    voto_existente = Voto.query.filter_by(id_usuario=id_usuario, id_pregunta=id_pregunta).first()
    if voto_existente:
        return jsonify({'error': 'El usuario ya ha votado en esta pregunta'}), 409

    try:
        nuevo_voto = Voto(
            id_pregunta=id_pregunta,
            id_respuesta=id_respuesta,
            id_usuario=id_usuario
        )
        db.session.add(nuevo_voto)
        db.session.commit()

        return jsonify({'message': 'Voto registrado con éxito'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    nombre_usuario = data.get('nombre_usuario')
    correo_electronico = data.get('correo_electronico')

    if not nombre_usuario or not correo_electronico:
        return jsonify({'error': 'Faltan datos obligatorios (nombre_usuario o correo_electronico)'}), 400

    usuario_existente = Usuario.query.filter(
        (Usuario.nombre_usuario == nombre_usuario) | (Usuario.correo_electronico == correo_electronico)
    ).first()

    if usuario_existente:
        return jsonify({'error': 'El usuario ya está registrado'}), 409

    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        correo_electronico=correo_electronico
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado con éxito'}), 201

@main.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')

    if not nombre_usuario:
        return jsonify({'error': 'El nombre de usuario es obligatorio'}), 400

    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    if not usuario:
        return jsonify({'error': 'El usuario no existe'}), 404

    return jsonify({
        'message': f'Bienvenido, {usuario.nombre_usuario}!',
        'id_usuario': usuario.id_usuario
    }), 200

@main.route('/usuarios', methods=['GET'])
def get_usuarios():
    todos_los_usuarios = Usuario.query.all()
    usuarios = [{'id_usuario': usuario.id_usuario, 'nombre_usuario': usuario.nombre_usuario} for usuario in todos_los_usuarios]
    return jsonify(usuarios)