import streamlit as st
from controller.Controlador import Controlador

class MainView:
    # Constructor.
    def __init__(self, controlador):
        super().__init__()
        self.controller = controlador