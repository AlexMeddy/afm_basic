import textwrap

def gen_calc(attribute):
    return textwrap.dedent(f"""
    def CALC_{attribute}(self):
        self.{attribute} = {attribute}

    def CALC_{attribute}_TREE(self):
        self.CALC_{attribute}()
        for child in self.children_list:
            child.CALC_{attribute}_TREE()
    """).strip("\n")


def gen_do_something(action, attributes):
    printed = "\n        ".join([f"print('{attr} =', self.{attr})" for attr in attributes]) if attributes else "pass"
    return textwrap.dedent(f"""
    def DO_SOMETHING_{action}(self):
        {printed}

    def DO_SOMETHING_{action}_TREE(self):
        self.DO_SOMETHING_{action}()
        for child in self.children:
            child.DO_SOMETHING_{action}_TREE()
    """).strip("\n")


def gen_find(adjective, attribute):
    adj_prefix = f"{adjective}_" if adjective else ""
    param = f"{adj_prefix}{attribute}_p"

    return textwrap.dedent(f"""
    def FIND_{adj_prefix}{attribute}_TREE(self, {param}):
        {adj_prefix}{attribute} = {param}
        #FIND_{adj_prefix}{attribute} logic 
        for child in self.children:
            child.FIND_{adj_prefix}{attribute}_TREE({adj_prefix}{attribute})
    """).strip("\n")


def gen_findby(attribute):
    return textwrap.dedent(f"""
    def FINDBY_{attribute}(self, {attribute}_p):
        {attribute} = {attribute}_p
        #FINDBY_{attribute} logic 
        for child in self.children:
            child.FINDBY_{attribute}({attribute})
    """).strip("\n")


def gen_mapping(option, src, tgt):
    if option == "1":  # LINEAR_TO_LINEAR
        return textwrap.dedent(f"""
        def map_LINEAR_TO_LINEAR_{src}_{tgt}_LINEAR(self, src_linear_list_p):
            src_linear_list = src_linear_list_p
            for child in src_linear_list:
                #map_LINEAR_TO_LINEAR_{src}_{tgt}_LINEAR logic 
        """).strip("\n")

    elif option == "2":  # LINEAR_TREE
        return textwrap.dedent(f"""
        def map_LINEAR_TREE_{src}_{tgt}_TREE(self, src_linear_list_p):
            src_linear_list = src_linear_list_p
            for child in src_linear_list:
                #map_LINEAR_TREE_{src}_{tgt}_TREE logic 
        """).strip("\n")

    elif option == "3":  # TREE_TO_LINEAR
        return textwrap.dedent(f"""
        def map_TREE_TO_LINEAR_TREE(self, src_root_p):
            src_root = src_root_p
            for child in src_root.children_list:
                src_root = self.map_TREE_TO_LINEAR_TREE(child)
                #map_TREE_TO_LINEAR logic 
        """).strip("\n")

    elif option == "4":  # TREE_TREE
        return textwrap.dedent(f"""
        def map_TREE_TREE_{src}_{tgt}_TREE(self, src_root_p):
            src_root = src_root_p
            for child in src_root.children_list:
                src_root = self.map_TREE_TO_LINEAR_TREE(child)
                #map_TREE_TREE_{src}_{tgt}_TREE logic 
        """).strip("\n")

    else:
        return "# Invalid mapping option"


def main():
    print("Select method pattern:")
    print("1 = CALC")
    print("2 = DO_SOMETHING")
    print("3 = FIND")
    print("4 = FINDBY")
    print("5 = MAPPING")

    pattern = input("Enter choice: ").strip()

    output = ""

    if pattern == "1":  # CALC
        attr = input("Enter attribute name: ").strip()
        output += gen_calc(attr)

    elif pattern == "2":  # DO_SOMETHING
        action = input("Enter ACTION_NAME: ").strip()
        attrs = input("Enter comma-separated attribute names (optional): ").strip()
        attr_list = [a.strip() for a in attrs.split(",") if a.strip()] if attrs else []

        output += gen_do_something(action, attr_list)

        # Generate CALC methods for each attribute
        for a in attr_list:
            output += "\n\n" + gen_calc(a)

    elif pattern == "3":  # FIND
        adj = input("Enter adjective (optional, e.g. HIGHEST): ").strip()
        adj = adj.upper() if adj else ""
        attr = input("Enter attribute name: ").strip()

        output += gen_find(adj, attr)

        # CALC method for this attribute
        output += "\n\n" + gen_calc(attr)

    elif pattern == "4":  # FINDBY
        attr = input("Enter attribute name: ").strip()
        output += gen_findby(attr)

    elif pattern == "5":  # MAPPING
        print("Select mapping type:")
        print("1 = LINEAR_TO_LINEAR")
        print("2 = LINEAR_TREE")
        print("3 = TREE_TO_LINEAR")
        print("4 = TREE_TREE")
        option = input("Enter mapping option number: ").strip()

        src = input("Enter SOURCE_OBJ: ").strip()
        tgt = input("Enter TARGET_OBJ: ").strip()

        output += gen_mapping(option, src, tgt)

    else:
        print("Invalid selection.")
        return

    print("\n======= GENERATED METHODS =======\n")
    print(output)
    print("\n=================================\n")


if __name__ == "__main__":
    main()
