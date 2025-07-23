import falcon
import csv
import io
from schema import Item
from pydantic import ValidationError
from falcon import before
from hooks.hook import auth_required

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
        try:
            raw_data = req.media
            item = Item(**raw_data)
            items.append(item.model_dump())

            log_item_addition(item.model_dump())

            resp.status = falcon.HTTP_201
            resp.media = {
                "message": "Item added successfully",
                "item": item.model_dump()
            }

        except ValidationError as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": e.errors()}

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}


def log_item_addition(item):
    print(f"Logged item: {item}")


app = falcon.App()


app.add_route("/items", ItemResource())
app.add_route("/items/{format}", ItemResource())
