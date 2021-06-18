from model.Model import Model
from view.View import View
from controller.Controller import Controller


def main():
    """ Start point of the application.
    Model, View and Controller are instantiated here and the application started.

    :return: void
    """

    # create MVC
    m = Model()
    v = View()
    Controller(m, v)

    # start application
    v.run()


if __name__ == "__main__":
    main()
