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


@app.route("/check-result", methods=["POST"])
def check():
    ip_address = request.form.get("ip_address")
    dict_result = check_access_sessions.main(ip_address)
    return render_template("check-result.html", dict_result=dict_result)


@app.route("/mac/<mac>", methods=["GET", "POST"])
def search_ise(mac):
    endpoint_group_name = 'Unknown'
    ise_groups = ise_api.get_group_id()
    print(ise_groups)
    endpoint_group_id = ise_api.get_endpoint_group_id(mac)
    for group_id, group_name in ise_groups.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if group_id == endpoint_group_id:
            endpoint_group_name = group_name
    return render_template("update-mac.html", mac=mac, endpoint_group_id=endpoint_group_name, ise_groups=ise_groups)


@app.route("/update/<mac>", methods=["POST"])
def update_ise(mac):

    ise_group_id = request.form.get("ise_group_id")
    result = ise_api.update_endpoint_group(mac, ise_group_id)
    if result.status_code == 200:
        update_result = True
    else:
        update_result = False
    return render_template("update-result.html", result=update_result)


@app.route("/endpoint", methods=["POST"])
def search_endpoint():
    mac_check = True
    mac = request.form.get("mac")
    endpoint_group_name = 'Unknown'
    normalized_mac = ise_api.mac_normalization(mac, '.')
    if normalized_mac == 'Error':
        mac_check = False
        return render_template("update-mac.html", mac_check=mac_check, mac=mac)
    ise_groups = ise_api.get_group_id()
    endpoint_group_id = ise_api.get_endpoint_group_id(mac)
    for group_id, group_name in ise_groups.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if group_id == endpoint_group_id:
            endpoint_group_name = group_name
    return render_template("update-mac.html", mac_check=mac_check, mac=mac, endpoint_group_id=endpoint_group_name, ise_groups=ise_groups)