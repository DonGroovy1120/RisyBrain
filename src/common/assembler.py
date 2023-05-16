# assembler to mapping data into another data type.
from flask import jsonify

from src.model.basic_model import BasicModel


class Assembler:
    # mapping to BasicModel
    def to_basic_model(self, data: any) -> BasicModel:
        model = BasicModel(data["image_name"], data["message"])
        return model

    # mapping to http response
    def to_response(self, code, message, result) -> any:
        response = jsonify({"message": message, "result": result})
        response.status_code = code
        return response
