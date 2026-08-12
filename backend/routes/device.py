from flask import Blueprint, request, jsonify

from models.device import (
    get_all_devices,
    get_device_by_id,
    add_device
)


devices_bp = Blueprint(
    "devices",
    __name__,
    url_prefix="/api/devices"
)


# ==========================================
# GET ALL DEVICES
# ==========================================

@devices_bp.route(
    "",
    methods=["GET"]
)
def devices():

    try:

        device_list = get_all_devices()


        return jsonify({

            "success": True,

            "devices": device_list

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# ==========================================
# GET ONE DEVICE
# ==========================================

@devices_bp.route(
    "/<int:device_id>",
    methods=["GET"]
)
def device(device_id):

    try:

        result = get_device_by_id(
            device_id
        )


        if not result:

            return jsonify({

                "success": False,

                "message":
                    "Device not found."

            }), 404


        return jsonify({

            "success": True,

            "device": result

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# ==========================================
# ADD DEVICE
# ==========================================

@devices_bp.route(
    "/add",
    methods=["POST"]
)
def add():

    data = request.get_json() or {}


    device_code = data.get(
        "device_code",
        ""
    ).strip()


    device_name = data.get(
        "device_name",
        ""
    ).strip()


    quantity = data.get(
        "quantity"
    )


    if not device_code:

        return jsonify({

            "success": False,

            "message":
                "Device code is required."

        }), 400


    if not device_name:

        return jsonify({

            "success": False,

            "message":
                "Device name is required."

        }), 400


    try:

        quantity = int(quantity)

    except:

        return jsonify({

            "success": False,

            "message":
                "Quantity must be a number."

        }), 400


    if quantity < 0:

        return jsonify({

            "success": False,

            "message":
                "Quantity cannot be negative."

        }), 400


    try:

        device_id = add_device(
            device_code,
            device_name,
            quantity
        )


        return jsonify({

            "success": True,

            "message":
                "Device added successfully.",

            "device_id":
                device_id

        }), 201


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500