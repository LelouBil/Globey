import logging

import Globey
import requests

log = logging.getLogger(__name__)

basepath = "https://discordapp.com/api/v6/"

useragent = "Globey ('http://discord.gg/invite/U4urVYr','1.0')"

headers = {
    'Authorization': "Bot " + Globey._token,
    'user-agent': useragent
}


def get_endpoint(endpoint: str, params=None):
    if params is None:
        params = {}
    Globey.l().debug("GETting endpoint %s with %s", endpoint, params)
    rep = requests.get(basepath + endpoint, params=params, headers=headers)
    if not rep:
        raise ApiError(rep)
    return rep


def post_endpoint(endpoint: str, data=None):
    if data is None:
        data = {}
    hd = headers
    hd["content-type"] = "application/json"
    Globey.l().debug("POSTing endpoint %s with %s", endpoint, data)
    rep = requests.post(basepath + endpoint, json=data, headers=hd)
    if not rep:
        raise ApiError(rep)
    return rep


def delete_endpoint(endpoint: str):
    Globey.l().debug("DELETEing endpoint %s", endpoint)
    rep = requests.delete(basepath + endpoint)
    if not rep:
        raise ApiError(rep)
    return rep


class ApiError(Exception):
    code: int
    rep: requests.Response

    def __init__(self, rep: requests.Response):
        self.code = rep.status_code
        self.rep = rep

    def stacktrace(self) -> str:
        return str(self.rep)
