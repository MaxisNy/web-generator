from textnode import TextNode

def main():
    tn1 = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(tn1)
    tn2 = TextNode("This is a text node", "normal", "https://www.boot.dev")
    print(tn1 == tn2)

main()
