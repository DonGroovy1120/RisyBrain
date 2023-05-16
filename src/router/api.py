import json
import os

from flask import Blueprint, request, jsonify, send_from_directory

from src.common.assembler import Assembler
from src.langchain.chatbot import getCompletion, getTextFromImage, query_image_ask
from src.firebase.cloudmessage import send_message, get_tokens
from src.langchain.csv_embed import csv_embed
from src.langchain.image_embedding import embed_image_text, query_image_text
from src.model.basic_model import BasicModel
from src.model.feedback_model import FeedbackModel
from src.service.feedback_service import FeedbackService


def construct_blueprint_api(generator):
    api = Blueprint("send_notification", __name__)

    # Assembler
    assembler = Assembler()

    # Service
    feedback_service = FeedbackService()

    @generator.response(
        status_code=200, schema={"message": "message", "result": "test_result"}
    )
    @generator.request_body(
        {"message": "this is test message", "token": "test_token", "uuid": "test_uuid"}
    )
    @api.route("/sendNotification", methods=["POST"])
    def send_notification():
        data = json.loads(request.get_data())
        query = data["message"]
        token = data["token"]
        uuid = data["uuid"]

        result = getCompletion(query, uuid)

        notification = {"title": "alert", "content": result}

        state, value = send_message(notification, [token])
        response = jsonify({"message": value, "result": result})
        response.status_code = 200
        return response

    @generator.response(
        status_code=200, schema={"message": "message", "result": "test_result"}
    )
    @generator.request_body(
        {
            "image_name": "this is test image path",
            "token": "test_token",
            "uuid": "test_uuid",
        }
    )
    @api.route("/uploadImage", methods=["POST"])
    def upload_image():
        data = json.loads(request.get_data())
        image_name = data["image_name"]
        token = data["token"]
        uuid = data["uuid"]

        result = getTextFromImage(image_name)

        embed_result = embed_image_text(result, image_name, uuid)

        notification = {"title": "alert", "content": embed_result}

        state, value = send_message(notification, [token])
        response = jsonify({"message": value, "result": result})
        response.status_code = 200
        return response

    @generator.response(
        status_code=200, schema={"message": "message", "result": "test_result"}
    )
    @generator.request_body(
        {
            "image_name": "this is test image path",
            "message": "this is a test message",
            "token": "test_token",
            "uuid": "test_uuid",
        }
    )
    @api.route("/image_relatedness", methods=["POST"])
    def image_relatedness():
        data = json.loads(request.get_data())
        image_name = data["image_name"]
        message = data["message"]
        token = data["token"]
        uuid = data["uuid"]

        image_content = getTextFromImage(image_name)
        # check message type
        image_response = {}
        try:
            # check about asking image description with trained data
            if query_image_ask(image_content, message, uuid):
                image_response["image_desc"] = image_content
            else:
                relatedness_data = query_image_text(image_content, message, uuid)

                image_response["image_name"] = relatedness_data
        except ValueError as e:
            print("image_relatedness parsing error for message chain data")

        notification = {"title": "alert", "content": json.dumps(image_response)}
        state, value = send_message(notification, [token])
        response = jsonify(
            {
                "message": value,
                "result": json.dumps(
                    {
                        "program": "image",
                        "content": json.dumps(image_response),
                    }
                ),
            }
        )
        response.status_code = 200
        return response

    @api.route("/file/<string:filename>")
    def get_swagger_file(filename):
        print(os.getcwd() + "/src/static/")
        return send_from_directory(
            os.getcwd() + "/src/static/", path=filename, as_attachment=False
        )

    @generator.response(
        status_code=200, schema={"message": "message", "result": "test_result"}
    )
    @api.route("/training")
    def csv_training():
        csv_embed()

        return assembler.to_response(200, "trained successfully", "")

    @generator.request_body(
        {
            "token": "test_token",
            "uuid": "test_uuid",
            "prompt": {"image_name": "test_image", "message": "test_message"},
            "completion": {"image_name": "test_image", "message": "test_message"},
            "rating": 1,
        }
    )
    @generator.response(
        status_code=200, schema={"message": "message", "result": "test_result"}
    )
    @api.route("/feedback", methods=["POST"])
    def add_feedback():
        try:
            data = json.loads(request.get_data())
            token = data["token"]
            uuid = data["uuid"]

            # parsing feedback payload
            prompt = assembler.to_basic_model(data["prompt"])
            completion = assembler.to_basic_model(data["completion"])
            rating = data["rating"]
            feedback = FeedbackModel(uuid, prompt, completion, rating)

            # add the feedback
            feedback_service.add(feedback)
        except Exception as e:
            return assembler.to_response(400, "failed to add", "")
        return assembler.to_response(200, "added successfully", "")

    @generator.response(
        status_code=200, schema={"message": "message", "result": "test_result"}
    )
    @api.route("/feedback/<string:search>/<int:rating>")
    def get_feedback(search, rating):
        result = feedback_service.get(search, rating)
        return assembler.to_response(200, "added successfully", json.dumps(result))

    return api
