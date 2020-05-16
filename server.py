import os
import sys
from flask import Flask, render_template, send_from_directory

ROOT_FOLDER = sys.argv[1]

app = Flask(__name__)


@app.route("/")
def folder_content():
    files = []
    for filename in os.listdir(ROOT_FOLDER):
        path = os.path.join(ROOT_FOLDER, filename)
        if os.path.isfile(path) or os.path.isdir(path):
            files.append(filename)
    rendered = render_template('index.html', files=files)
    return rendered


@app.route("/<path:subpath>")
def subfolder_content(subpath):
    whole_path = os.path.join(ROOT_FOLDER, subpath)
    subpath_is_file = os.path.isfile(whole_path)
    if os.path.exists(whole_path):
        if subpath_is_file:
            return send_from_directory(ROOT_FOLDER, subpath, as_attachment=True)
        else:
            files = {}
            for filename in os.listdir(whole_path):
                if os.path.isfile(whole_path) or os.path.isdir(whole_path):
                    files[filename] = subpath
            rendered = render_template('current_folder.html', files=files)
            return rendered
    else:
        rendered = render_template("not_found.html")
        return rendered, 404


@app.route("/<path:subpath>", methods=["MKCOL"])
def create_folder(subpath):
    whole_path = os.path.join(ROOT_FOLDER, subpath)
    if not os.path.exists(whole_path):
        os.makedirs(whole_path)
        rendered = render_template('folder_create.html', subpath=subpath)
        return rendered, 201
    else:
        rendered = render_template('folder_exists.html')
        return rendered, 400


@app.route("/<path:subpath>", methods=["DELETE"])
def delete_folder(subpath):
    whole_path = os.path.join(ROOT_FOLDER, subpath)
    if os.path.exists(whole_path):
        os.rmdir(whole_path)
        rendered = render_template("folder_delete.html")
        return rendered, 204
    else:
        rendered = render_template("not_found.html")
        return rendered, 404


if __name__ == "__main__":
    app.run(debug=True, port=8888)