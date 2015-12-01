compile_ui: ui/pyspectrum_main_window.ui ui/import_image.ui ui/rotate_image_dialog.ui ui/calibrate_spectrum.ui ui/line_edit.ui \
	    ui/reference_spectra_dialog.ui ui/select_plotted_point.ui ui/plots_math.ui ui/lines_dialog.ui ui/finish_spectrum.ui 
	for ui in $^; do pyuic5 $$ui -o pyui/$$( basename $$ui .ui).py ; done

all: compile_ui

run: all
	python3 pyspectrum.py
	
unit_tests: all
	python3 -m unittest tests/unit/fits_spectrum_unit.py

tests: unit_tests
  
clean:
	rm -f pyui/*.py
