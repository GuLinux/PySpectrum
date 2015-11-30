compile_ui: pyspectrum_main_window.ui import_image.ui rotate_image_dialog.ui calibrate_spectrum.ui miles_dialog.ui select_plotted_point.ui plots_math.ui
	for ui in $^; do pyuic5 $$ui -o ui_$$( basename $$ui .ui).py ; done

all: compile_ui

run: all
	python3 pyspectrum.py
	
unit_tests: all
	python3 -m unittest tests/unit/fits_spectrum_unit.py


tests: unit_tests
  
clean:
	rm -f ui_*.py
