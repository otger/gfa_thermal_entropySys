#!/usr/bin/python
# -*- coding: utf-8 -*-
from .states import *

__author__ = 'otger'


class StateMachine(object):
    def __init__(self, functionality, settings, boundary_conditions):
        self.func = functionality
        self.settings = settings
        self.bc = boundary_conditions
        self.current_state = IdleState(sm=self)
        self.current_state.initial_run()

    def update(self):
        self.current_state.update()

    def new_state(self, state):
        """
        Method used by states when after an update conditions, state has to change
        :param state:
        :return:
        """
        self.current_state = state
        self.current_state.initial_run()

    def start_cooling(self):
        self.current_state.change_request(StateRequests.CoolDown)

    def stop_cooling(self):
        self.current_state.change_request(StateRequests.Idle)
