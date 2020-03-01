class SlackBlockBuilder:
    def __init__(self):
        self.__block = []

    def add_section(self, title, accessory=None):
        section = dict(
            type="section",
            text=dict(type="mrkdwn", text=title)
        )
        if accessory is not None:
            section.update(accesory=accessory)
        self.__block.append(section)
        return self

    def add_image(self, text, url, alt_text):
        image = dict(
            type="image",
            title=dict(type="plain_text", text=text, emoji=True),
            image_url=url,
            alt_text=alt_text
        )
        self.__block.append(image)
        return self

    def add_context(self, text):
        elements = SlackElementsBuilder().add_text(text).build()
        self.__block.append(dict(
            type="context",
            elements=elements
        ))
        return self

    def add_divider(self):
        self.__block.append(dict(type="divider"))
        return self

    def add_actions(self, elements):
        self.__block.append(
            dict(
                type="actions",
                elements=elements
            )
        )
        return self

    def build(self):
        return self.__block


class SlackElementsBuilder:
    def __init__(self):
        self.__elements = []

    def add_text(self, text):
        self.__elements.append(
            dict(
                type="mrkdwn",
                text=text
            )
        )
        return self

    def add_conversation_select(self, text):
        self.__elements.append(
            dict(
                type="conversations_select",
                placeholder=dict(type="plain_text", text=text, emoji=True)
            )
        )
        return self

    def add_channel_select(self, text):
        self.__elements.append(
            dict(
                type="channels_select",
                placeholder=dict(type="plain_text", text=text, emoji=True)
            )
        )
        return self

    def add_user_select(self, text):
        self.__elements.append(
            dict(
                type="users_select",
                placeholder=dict(type="plain_text", text=text, emoji=True)
            )
        )
        return self

    def add_static_select(self, text, items):
        options = []
        for item in items:
            options.append(
                {
                    dict(
                        text=dict(type="plain_text", text=item.name, emoji=True),
                        value=item.value
                    )
                }
            )
        self.__elements.append(
            dict(
                type="static_select",
                placeholder=dict(type="plain_text", text=text, emoji=True),
                options=options
            )
        )
        return self

    def add_date_picker(self, text, initial_date):
        self.__elements.append(
            dict(
                type="datepicker",
                initial_date=initial_date,
                placeholder=dict(type="plain_text", text=text, emoji=True)
            )
        )
        return self

    def build(self):
        return self.__elements


class SlackAttachmentBuilder:
    def __init__(self):
        self.__attachments = []

    def add_item(self, blocks, color="#00ff00"):
        self.__attachments.append(dict(
            color=color,
            blocks=blocks
        ))
        return self

    def build(self):
        return self.__attachments
