import os
import re


def split_text_into_sentences(text):
    # Разбиваем текст на предложения
    sentences = re.split('(?<=[.!?]) +', text)
    return sentences


def split_file_into_chunks(input_file, output_prefix, num_chunks):
    with open(input_file, 'r') as f:
        text = f.read()

    sentences = split_text_into_sentences(text)

    total_sentences = len(sentences)
    sentences_per_chunk = total_sentences // num_chunks
    remainder = total_sentences % num_chunks

    start_index = 0
    for i in range(num_chunks):
        chunk_size = sentences_per_chunk + (1 if i < remainder else 0)
        end_index = start_index + chunk_size
        chunk_data = sentences[start_index:end_index]

        output_file = f"output/{output_prefix}_{i+1}.txt"
        with open(output_file, 'w') as f_out:
            f_out.write(' '.join(chunk_data))

        start_index = end_index

    print(f"File '{input_file}' has been split into {num_chunks} chunks.")


def clean_previous_files(output_prefix):
    for filename in os.listdir('.'):
        if filename.startswith(output_prefix) and filename.endswith('.txt'):
            os.remove(filename)


def go(file_path):
    input_file = file_path
    output_prefix = "chunk"
    num_chunks = 5

    clean_previous_files(output_prefix)
    split_file_into_chunks(input_file, output_prefix, num_chunks)
