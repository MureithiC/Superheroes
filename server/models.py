from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # Relationship to HeroPower
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')

    # Serialize only relevant fields
    serialize_rules = ('-hero_powers', 'hero_powers.power')

    # Association proxy to access powers through hero_powers
    powers = association_proxy('hero_powers', 'power')

    def __repr__(self):
        return f'<Hero {self.id} {self.name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # Relationship to HeroPower
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')

    # Serialize only relevant fields
    serialize_rules = ('-hero_powers',)

    # Validation to ensure description is at least 20 characters
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

    def __repr__(self):
        return f'<Power {self.id} {self.name}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # Serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # Validation for strength to be either 'Strong', 'Weak', or 'Average'
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'