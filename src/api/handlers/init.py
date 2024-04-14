from smskillsdk.models.api import InitRequest


def init_handler(request: InitRequest):
    """
    Init handler
    https://docs.soulmachines.com/skills/api#tag/Init

    Runs when a DDNA Studio project is deployed with this Skill configured.
    """

    print("Init handler got:", request)
    pass
