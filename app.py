import falcon
import csv
import io
from schema import Item
from pydantic import ValidationError
from falcon import HTTPUnauthorized
from falcon import before
from hooks.hook import auth_required
from custom_error_handler import handle_value_error, handle_unauthorized_error, handle_generic_exception

items = []  # Mock database


class ItemResource:
    # I added a format parameter
    def on_get(self, req, resp, format=None):
        if format == "csv":
            if not items:
                csv_data = ""
            else:
                #convert to CSV 
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=items[0].keys())
                writer.writeheader()
                writer.writerows(items)
                csv_data = output.getvalue()
                output.close()

            resp.status = falcon.HTTP_200
            resp.content_type = 'text/csv'
            resp.text = csv_data

        else: 
            #default output
            resp.status = falcon.HTTP_200
            resp.media = {"items": items}

    @before(auth_required)
    def on_post(self, req, resp):

        raw_data = req.media
        item = Item(**raw_data)
        items.append(item.model_dump())

        log_item_addition(item.model_dump())

        resp.status = falcon.HTTP_201
        resp.media = {
            "message": "Item added successfully",
            "item": item.model_dump()
        }


def log_item_addition(item):
    print(f"Logged item: {item}")


app = falcon.App()


app.add_route("/items", ItemResource())
app.add_route("/items/{format}", ItemResource())
# Custon ERROR
app.add_error_handler(ValidationError, handle_value_error)
app.add_error_handler(HTTPUnauthorized, handle_unauthorized_error)
app.add_error_handler(Exception, handle_generic_exception)