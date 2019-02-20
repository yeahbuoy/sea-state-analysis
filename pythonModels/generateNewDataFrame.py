from preProcessing import preProcessing
CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./dataframe.pkl"
OUT_PATH = "../data/split_pictures"
preProcessing.load_dataframe(IMAGE_DIRECTORY, CSV_DATA_FILE, PICKLE_PATH, OUT_PATH, forceNewData=True)