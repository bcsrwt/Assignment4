# python imports
# third-party imports
import json

from flask import Flask, jsonify, make_response
from flask import request
from dotenv import load_dotenv
import commands

load_dotenv()

app = Flask(__name__)


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


@app.route('/delete<int:bookmark_id>', methods=['DELETE'])
def get_bookmark_id_for_deletion(bookmark_id):
    commands.DeleteBookmarkCommand()
    prep_call = bookmark_id
    return jsonify({'result': True})


@app.route("/import", methods=['GET', 'POST'])
def get_github_import_options():
    data = request.get_json(force=True)
    github_username = data['github_username']
    preserve_timestamps = data['preserve_timestamps']
    data = {
        "github_username": github_username,
        "preserve_timestamps": preserve_timestamps
    }
    return jsonify({'data': data}), 201


# get bookmark information
@app.route("/new_info", methods=['GET', 'POST'])
def get_new_bookmark_info():
    data = request.get_json(force=True)
    bookmark_id = data['bookmark_id']
    field = data['field']
    new_value = data['new_value']
    updated_data = {
        "id": bookmark_id,
        "update": {field: new_value},
    }
    commands.EditBookmarkCommand()
    prep_call = updated_data
    return jsonify({'updated_data': updated_data}), 201


# error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# home
@app.route("/")
def run_commands():
    commands.CreateBookmarksTableCommand().execute()
    return "Bookmarks Created!"


options = [

    {"A": "Add a bookmark"},
    {"B": "List bookmarks by date"},
    {"T": "List bookmarks by title"},
    {"E": "Edit a bookmark"},
    {"D": "Delete a bookmark"},
    {"G": "Import GitHub stars"}

]


# list all the options
@app.route('/options', methods=['GET'])
def get_options():
    return jsonify({'options': options})


# get bookmarks
@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    data = commands.ListBookmarksCommand()
    print(data)
    return jsonify({'result': True})


# create a bookmark
@app.route("/create", methods=['GET', 'POST'])
def get_new_bookmark_data():
    data = request.get_json(force=True)
    print(data)
    title = data['title']
    url = data['url']
    notes = data['notes']
    bookmark = {
        "title": title,
        "url": url,
        "notes": notes
    }
    commands.AddBookmarkCommand()
    prep_call = bookmark
    return jsonify({'bookmark': bookmark}), 201


# edit bookmarks
@app.route("/edit", methods=['POST'])
def edit_bookmark_data():
    data = request.get_json()
    title = data['title']
    url = data['url']
    notes = data['notes']
    bookmark = {
        "title": title,
        "url": url,
        "notes": notes
    }
    commands.EditBookmarkCommand()
    prep_call = bookmark
    return jsonify({'bookmark': bookmark}), 201


if __name__ == "__main__":
    app.run()
