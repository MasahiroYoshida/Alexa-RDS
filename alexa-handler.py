# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard, AskForPermissionsConsentCard
from ask_sdk_model import Response
from ask_sdk_model.services import ServiceException

from app import getFlight, getFlightToSpecific, getFlightToSpecificOnDate, getRecentTicket
from helper import convert
sb = CustomSkillBuilder(api_client=DefaultApiClient)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

permissions = ["read::alexa:device:all:address"]
NOTIFY_MISSING_PERMISSIONS = ("Please enable Location permissions in "
                              "the Amazon Alexa app.")
NO_ADDRESS = ("It looks like you don't have an address set. "
              "You can set your address from the companion app.")
ADDRESS_AVAILABLE = "Here is your full address: {}, {}, {}"
ERROR = "Uh Oh. Looks like something went wrong."
LOCATION_FAILURE = ("There was an error with the Device Address API. "
                    "Please try again.")

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to Flight SN. you can say find flight"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class GetFlightIntentHandler(AbstractRequestHandler):
    """Handler for Get Flight Intent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetFlightIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info(handler_input.request_envelope.request)
        converted_input = convert(handler_input.request_envelope.request)
        logger.info(converted_input)

        speech_text = getFlight()

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class GetFlightToSpecificIntentHandler(AbstractRequestHandler):
    """Handler for Get Flight Intent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetFlightToSpecificIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info(handler_input.request_envelope.request)
        slots   = convert(handler_input.request_envelope.request.intent.slots)
        logger.info(slots)
        destination = slots['destination'].value
        start       = slots['start'].value
        logger.info("start: {}, destination: {}".format(start, destination))
        if start is None:
            speech_text = getFlightToSpecific(destination)
        else:
            speech_text = getFlightToSpecific(destination, start)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class GetFlightToSpecificOnDateIntentHandler(AbstractRequestHandler):
    """Handler for Get Flight Intent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetFlightToSpecificOnDateIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info(handler_input.request_envelope.request)
        slots = convert(handler_input.request_envelope.request.intent.slots)
        logger.info(slots)
        destination = slots['destination'].value
        start       = slots['start'].value
        departure   = slots['departure'].value
        logger.info("start: {}, destination: {}, departure: {}".format(start, destination, departure))
        if start is None:
            speech_text = getFlightToSpecificOnDate(departure, destination)
        else:
            speech_text = getFlightToSpecificOnDate(departure, destination, start)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class GetRecentTicketIntentHandler(AbstractRequestHandler):
    """Handler for Get Flight Intent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetRecentTicketIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        customer_id = 1012093031 #this should be email and query with email
        
        speech_text = getRecentTicket(customer_id)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response
        
class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello Python World from Classes!"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class GetAddressIntentHandler(AbstractRequestHandler):
    # Handler for Getting Device Address or asking for location consent
    def can_handle(self, handler_input):
        return is_intent_name("GetAddressIntent")(handler_input)

    def handle(self, handler_input):
        req_envelope = handler_input.request_envelope
        response_builder = handler_input.response_builder
        service_client_fact = handler_input.service_client_factory

        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.user.permissions.consent_token):
            response_builder.speak(NOTIFY_MISSING_PERMISSIONS)
            response_builder.set_card(
                AskForPermissionsConsentCard(permissions=permissions))
            return response_builder.response

        try:
            device_id = req_envelope.context.system.device.device_id
            device_addr_client = service_client_fact.get_device_address_service()
            addr = device_addr_client.get_full_address(device_id)

            if addr.address_line1 is None and addr.state_or_region is None:
                response_builder.speak(NO_ADDRESS)
            else:
                response_builder.speak(ADDRESS_AVAILABLE.format(
                    addr.address_line1, addr.state_or_region, addr.postal_code))
            return response_builder.response
        except ServiceException:
            response_builder.speak(ERROR)
            return response_builder.response
        except Exception as e:
            raise e


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetFlightIntentHandler())
sb.add_request_handler(GetFlightToSpecificIntentHandler())
sb.add_request_handler(GetFlightToSpecificOnDateIntentHandler())
sb.add_request_handler(GetRecentTicketIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()