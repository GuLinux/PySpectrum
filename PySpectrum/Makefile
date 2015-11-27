compile_ui: pyspectrum_main_window.ui import_image.ui
	for ui in $^; do pyuic5 $$ui -o ui_$$( basename $$ui .ui).py ; done

all: compile_ui

clean:
	rm -f ui_*.py
