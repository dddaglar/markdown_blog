from enum import Enum

class TextType(Enum):
    NORMAL= "normal"
    BOLD= "bold"
    ITALIC= "italic"
    CODE= "code"
    LINK= "link"
    IMAGE= "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        try:
            self.text_type = TextType(text_type)
        except ValueError:
            raise ValueError(f"Invalid text_type '{text_type}'.")
        self.url = url

    def __eq__(self, other):
        return ( 
            isinstance(other, TextNode) and
            self.text == other.text and 
            self.text_type.value == other.text_type.value and 
            self.url == other.url
        )
    
    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")


