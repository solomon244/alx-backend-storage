#!/usr/bin/env python3
""" Python function that lists all documents in a collection: """


def list_all(mongo_collection):
    """
        list of documents or empty list if no document present in collection
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find({}))
