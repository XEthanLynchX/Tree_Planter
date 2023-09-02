from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

from flask import flash

db = 'tree'

class Tree:
  def __init__( self , db_data ):
    self.id = db_data['id']
    self.user_id = db_data['user_id']
    self.species = db_data['species']
    self.location = db_data['location'] 
    self.reason = db_data['reason']
    self.date_planted = db_data['date_planted']
    self.created_at = db_data['created_at']
    self.updated_at = db_data['updated_at']
    self.creator = None

  @classmethod
  def save_tree(cls, form_data):
    query= 'INSERT INTO tree(species, location, reason, date_planted, user_id) VALUES( %(species)s, %(location)s, %(reason)s, %(date_planted)s, %(user_id)s );'
    return connectToMySQL(db).query_db(query, form_data)   

  @classmethod
  def get_all(cls): 
    query = "SELECT * FROM tree JOIN user_info ON tree.user_id = user_info.id;"
    results = connectToMySQL(db).query_db(query)
    trees = []
    for row in results:
            
      one_tree = cls(row)
            
      one_trees_author_info = {
          "id": row['user_info.id'], 
          "first_name": row['first_name'],
          "last_name": row['last_name'],
          "email": row['email'],
          "password": row['password'],
          "created_at": row['user_info.created_at'],
          "updated_at": row['user_info.updated_at']
        }
      author = user.User(one_trees_author_info)
      one_tree.creator = author
      trees.append(one_tree)
    return trees


  @classmethod
  def update(cls,form_data):
    query = """
        UPDATE tree
        SET species = %(species)s,
        location = %(location)s,
        reason = %(reason)s ,
        date_planted = %(date_planted)s
        WHERE (id = %(id)s);
            """
    return connectToMySQL(db).query_db(query,form_data)

  @classmethod
  def get_id(cls,data):
    query = """
            SELECT * FROM tree
            JOIN user_info on tree.user_id = user_info.id
            WHERE tree.id = %(id)s;
            """
    result = connectToMySQL(db).query_db(query,data)
    if not result:
      return False

    result = result[0]
    this_tree = cls(result)
    user_data = {
              "id": result['user_info.id'],
              "first_name": result['first_name'],
              "last_name": result['last_name'],
              "email": result['email'],
              "password": "",
              #make a new variable on exam for date_made
              "created_at": result['user_info.created_at'],
              "updated_at": result['user_info.updated_at']
        }
    this_tree.creator = user.User(user_data)
    return this_tree

  @classmethod
  def destroy(cls,data):
    query = """
      DELETE FROM tree
      WHERE id = %(id)s;
      """
    return connectToMySQL(db).query_db(query,data)

  @staticmethod
  def validate_tree(form_data):
    is_valid = True

    if len(form_data['species']) < 5:
      flash("Species must be at least 5 characters long.")
      is_valid = False
    if len(form_data['location']) < 3:
      flash("Location must be at least 2 characters long.")
      is_valid = False
    if len(form_data['reason']) > 50:
      flash("Your reason can't exceed 50 characters long.")
      is_valid = False
    if len(form_data['reason']) < 5:
      flash("Your reason must be at least 5 characters long.")
      is_valid = False
    if form_data['date_planted'] == '':
      flash("Please input a date.")
      is_valid = False

    return is_valid