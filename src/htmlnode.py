class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_str = ""
        if self.props != None:
            for prop in self.props:
                props_str += " " + prop + "=" + f'"{self.props.get(prop)}"'
        return props_str

    def __repr__(self) -> str:
        output = f"HTMLNode TAG: {self.tag}\n"
        output += f"HTMLNode VALUE: {self.value}\n"
        output += f"HTMLNode CHILDREN: {self.children}".replace('\n', ', ') + "\n"
        output += f"HTMLNode PROPS: {self.props}"
        return output