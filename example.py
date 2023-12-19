from uparser import Uparses



if __name__ == "__main__":
    with open("site.txt", "UTF-8") as f:
        s = "".join(f.readlines())
        parser = Uparses()
        parser.parse(s)
        print(parser.get_by_class("a"))