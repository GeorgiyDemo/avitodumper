import yaml
dictionary = {
    "numbers_count": 30,
    "second_url" : "/moskva/lichnye_veschi?s_trg=10&user=1&p=",
    "phone_number_length" : 11,
    "city_in_url" : "moskva",
}

print(yaml.dump(dictionary))