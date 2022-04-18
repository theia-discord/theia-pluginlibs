class EmojiList(dict):
    def __call__(self, name: str) -> str:
        if name not in self:
            return self["__unknown__"]
        return self[name]

emoji = EmojiList([
    ("__unknown__", "\U0001f533"),
    ("error", "\U0000274c"),
    ("warning", "\U000026a0\U0000fe0f"),
    ("success", "\U00002714\U0000fe0f"),
    ("question", "\U00002753"),
    ("wtf", "\U00002049\U0000fe0f"),
    ("robot", "\U0001f916"),
])
