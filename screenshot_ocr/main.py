import logging


def run():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=logging.DEBUG,
    )

    from screenshot_ocr import cli

    cli.run_program()


if __name__ == "__main__":
    run()
