import os

from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
import check_access_sessions
import ise_api

app = Flask(__name__, static_url_path='/static')

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("main.html")


@app.route("/check", methods=["POST"])
def check():
    ip_address = request.form.get("ip_address")
    dict_result = check_access_sessions.main(ip_address)
    #return jsonify(dict_result)
    return render_template("result.html", dict_result=dict_result)

@app.route("/search/<mac>", methods=["GET", "POST"])
def search_ise(mac):
    ise_groups = ise_api.get_group_id()
    return render_template("update-mac.html", mac=mac, ise_groups=ise_groups)

@app.route("/update/<mac>", methods=["POST"])
def update_ise(mac):

    ise_group_id = request.form.get("ise_group_id")
    result = ise_api.update_endpoint_group(mac, ise_group_id)
    if result.status_code == 200:
        update_result = True
    else:
        update_result = False
    return render_template("update-result.html", result=update_result)
