from textnode import TextType, TextNode

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        if isinstance(children,list) or children is None:
            self.children = children
        else:
            raise ValueError("Children should be a list")
        if isinstance(props,dict) or props is None:
            self.props = props
        else:
            raise ValueError("Props should be a dict")

    def to_html(self):
        raise NotImplementedError("not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        res = ""
        for k,v in self.props.items():
            res += f' {k}="{v}"'
        return res[1:]
    
    def __repr__(self):
        return f"tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag,value,props=None):
        if value == None:
            raise ValueError("value cannot be None")
        children = None
        super().__init__(tag, value,children,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None:
            return self.value
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"  
        else:
            if self.tag == "img":
                res = f"<{self.tag}"
                for k,v in self.props.items():
                    res += f' {k}="{v}"'
                res += f">"
                return res
            else:
                res = f"<{self.tag}"
                for k,v in self.props.items():
                    res += f' {k}="{v}"'
                res += f">{self.value}</{self.tag}>"
                return res
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
            super().__init__(tag, value=None, children=children,props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag of a ParentNode must have a value")
        elif self.children == None or self.children == []:
            raise ValueError("Children of a ParentNode must have a value")
        else:
            res = f"<{self.tag}>"
            for child in self.children:
                adder = child.to_html()
                res += adder
            res += f"</{self.tag}>"
            return res
        

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Text type is not valid")
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text,props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="",props={"src":text_node.url, "alt":text_node.text})