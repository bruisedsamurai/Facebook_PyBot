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


class BadParameterError(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        
        :type description: object
        
        """
        self.description = description


class AccessTokenErrors(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        
        :type description: object
        
        """
        self.description = description


class PermissionError(Error):
    def __init__(self, description):
        """
        @required
        Code
        Description
        
        :type description: object
        
        """
        self.description = description


class AccountLinkingErrors(Error):
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


def raise_error(response_data):
    if response_data["error"]["code"] == 1200:
        return InternalError("Temporary send message failure. Please try again later.")
    elif response_data["error"]["code"] == 4:
        return LimitError("Too many send requests to phone numbers")
    elif response_data["error"]["code"] == 100:
        if response_data["error"].get("error_subcode") == 2018109:
            return LimitError("Attachment size exceeds allowable limit")
        elif response_data["error"].get("error_subcode") == 2018001:
            return BadParameterError("No matching user found")
        else:
            data = response_data["error"]["message"]
            return BadParameterError(data)
    elif response_data["error"]["code"] == 613:
        return LimitError("Calls to this API have exceeded the rate limit")
    elif response_data["error"]["code"] == 190:
        return AccessTokenErrors("Invalid OAuth access token.")
    elif response_data["error"]["code"] == 10:
        if response_data["error"].get("error_subcode") == 2018065:
            return PermissionError(
                "This message is sent outside of allowed window. "
                "You need page_messaging_subscriptions permission to be able to do it.")
        elif response_data["error"].get("error_subcode") == 2018108:
            return PermissionError(
                "This Person Cannot Receive Messages: This person isn't receiving messages from you right now.")
    elif response_data["error"]["code"] == 200:
        if response_data["error"].get("error_subcode") == 2018028:
            return PermissionError(
                "Cannot message users who are not admins, "
                "developers or testers of the app until pages_messaging permission is reviewed and the app is live.")
        elif response_data["error"]["error_subcode"] == 2018027:
            return PermissionError(
                "Cannot message users who are not admins, "
                "developers or testers of the app "
                "until pages_messaging_phone_number permission is reviewed and the app is live.")
        elif response_data["error"]["error_subcode"] == 2018021:
            return PermissionError(
                "Requires phone matching access fee to be paid by this page"
                " unless the recipient user is an admin, developer, or tester of the app.")
        elif response_data["error"]["error_subcode"] == 1545041:
            return PermissionError("Message Not Sent: This person isn't available right now.")
    elif response_data["error"]["code"] == 10303:
        return AccountLinkingErrors("Invalid account_linking_token")
    elif response_data["error"]["code"] == 194:
        message = response_data["error"]["message"]
        return OAuthException(message)
    elif response_data["error"]["code"] == 803:
        message = response_data["error"]["message"]
        return OAuthException(message)
    else:
        return Exception(response_data["error"]["message"])


class ElementCountExceeded(Error):

    def __init__(self, description):
        self.description = description


class QuickReplyCountExceeded(Error):

    def __init__(self, description):
        self.description = description


class CharacterCountExceeded(Error):

    def __init__(self, description):
        self.description = description
