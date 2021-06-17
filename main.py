from model.Model import Model
from view.View import View
from controller.Controller import Controller


def main():
    # create View
    m = Model()
    v = View()
    c = Controller(m, v)

    # start application
    v.run()


if __name__ == "__main__":
    main()
