import pickle


def save_file(file, file_name):
    with open(f"resources/candidates/{file_name}.pkl", "wb") as f:
        pickle.dump(file, f)
        f.close()


def read_file(file_name):
    with open(f"resources/candidates/{file_name}.pkl", "rb") as f:
        load = pickle.load(f)
        f.close()
    return load
