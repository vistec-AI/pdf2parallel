from tika import parser
import os
import re
import argparse
import pythainlp
import glob
import tqdm
import nltk

def pdf2text_en(file_name):
    text = parser.from_file(file_name)['content']
    text_file = os.path.splitext(file_name)[0] + '.txt'
    with open(text_file, mode='w') as out:
        out.write(text)
    print (f'{text_file} -- Number of characters: {len(text)}')

def pdf2text_th(file_name):
    parsed_pdf = parser.from_file(file_name)['content']
    mapping = dict([
        #('\uf700', ''),
        ('\uf701', 'ิ'),
        ('\uf702', 'ี'),
        ('\uf703', 'ึ'),
        ('\uf704', 'ื'),
        ('\uf705', '่'),
        ('\uf706', '้'),
        ('\uf707', '๊'),
        ('\uf708', '๋'),
        ('\uf709', '์'),
        ('\uf70a', '่'),
        ('\uf70b', '้'),
        ('\uf70c', '๊'),
        ('\uf70d', '๋'),
        ('\uf70e', '์'),
        ('\uf70f', ''),
        ('\uf710', 'ัั'),
        ('\uf711', ''),
        ('\uf712', '็'),
        ('\uf713', '่'),
        ('\uf714', '้'),    
    ])
    mapping = str.maketrans(mapping)
    text = parsed_pdf.translate(mapping)
    text = re.sub(' า','ำ', text)
    #text = pythainlp.util.normalize(text)
    write_errors(file_name, text)
    text_file = os.path.splitext(file_name)[0] + '.txt'
    with open(text_file, mode='w') as out:
        out.write(text)
    print (f'{text_file} -- Number of characters: {len(text)}')
    
def write_errors(file_name, text):
    errors = [text[i-15:i+15] for i, char in enumerate(text) if ord(char) > 10000]
    err_file_name = os.path.splitext(file_name)[0] + '.err'
    print (f'{file_name} -- Number of ord(char) > 1000: {len(errors)}')
    with open(err_file_name, mode='w') as out:
        for err in errors:
            out.write(err)
            out.write('\n')

def break_sentences_en(f):
    sentences = nltk.sent_tokenize(open(f).read())
    output_file = os.path.splitext(f)[0] + '.sent'
    with open(output_file, mode='w') as out:
        for s in sentences:
            s = re.sub('[\n]','',s)
            #out.write(' '.join(nltk.word_tokenize(s)))
            out.write(s)
            out.write('\n')

def break_sentences_th(f):
    text = open(f).read()
    paragraphs = re.split('\n{2,}',text)
    paragraphs = [re.sub('[\n]','',x) for x in paragraphs if re.search('[ก-์]{10}', x)]
    sentences = [x for p in paragraphs for x in pythainlp.sent_tokenize(p)]
    output_file = os.path.splitext(f)[0] + '.sent'
    with open(output_file, mode='w') as out:
        for s in sentences:
            #out.write(' '.join(pythainlp.tokenize.word_tokenize(s)))
            out.write(s)
            out.write('\n')
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--en_dir', type=str)
    parser.add_argument('--th_dir', type=str)
    args = parser.parse_args()
    
    pdf_ens = glob.glob(f'{args.en_dir}*.pdf')
    pdf_ths = glob.glob(f'{args.th_dir}*.pdf')
    print(f'There are {len(pdf_ens)} en documents and {len(pdf_ths)} th documents')
    
    #pdf2text
    for pdf_th in tqdm.tqdm(pdf_ths): pdf2text_th(pdf_th)
    for pdf_en in tqdm.tqdm(pdf_ens): pdf2text_en(pdf_en)
        
    txt_ens = glob.glob(f'{args.en_dir}*.txt')
    txt_ths = glob.glob(f'{args.th_dir}*.txt')
    print(f'There are {len(txt_ens)} en documents and {len(txt_ths)} th documents')
    
    #txt2sent
    for txt_en in tqdm.tqdm(txt_ens): break_sentences_en(txt_en)
    for txt_th in tqdm.tqdm(txt_ths): break_sentences_th(txt_th)
    print('Done')
        
   

