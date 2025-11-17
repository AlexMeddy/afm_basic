def generate_calc_methods(attribute_name):
    calc_method = f"""def CALC_{attribute_name}(self):
    self.{attribute_name} = {attribute_name}
"""
    calc_tree_method = f"""def CALC_{attribute_name}_TREE(self):
    self.CALC_{attribute_name}()
    for child in self.children:
        child.CALC_{attribute_name}_TREE()
"""
    return calc_method + "\n" + calc_tree_method

def generate_do_something_methods(action_name, attributes):
    attr_list = [attr.strip() for attr in attributes.split(",")] if attributes else []
    do_method_body = "\n    ".join([f"print(self.{attr})" for attr in attr_list]) or "pass"
    do_method = f"""def DO_SOMETHING_{action_name}(self):
    {do_method_body}
"""
    do_tree_method = f"""def DO_SOMETHING_{action_name}_TREE(self):
    self.DO_SOMETHING_{action_name}()
    for child in self.children:
        child.DO_SOMETHING_{action_name}_TREE()
"""
    # Also generate CALC methods for each attribute
    calc_methods = "\n".join([generate_calc_methods(attr) for attr in attr_list])
    return do_method + "\n" + do_tree_method + "\n" + calc_methods

def generate_find_methods(adjective, attribute_name):
    adj_prefix = f"{adjective}_" if adjective else ""
    find_tree_method = f"""def FIND_{adj_prefix}{attribute_name}_TREE(self, {adj_prefix}{attribute_name}_p):
    {adj_prefix}{attribute_name} = {adj_prefix}{attribute_name}_p
    # FIND_{adj_prefix}{attribute_name} logic
    for child in self.children:
        child.FIND_{adj_prefix}{attribute_name}_TREE({adj_prefix}{attribute_name})
"""
    calc_methods = generate_calc_methods(attribute_name)
    return find_tree_method + "\n" + calc_methods

def generate_findby_method(attribute_name):
    return f"""def FINDBY_{attribute_name}(self, {attribute_name}_p):
    {attribute_name} = {attribute_name}_p
    # FINDBY_{attribute_name} logic
    for child in self.children:
        child.FINDBY_{attribute_name}({attribute_name})
"""

def generate_mapping_method(option, source_obj, target_obj):
    if option == "LINEAR_TO_LINEAR":
        return f"""def map_LINEAR_TO_LINEAR_{source_obj}_{target_obj}_LINEAR(self, src_linear_list_p):
    src_linear_list = src_linear_list_p
    for child in src_linear_list:
        # map_LINEAR_TO_LINEAR_LINEAR logic
"""
    elif option == "TREE_TO_LINEAR":
        return f"""def map_TREE_TO_LINEAR_TREE(self, src_root_p):
    src_root = src_root_p
    for child in src_root.children_list:
        src_root = self.map_TREE_TO_LINEAR_TREE(child)
        # map_TREE_TO_LINEAR logic
"""
    elif option == "LINEAR_TREE":
        return f"""def map_LINEAR_TREE_{source_obj}_{target_obj}(self):
    # map_LINEAR_TREE logic
"""
    elif option == "TREE_TREE":
        return f"""def map_TREE_TREE_{source_obj}_{target_obj}(self):
    # map_TREE_TREE logic
"""
    else:
        return "# Invalid mapping option"

def main():
    print("Select method pattern:")
    print("1. CALC\n2. DO_SOMETHING\n3. FIND\n4. FINDBY\n5. MAPPING")
    choice = input("Enter number: ").strip()

    if choice == "1":
        attr = input("Enter attribute name: ").strip()
        print(generate_calc_methods(attr))
    elif choice == "2":
        action = input("Enter ACTION_NAME: ").strip()
        attrs = input("Enter comma-separated attribute names (optional): ").strip()
        print(generate_do_something_methods(action, attrs))
    elif choice == "3":
        adjective = input("Enter adjective (optional, e.g., HIGHEST): ").strip()
        attr = input("Enter attribute name: ").strip()
        print(generate_find_methods(adjective, attr))
    elif choice == "4":
        attr = input("Enter attribute name: ").strip()
        print(generate_findby_method(attr))
    elif choice == "5":
        print("Select mapping option:")
        print("1. LINEAR_TO_LINEAR\n2. LINEAR_TREE\n3. TREE_TO_LINEAR\n4. TREE_TREE")
        opt_map = input("Enter option: ").strip()
        options_dict = {"1": "LINEAR_TO_LINEAR", "2": "LINEAR_TREE", "3": "TREE_TO_LINEAR", "4": "TREE_TREE"}
        option = options_dict.get(opt_map, "")
        source_obj = input("Enter SOURCE_OBJ: ").strip()
        target_obj = input("Enter TARGET_OBJ: ").strip()
        print(generate_mapping_method(option, source_obj, target_obj))
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
