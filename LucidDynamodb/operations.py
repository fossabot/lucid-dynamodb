import boto3
import logging
class DynamoDb:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.db = boto3.resource(
            "dynamodb",
            region_name = region_name,
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key,
        )
        
    def create_table(self, TableName, KeySchema, AttributeDefinitions, ProvisionedThroughput, GlobalSecondaryIndexes=[]):
        """Create a new table

        Args:
            TableName (str): Table name
            KeySchema (list): A key schema specifies the attributes that make up the primary key of a table.
            AttributeDefinitions (list): An array of attributes that describe the key schema for the table.
            ProvisionedThroughput (dict): Provisioned throughput settings for this specified table. 
            GlobalSecondaryIndexes (list, optional): An index with a partition key and a sort key that can be different from those on the base table.

        Returns:
            bool: Table creation is successful or failed
        """
        try:
            if(len(GlobalSecondaryIndexes)>0):
                table = self.db.create_table(
                    TableName=TableName,
                    KeySchema=KeySchema,
                    AttributeDefinitions=AttributeDefinitions,
                    GlobalSecondaryIndexes=GlobalSecondaryIndexes,
                    ProvisionedThroughput=ProvisionedThroughput
                )
            else:
                table = self.db.create_table(
                    TableName=TableName,
                    KeySchema=KeySchema,
                    AttributeDefinitions=AttributeDefinitions,
                    ProvisionedThroughput=ProvisionedThroughput
                )
                # Wait until the table exists.
                table.meta.client.get_waiter('table_exists').wait(TableName=TableName)
            return True
        except Exception as e:
            logging.warning(e)
            return False

    def delete_table(self, TableName):
        """Delete a table

        Args:
            TableName (str): Table name

        Returns:
            bool: Table deletion is successful or failed
        """
        try:
            table = self.db.Table(TableName)
            table.delete()
            table.wait_until_not_exists()
            return True
        except Exception as e:
            logging.warning(e)
            return False
                
    def read_all_table_names(self):
        """Get all table names

        Returns:
            list: List of table names
        """
        try:
            db_client = boto3.client(
                "dynamodb",
                region_name = self.region_name,
                aws_access_key_id = self.aws_access_key_id,
                aws_secret_access_key = self.aws_secret_access_key,
            )
            table_names = db_client.list_tables()['TableNames']
            return table_names
        except Exception as e:
            logging.warning(e)
            return []

    def create_item(self, TableName ,Item):
        """Create a New Item

        Args:
            TableName (str): Table name
            Item (dict): Item with Primary key

        Returns:
            bool: Item creation is successful or failed
        """
        try:
            table = self.db.Table(TableName)
            table.put_item(Item=Item)
            return True
        except Exception as e:
            logging.warning(e)
            return False
        
    def delete_item(self, TableName, Key, ConditionExpression = "", ExpressionAttributeValues={}):
        """Delete an Item

        Args:
            TableName (str): Table name
            Key (dict): Primary Key
            ConditionExpression (str, optional): ConditionExpression to prevent the item from being deleted if the condition is not met.
            ExpressionAttributeValues (dict, optional): Expressed attribute values.

        Returns:
            bool: Item deletion is successful or failed
        """
        try:
            table = self.db.Table(TableName)
            if(len(ConditionExpression)>0 and len(ExpressionAttributeValues)>0):
                table.delete_item(
                    Key=Key,
                    ConditionExpression=ConditionExpression,
                    ExpressionAttributeValues=ExpressionAttributeValues
                )
            else:
                table.delete_item(
                    Key=Key
                )
            return True
        except Exception as e:
            logging.warning(e)
            return False
        
    def read_item(self, TableName, Key):
        """Read an Item

        Args:
            TableName (str): Table name
            Key (dict): Primary Key

        Returns:
            dict: Item
        """
        try:
            table = self.db.Table(TableName)
            response = table.get_item(Key=Key)
            return response.get('Item')
        except Exception as e:
            logging.warning(e)
            return []
    
    def update_item(self):
        pass
