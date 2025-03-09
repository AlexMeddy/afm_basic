from CContinent import CContinent
from CCountry import CCountry
from CState import CState
from CCity import CCity
continent_obj = CContinent("Australasia")
continent_obj.country_list.append(CCountry("Australia"))
continent_obj.country_list[0].state_list.append(CState("NSW"))
continent_obj.country_list[0].state_list.append(CState("QLD"))
continent_obj.country_list[0].state_list[0].city_list.append(CCity("Bondi", 600000))
continent_obj.country_list[0].state_list[0].city_list.append(CCity("Ryde", 50000))
continent_obj.country_list[0].state_list[0].city_list.append(CCity("Sydney", 900000))
state_obj = continent_obj.country_list[0].state_list[0]

city_name = "Sydney"
rc = state_obj.find_city_by_name(city_name)
if rc == 1:
    print("calling: {} found: {}".format(state_obj.name, city_name))
else:
    print("calling: {} not found: {}".format(state_obj.name, city_name))
        
city_name = "bla"
rc = state_obj.find_city_by_name(city_name)
if rc == 1:
    print("calling: {} found: {}".format(state_obj.name, city_name))
else:
    print("calling: {} not found: {}".format(state_obj.name, city_name))
    
city_name = "Bondi"
city_ptr_l = state_obj.find_city_by_namev2(city_name)
if city_ptr_l != None:
    print("calling: {} found: {}".format(state_obj.name, city_name))
    print("city: {} before population change: {}".format(city_ptr_l.name, city_ptr_l.population))
    city_ptr_l.population = 740000
    print("city: {} after population change: {}".format(city_ptr_l.name, city_ptr_l.population))
else:
    print("calling: {} not found: {}".format(state_obj.name, city_name))
    
def output_print_tree(continent_obj_p):
    print("name of continent: {}".format(continent_obj_p.name))
    for cn_country in continent_obj_p.country_list:
        print("name of country: {}".format(cn_country.name))
        for cn_state in continent_obj_p.country_list[0].state_list:
            print("name of state: {}".format(cn_state.name))
            for cn_city in continent_obj_p.country_list[0].state_list[0].city_list:
                print("name of city: {}".format(cn_city.name))
                
output_print_tree(continent_obj)