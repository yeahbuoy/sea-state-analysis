from preProcessing import preProcessing
CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./dataset.pkl"
preProcessing.load_dataset(CSV_DATA_FILE, IMAGE_DIRECTORY, PICKLE_PATH, forceNewData=True)