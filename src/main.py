from app import app


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({"id": person.id, "name": person.name}), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify({"id": planet.id, "name": planet.name}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email} for u in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(1)  # Suponemos que el usuario con ID 1 es el actual
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    results = []
    for fav in favorites:
        if fav.planet_id:
            planet = Planet.query.get(fav.planet_id)
            results.append({"type": "planet", "name": planet.name})
        if fav.people_id:
            person = People.query.get(fav.people_id)
            results.append({"type": "people", "name": person.name})
    return jsonify(results), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    new_fav = Favorite(user_id=1, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    new_fav = Favorite(user_id=1, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Person added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": "Planet removed from favorites"}), 200
    return jsonify({"msg": "Favorite not found"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    fav = Favorite.query.filter_by(user_id=1, people_id=people_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": "Person removed from favorites"}), 200
    return jsonify({"msg": "Favorite not found"}), 404
