#!/usr/bin/env python3
"""The main console for the app
"""
import cmd
import model
import shlex  # function that split a line along spaces except that in double quotes
import sqlalchemy
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.property import Property_Type
from models.review import Review
from models.state import State
from models.user import User

model_classes = {
        "Amenity": Amenity,
        "City": City,
        "Property_Type": Property_Type,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
}

class ECSTASYCommand(cmd.Cmd):
    """The main app command"""
    prompt = '(ecstasy)'

    def do_EOF(self, arg):
        """Exit the console"""
        return True

    def emptyline(self):
        """overwriting the emptyline method"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self. args):
        """Function that creates a dictionary from a list of strings"""
        new_dict = {}
        for ag in args:
            if "=" in ag:
                kvp = ag.split('=', 1)
                key = kvp[0]
                val = kvp[1]
                if val[0] == val[-1] == '"':
                    val = shlex.split(val)[0].replace('_', ' ')
                else:
                    try:
                        val = int(val)
                    except Exception:
                        try:
                            val = float(val)
                        except Exception:
                            continue
                new_dict[key] = val
        return new_dict

    def do_create(self, arg):
        """Function that creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = model_classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Function that prints an instance of a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in model_classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Function that deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in model_classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id not found **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Function that prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in model_classes:
            obj_dict = models.storage.all(model_classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Function that updates an instance based on the class name, id,
        attribute and value
        """
        args = shlex.split(arg)
        integers = ["number__of_rooms", "number_of_bathrooms", "number_of_toilets",
                    "max_occupants", "price"]
        floats = ["latitude", "longitude"]
        boolean = ["water_treatment", "sewage_treatment", "access_control"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in model_classes:
            if len(args) > 1:
                key = arg[0] + "." + args[1]
                if key in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except Exception:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[key], args[2], args[3])
                            models.storage.all()[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    ECSTACYCommand().cmdloop()
