compile_ui: pyspectrum_main_window.ui 
	for ui in $^; do pyuic5 $$ui -o ui_$$( basename $$ui .ui).py ; done
  
all: compile_ui

