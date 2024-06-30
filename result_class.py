import streamlit as st
import torch
from utils import model

name = model.names

def resultClassList(results):
    result_class = []
    for result in results:
        class_ids = result.boxes.cls
        for id in class_ids:
            if id not in result_class:
                result_class.append(int(id))
    return list(result_class)

def getClassName(id):
    return name.get(id)

        
