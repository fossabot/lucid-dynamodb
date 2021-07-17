from LucidDynamodb import DynamoDb
import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    db = DynamoDb()
    item_creation_status = db.create_item(
        table_name="dev_jobs", 
        item={
            "company_name": "Google",
            "role_id": "111",
            "role": "Software Engineer 1",
            "salary": "$1,50,531",
            "locations": ["Mountain View, California", "Austin, Texas", "Chicago, IL"],
            "yearly_hike_percent": 8,
            "benefits": set(["Internet, Medical, Edu reimbursements", 
                             "Health insurance",
                             "Travel reimbursements"
                             ]),
            "overall_review":{
                "overall_rating" : "4/5",
                "compensation_and_benefits": "3.9/5"
            }
        }
    )
    try:
        logging.info("Item created successfully")
    except Exception as e:
        logging.warning("Item creation failed - {}".format(e))
        
"""
dineshsonachalam@macbook examples % python 3-create-a-new-item.py
INFO:botocore.credentials:Found credentials in environment variables.
INFO:root:Item created successfully
"""