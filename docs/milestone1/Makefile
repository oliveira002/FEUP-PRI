# define the name of the virtual environment directory
VENV := venv

# Define the name of the output directory for unzipped files
DATASET_DIR := data

OUTPUT_FILE = data/steam_data.csv
OUTPUT_FILE2 = data/text_content.csv
FILE_ID = 1PxbOqSO-qyCw-iw-7C1TYnqkyWwSKgyB
FILE_ID2 = 1J1ZTFsR0BHH5sTatHDYmI9YLIQZsKDj2


# default target, when make executed without arguments
all: download install venv run clean

download:
	@echo "Downloading the file..."
	@mkdir $(DATASET_DIR)
	@python3 -m pip install gdown --quiet
	@python3 -c "import gdown; gdown.download('https://drive.google.com/uc?id=$(FILE_ID)', '$(OUTPUT_FILE)', quiet=False)"
	@python3 -c "import gdown; gdown.download('https://drive.google.com/uc?id=$(FILE_ID2)', '$(OUTPUT_FILE2)', quiet=False)"
	@echo "Download complete."



install:
	python3 -m venv $(VENV)	
# venv is a shortcut target
venv: $(VENV)/Scripts/activate
	./$(VENV)/Scripts/pip install python-steam-api
	./$(VENV)/Scripts/pip install beautifulsoup4

run: venv
	./$(VENV)/Scripts/python data_prep.py

clean:
	rm -f $(OUTPUT_FILE)
	rm -f $(OUTPUT_FILE2)

	

.PHONY: all

