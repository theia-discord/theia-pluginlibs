import sys
import json

class TheiaReply(dict):
    REPLY_TYPE = "UnknownReply"

    def emit(self):
        sys.stdout.write(json.dumps({self.__class__.REPLY_TYPE: self}))
        sys.stdout.flush()

class SendMessage(TheiaReply):
    REPLY_TYPE = "SendMessage"

    def in_reply_to(self, message):
        self["channel_id"] = message["channel_id"]
        self["in_reply_to"] = message["message_id"]
        return self
