from classes_for_bot import PhoneLengthError, PhoneTypeError, BirthdayTypeError

# Exception handling decorator


def error_exception(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Try again. Enter correct name and phone number"
        except KeyError:
            return "Try again. Enter correct name"
        except TypeError:
            return "Not enough parameters to execute the command. Please try again"
        except ValueError:
            return "Incorrect name entered. Please try again"
        except PhoneTypeError:
            return "Incorrect number entered. Please try again"
        except PhoneLengthError:
            return "Phone length must have 10 or 12 digits"
        except BirthdayTypeError:
            return "Wrong type of birthday entered"
    return wrapper
