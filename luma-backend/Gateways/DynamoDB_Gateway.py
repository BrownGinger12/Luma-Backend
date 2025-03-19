import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoDB:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource("dynamodb", "us-east-2")
        self.table = self.dynamodb.Table(table_name)
        
    def scan_table(self, attribute_name, attribute_value):
        """Scans the table for a specific attribute value."""
        try:
            response = self.table.scan(
                FilterExpression=Attr(attribute_name).eq(attribute_value)
            )

            return response.get("Items", [])
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    def item_exists(self, key):
        """Checks if an item exists in the table."""
        try:
            response = self.table.get_item(Key=key)
            return response.get("Item")
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}

    def put_item(self, item, item_id):
        """Inserts a new item only if it does not already exist."""

        if self.item_exists(item_id):
            return {"statusCode": 400, "message": "Item already exists"}
        
        try:
            self.table.put_item(Item=item)
            return {"statusCode": 200, "message": "Item added successfully"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}

    def get_item(self, key):
        """Fetches an item from the table using its key."""
        try:
            response = self.table.get_item(Key=key)
            if "Item" in response:
                return {"statusCode": 200, "data": response["Item"]}
            return {"statusCode": 404, "message": "Item not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}

    def get_all_items(self):
        """Fetches all items from the table."""
        try:
            response = self.table.scan()
            return {"statusCode": 200, "data": response.get("Items", [])}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}

    def update_item(self, key, update_expression, expression_values):
        """Updates an item only if it exists."""
        if not self.item_exists(key):
            return {"statusCode": 404, "message": "Item does not exist"}

        try:
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
            )
            return {"statusCode": 200, "message": "Item updated successfully"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}

    def delete_item(self, key):
        """Deletes an item only if it exists."""
        if not self.item_exists(key):
            return {"statusCode": 404, "message": "Item does not exist"}

        try:
            self.table.delete_item(Key=key)
            return {"statusCode": 200, "message": "Item deleted successfully"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}

    def query_items(self, product_id):
        """Queries items from DynamoDB using only the partition key (product_id)."""
        try:
            response = self.table.query(
                KeyConditionExpression=Key("product_id").eq(product_id)
            )
            return {"statusCode": 200, "data": response.get("Items", [])}

        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
