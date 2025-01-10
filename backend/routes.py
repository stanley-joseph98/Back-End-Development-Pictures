from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures."""
    if data:
        return jsonify(data), 200  # Return the list of pictures as JSON
    return jsonify({"message": "No pictures found"}), 404  # Return a 404 if no pictures are found

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by its ID."""
    index = id - 1  # Adjust for 0-based index
    if 0 <= index < len(data):
        return jsonify(data[index]), 200  # Return the picture at the specified index
    return jsonify({"message": "Picture not found"}), 404  # Return a 404 if the picture is not found


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture."""
    new_picture = request.get_json()

    # Check if the new picture has an 'id'
    if 'id' not in new_picture:
        return jsonify({"message": "ID is required"}), 400  # Bad request if ID is missing

    # Check if a picture with the same ID already exists
    for picture in data:
        if picture['id'] == new_picture['id']:
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    # Append the new picture to the data list
    data.append(new_picture)

    # Optionally, you might want to save the updated data back to the JSON file here

    return jsonify(new_picture), 201  # Return the created picture with a 201 status code

    
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture by its ID."""
    # Extract picture data from the request body
    updated_picture = request.get_json()

    # Find the picture in the data list
    for index, picture in enumerate(data):
        if picture['id'] == id:
            # Update the picture with the new data
            data[index] = updated_picture
            return jsonify(updated_picture), 200  # Return the updated picture with a 200 status code

    # If the picture is not found, return a 404 response
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its ID."""
    # Find the picture in the data list
    for index, picture in enumerate(data):
        if picture['id'] == id:
            del data[index]  # Delete the picture from the list
            return '', 204  # Return an empty body with a 204 No Content status

    # If the picture is not found, return a 404 response
    return jsonify({"message": "Picture not found"}), 404
