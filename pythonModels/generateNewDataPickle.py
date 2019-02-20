from preProcessing import preProcessing
CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./dataset.pkl"
preProcessing.load_dataset(IMAGE_DIRECTORY, CSV_DATA_FILE, PICKLE_PATH, forceNewData=True)