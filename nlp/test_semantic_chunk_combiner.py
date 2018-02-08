from nlp.semantic_chunk_combiner import SemanticChunkCombiner

MODEL_FILE_NAME = './nlp/datamodels/model.json'
DATASET_FILE_NAME = './crf/data/dataset_crf.txt'

def main():

    samples = ['чтобы [перейти, дорогу] в России, посмотрите направо',
               'Чем выше мощность тем быстрее будут готовиться некоторые блюда.',
               'Мультиварки бывают с механическим и электронным управлением',
               '[Механическое управление] это [поворотные переключатели], с помощью которых устанавливают [время приготовления] и температуру. ']
    test_sample = 'Функция «мультиповар» позволяет задавать температуру и время приготовления вручную прямо в процессе приготовления'
    combiner = SemanticChunkCombiner()
    train = True

    if train:
        # samples = load_list_from_file(DATASET_FILE_NAME)
        combiner.train(samples, rand_seed=2, number_of_epochs=5)
        combiner.save_model(MODEL_FILE_NAME)
    else:
        combiner.load_model(MODEL_FILE_NAME)
        prediction = combiner.extract(test_sample)
        print(prediction)


if __name__ == '__main__':
    main()