# Main class

import NAO_config
import NAO_logger
import NAO_controller

controller = None


def start():
    ###
    # Summary: it starts the logger, the config and the controller
    # Parameters: none
    # Return: --
    ###

    logger = NAO_logger.Logger()
    config = NAO_config.Config(logger)

    global controller
    controller = NAO_controller.Controller(logger, config)
    controller.start()


def stop():
    ###
    # Summary: it stops everything
    # Parameters: none
    # Return: --
    ###

    controller.isStop = True


if __name__ == "__main__":
    logger = NAO_logger.Logger()
    config = NAO_config.Config(logger)

    controller = NAO_controller.Controller(logger, config)
    controller.start()