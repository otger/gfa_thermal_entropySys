#!/usr/bin/python
# -*- coding: utf-8 -*-
import abc
__author__ = 'otger'


class StateRequests(object):
    Idle = 0
    CoolDown = 1
    PeltierOff = 2


class BaseState(metaclass=abc.ABCMeta):

    def __init__(self, sm):
        self.sm = sm

    @abc.abstractmethod
    def initial_run(self):
        pass

    @abc.abstractmethod
    def update(self, conditions):
        """
        Update contorn conditions for state
        :param sm: State Machine, so it can change state if required by boundary conditions
        :param conditions: dictionary with boundary conditions values (sensors, status,...)
        :return: None
        """
        pass

    @abc.abstractmethod
    def change_request(self, request):
        """
        State receives a petition to change state externally
        :param request:
        :return:
        """
        pass


class IdleState(BaseState):
    name = 'idle'

    def initial_run(self):
        pass

    def update(self, conditions):
        # Idle is a static state, does not change based on boundary conditions, it only changes by request
        pass

    def change_request(self, request):
        if request == StateRequests.CoolDown:
            self.sm.next_state(CoolDownState(self.sm))


class CoolDownState(BaseState):
    name = 'cool_down'

    def initial_run(self):
        # Switch on power supply output
        self.sm.func.enable_power_supply()

    def update(self):
        if self.sm.bc['temperature'] < self.sm.settings['cold_threshold']:
            self.sm.next_state(WarmUpState())
        else:
            self.sm.func.power_supply_update_vi()

    def change_request(self, request):
        if request == StateRequests.Idle:
            self.sm.func.disable_power_supply()
            self.sm.next_state(IdleState(self.sm))


class WarmUpState(BaseState):
    name = 'warm_up'

    def initial_run(self):
        # Switch off power supply output
        self.sm.func.disable_power_supply()

    def update(self, conditions):
        if self.sm.bc['temperature'] > self.sm.settings['hot_threshold']:
            self.sm.next_state(CoolDownState(self.sm))

    def change_request(self, request):
        if request == StateRequests.Idle:
            self.sm.func.disable_power_supply()
            self.sm.next_state(IdleState(self.sm))

