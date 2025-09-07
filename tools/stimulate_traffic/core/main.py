import create_data

# Hằng số
FOLDER_PATH = 'tools/stimulate_traffic/datas'
SIZE = 32
NUM_CHAR = 5
MAX_LOOP = 1000

street_feature, points, ways, chars = create_data.handle(FOLDER_PATH, size=SIZE, num_char=NUM_CHAR, max_loop=MAX_LOOP)