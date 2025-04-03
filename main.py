#%%

# import checkpoint message
from helper_functions.checkpoint import checkpoint

# get interface design
from ui.interface_design import interface_init


def main():
    interface_init()


if __name__ == "__main__":
    main()

checkpoint(__file__)

