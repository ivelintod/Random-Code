class Person:

    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last


def upper_case_name(obj):
    return('%s %s' % (obj.first_name, obj.last_name)).upper()

upper_case_name.short_description = 'Customer names'

p = Person('Ivelin', 'Todorov')
print(upper_case_name(p))
print(upper_case_name.short_description)
