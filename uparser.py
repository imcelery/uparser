class Tag:
    def __init__(self, tag=None, attributes={}, content=[]):
        self.tag = tag
        self.content = content
        self.attributes = attributes

    def __str__(self):
        return f"{self.tag} " + " ".join(self.content)

    __repr__ = __str__

class Uparses:
    def __init__(self, html=None):
        self.html = html
        self.root = []
        self.tags = {}
        self.ids = {}
        self.classes = {}
        if self.html:
            self.parse()

    def parse_tag(self, s):
        tg = ""
        attributes = {}
        w = ""
        lw = ""
        found_tg = False
        in_string = False

        for i in s:
            if i == " " and not in_string:
                if not found_tg:
                    found_tg = True
                    tg = w
                    w = ""
                elif lw is not None:
                    attributes[lw] = w
                    lw = ""
                    w = ""
            elif i == '=' and not in_string:
                lw = w
                w = ""
            elif i == '"':
                in_string = not in_string
            else:
                w += i

        without_content = False
        if not found_tg:
            tg = w
        elif w != "":
            if "/" == w.strip():
                without_content = True
            else:
                attributes[lw] = w

        without_content = without_content or tg in ["meta", "link", "!DOCTYPE", "noscript", "img"]
        is_closed = '/' in tg
        return tg, attributes, is_closed, without_content

    def parse(self, html=None):

        if html:
            self.html = html

        if self.html:
            stack = [[]]
            l = 0
            r = len(self.html)

            while l < r:
                a = self.html.find("<", l)
                if a == -1:
                    break
                b = self.html.find(">", l)
                s = self.html[a+1:b]

                ss = self.html[l:a].strip()
                if ss:
                    stack[-1].append(ss)

                tg, attributes, is_closed, without_content = self.parse_tag(s)

                if without_content:
                    o = Tag(tg, attributes)

                    if tg in self.tags.keys():
                        self.tags[tg].append(o)
                    else:
                        self.tags[tg] = [o]

                    if "id" in attributes.keys():
                        self.ids[attributes["id"]] = o

                    if "class" in attributes.keys():
                        if attributes["class"] in self.classes.keys():
                            self.classes[attributes["class"]].append(o)
                        else:
                            self.classes[attributes["class"]] = [o]

                    stack[-1].append(o)

                elif is_closed:
                    if len(stack) > 1:
                        a = stack.pop()
                        stack[-1][-1].content = a
                else:
                    o = Tag(tg, attributes)

                    if tg in self.tags.keys():
                        self.tags[tg].append(o)
                    else:
                        self.tags[tg] = [o]

                    if "id" in attributes.keys():
                        self.ids[attributes["id"]] = o

                    if "class" in attributes.keys():
                        if attributes["class"] in self.classes.keys():
                            self.classes[attributes["class"]].append(o)
                        else:
                            self.classes[attributes["class"]] = [o]

                    stack[-1].append(o)
                    stack.append([])

                l = b + 1

        self.root = stack[0]

    def get_by_tag(self, tag):
        if tag in self.tags.keys():
            return self.tags[tag]
        else:
            return None

    def get_by_class(self, cl):
        if cl in self.classes.keys():
            return self.classes[cl]
        else:
            return None

    def get_by_id(self, id):
        if id in self.ids.keys():
            return self.ids[id]
        else:
            return None

