# -*- coding: utf-8 -*-

from jetkeys.signer import license_signer
from flask import Flask, request, Response

app = Flask(__name__)


class config(object):
    PROLONGATION_PERIOD = "607875500"


@app.route("/rpc/obtainTicket.action", methods=["GET"])
def obtain_ticket():
    app.logger.info("obtain a ticket: {}".format(request))
    params = {
        "build_date": request.args.get("buildDate", ""),
        "client_version": request.args.get("clientVersion", ""),
        "host_name": request.args.get("hostName", ""),
        "machine_id": request.args.get("machineId", ""),
        "product_code": request.args.get("productCode", ""),
        "product_family_id": request.args.get("productFamilyId", ""),
        "salt": request.args.get("salt", ""),
        "secure": request.args.get("secure", ""),
        "username": request.args.get("userName", ""),
        "version": request.args.get("version", ""),
        "version_number": request.args.get("versionNumber", "")
    }

    xml_resp = [
        "<ObtainTicketResponse><message></message><prolongationPeriod>",
        config.PROLONGATION_PERIOD,
        "</prolongationPeriod><responseCode>OK</responseCode><salt>",
        params['salt'],
        '</salt><ticketId>1</ticketId><ticketProperties>licensee=',
        params["username"].encode("utf-8"),
        '\tlicenseType=0\t',
        '</ticketProperties></ObtainTicketResponse>'
    ]
    xml_resp = "".join(xml_resp)

    signature = license_signer.generate_signature(xml_resp)
    full_response = signature + xml_resp
    app.logger.info("send: {}".format(full_response))
    return Response(full_response, mimetype="text/xml")


@app.route("/rpc/ping.action", methods=["GET"])
def ping():
    xml_response = [
        '<PingResponse><message></message><responseCode>OK</responseCode><salt>',
        request.args.get('salt', ''),
        '</salt></PingResponse>'
    ]
    response = "".join(xml_response)
    signature = license_signer.generate_signature(response)
    full_response = signature + response
    app.logger.info("send: {}".format(full_response))
    return Response(full_response, mimetype="text/xml")
