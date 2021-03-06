.PHONY: all
all: compile_ui compile_rcc

pyui/pyspectrum_main_window.py: ui/pyspectrum_main_window.ui
	pyuic5 $^ -o $@
pyui/import_image.py: ui/import_image.ui
	pyuic5 $^ -o $@
pyui/rotate_image_dialog.py: ui/rotate_image_dialog.ui
	pyuic5 $^ -o $@
pyui/calibrate_spectrum.py: ui/calibrate_spectrum.ui
	pyuic5 $^ -o $@
pyui/line_edit.py: ui/line_edit.ui
	pyuic5 $^ -o $@
pyui/reference_spectra_dialog.py: ui/reference_spectra_dialog.ui
	pyuic5 $^ -o $@
pyui/select_plotted_point.py: ui/select_plotted_point.ui
	pyuic5 $^ -o $@
pyui/plots_math.py: ui/plots_math.ui
	pyuic5 $^ -o $@
pyui/lines_dialog.py: ui/lines_dialog.ui
	pyuic5 $^ -o $@
pyui/finish_spectrum.py: ui/finish_spectrum.ui
	pyuic5 $^ -o $@
pyui/object_properties_dialog.py: ui/object_properties_dialog.ui
	pyuic5 $^ -o $@
pyui/homepage.py: ui/homepage.ui
	pyuic5 $^ -o $@
pyui/project_dialog.py: ui/project_dialog.ui
	pyuic5 $^ -o $@
pyui/stack_images.py: ui/stack_images.ui
	pyuic5 $^ -o $@
pyui/spectrum_trim_dialog.py: ui/spectrum_trim_dialog.ui
	pyuic5 $^ -o $@
pyui/project_widget.py: ui/project_widget.ui
	pyuic5 $^ -o $@
pyui/notification.py: ui/notification.ui
	pyuic5 $^ -o $@

resources_rc.py: resources/*
	pyrcc5 resources/resources.qrc > resources_rc.py

.PHONY: compile_rcc
compile_rcc: resources_rc.py

.PHONY: compile_ui
compile_ui: pyui/pyspectrum_main_window.py pyui/import_image.py pyui/rotate_image_dialog.py pyui/calibrate_spectrum.py pyui/line_edit.py pyui/homepage.py pyui/project_dialog.py \
	    pyui/reference_spectra_dialog.py pyui/select_plotted_point.py pyui/plots_math.py pyui/lines_dialog.py pyui/finish_spectrum.py pyui/object_properties_dialog.py \
	    pyui/stack_images.py pyui/spectrum_trim_dialog.py pyui/project_widget.py pyui/notification.py

.PHONY: run
run: all
	python3 pyspectrum.py
	
	
.PHONY: unit_tests
unit_tests: all
	python -m unittest discover -s tests/unit/ -p "*.py"

.PHONY: tests
tests: unit_tests
  
.PHONY: clean
clean:
	rm -f pyui/*.py
