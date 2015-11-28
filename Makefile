compile_ui: pyspectrum_main_window.ui import_image.ui rotate_image_dialog.ui calibrate_spectrum.ui miles_dialog.ui
	for ui in $^; do pyuic5 $$ui -o ui_$$( basename $$ui .ui).py ; done

all: compile_ui

clean:
	rm -f ui_*.py
