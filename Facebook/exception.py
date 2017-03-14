class Error(Exception):
    pass


class ValidationError(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class InternalError(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class LimitError(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class Bad_Parameter_Error(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class Access_Token_Errors(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class Permission_Error(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class Account_Linking_Errors(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        :type description: object
        """
        self.description = description


class OAuthException(Error):
    def __init__(self, description):
        """

        :param description:
        """
        self.description = description


def raiseError(response_data):
    if response_data["error"]["code"] == 1200:
        return InternalError("Temporary send message failure. Please try again later.")
    elif response_data["error"]["code"] == 4:
        return LimitError("Too many send requests to phone numbers")
    elif response_data["error"]["code"] == 100:
        if response_data["error"]["error_subcode"] == 2018109:
            return LimitError("Attachment size exceeds allowable limit")
        elif response_data["error"]["error_subcode"] == 2018001:
            return Bad_Parameter_Error("No matching user found")
        else:
            return Bad_Parameter_Error("Invalid fbid.")
    elif response_data["error"]["code"] == 613:
        return LimitError("Calls to this API have exceeded the rate limit")
    elif response_data["error"]["code"] == 190:
        return Access_Token_Errors("Invalid OAuth access token.")
    elif response_data["error"]["code"] == 10:
        if response_data["error"]["error_subcode"] == 2018065:
            return Permission_Error(
                "This message is sent outside of allowed window. You need page_messaging_subscriptions permission to be able to do it.")
        elif response_data["error"]["error_subcode"] == 2018108:
            return Permission_Error(
                "This Person Cannot Receive Messages: This person isn't receiving messages from you right now.")
    elif response_data["error"]["code"] == 200:
        if response_data["error"]["error_subcode"] == 2018028:
            return Permission_Error(
                "Cannot message users who are not admins, developers or testers of the app until pages_messaging permission is reviewed and the app is live.")
        elif response_data["error"]["error_subcode"] == 2018027:
            return Permission_Error(
                "Cannot message users who are not admins, developers or testers of the app until pages_messaging_phone_number permission is reviewed and the app is live.")
        elif response_data["error"]["error_subcode"] == 2018021:
            return Permission_Error(
                "Requires phone matching access fee to be paid by this page unless the recipient user is an admin, developer, or tester of the app.")
        elif response_data["error"]["error_subcode"] == 1545041:
            return Permission_Error("Message Not Sent: This person isn't available right now.")
    elif response_data["error"]["code"] == 10303:
        return Account_Linking_Errors("Invalid account_linking_token")
    elif response_data["error"]["code"] == 194:
        message = response_data["error"]["message"]
        return OAuthException(message)
