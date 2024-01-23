#!/usr/bin/env python3
""" List all documents in Python """


def list_all(mongo_collection) -> list:
    """ list all """
    return mongo_collection.find()
