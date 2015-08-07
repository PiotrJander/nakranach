# coding=utf-8
from behave import *

use_step_matcher("parse")


@given('I am logged in as "{user}"')
def step_impl(context, user):
    """
    :type context behave.runner.Context
    """
    pass


@step('a pub named "Rademenes"')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@step("I am an admin in Rademenes")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then(u'sidebar has "Użytkownicy" field with two subfields: "Lista" and "Zaproś"')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@step("I am not an admin")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then(u'sidebar has no "Użytkownicy" field')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@step("I am employed in Rademenes")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then(u'sidebar has "Lista kranów" field')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@step("I am not employed in any pub")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then(u'sidebar has no "Lista kranów" field')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass