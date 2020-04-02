# pdf2parallel

## Getting Started

1. Extract sentences from PDFs with Apache Tika (Thai sentences with `pythainlp` and English sentences with `nltk`)

```
python extract_sentences.py --en_dir en_data/ --th_dir th_data/
```

2. Align sentences using [universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/1)

```
python align_sentences_use.py --en_dir en_data/ --th_dir th_data/ --output_path assorted_government.csv
```

## Authors

* [@attapol](https://github.com/attapol) - Extraction and normalization of Thai texts from PDF
* [@pinedbean](https://github.com/pinedbean) - Universal sentence encoder inference code
* [@cstorm125](https://github.com/cstorm125/) - Sentence alignment with universal sentence encoder

## Acknowledgement
* [@pnphannisa](https://github.com/pnphannisa) - Sourcing government document in PDF files