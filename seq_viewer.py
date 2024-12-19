from sub_folder.function import *
import streamlit as st
import os
import re
from io import StringIO
from Bio import Align
from Bio import SeqIO

def align_sequences(seq1, seq2):
    aligner = Align.PairwiseAligner()
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -0.5
    aligner.extend_gap_score = -0.1
    alignment = aligner.align(seq1, seq2)
    return alignment[0]



# Main Streamlit Application
def main():
    st.title("シーケンスファイルのトリミングとペアワイズアラインメント")
    
    # GUIからパラメータを取得
    ran5_prime = st.number_input("5'末端のトリミング範囲 (bp):5'末端から指定した領域内で最後にNが出現してから10bp下流までを除きます", value=100)
    read_len = st.number_input("リード長 (bp):リード長より下流でNが出現した部分の上流10bp以降を除きます", value=800)
   
    # ファイルのアップロード
    uploaded_files = st.file_uploader("シーケンスファイル(read_)を選択してください", accept_multiple_files=True, type=["fasta"])
    comparison_file = st.file_uploader("比較配列(target)", type=["fasta", "gcc"], key="comparison")
    on=st.toggle("Reverse_mode")
    
    if uploaded_files and comparison_file and st.button('実行'):
        try:
            # Read uploaded files
            reads = []
            for uploaded_file in uploaded_files:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                seq_record = SeqIO.read(stringio, "fasta")
                if on:
                    seq_record =seq_record.reverse_complement()
                trimmed_sequence = trim_sequence(str(seq_record.seq), ran5_prime=ran5_prime, read_len=read_len)
                reads.append((uploaded_file.name, trimmed_sequence))
                


            # Read the comparison sequence
            comparison_stringio = StringIO(comparison_file.getvalue().decode("utf-8"))
            if comparison_file.name.endswith(".fasta"):
                comparison_seq = str(SeqIO.read(comparison_stringio, "fasta").seq)
            elif comparison_file.name.endswith(".gcc"):
                lines = comparison_stringio.readlines()
                comparison_seq = "".join([line.strip() for line in lines if not line.startswith('>')])
                comparison_seq = re.sub(r'.*ORIGIN1\s+([\s\S]+)', r'\1', comparison_seq)
                comparison_seq = comparison_seq.upper()
                comparison_seq = re.sub(r'[^ATCG]', '', comparison_seq)

            # Perform pairwise alignment
            alignments = [align_sequences(comparison_seq, read) for _, read in reads]

            # Debug output
            #st.markdown(str(alignments[0][0]), unsafe_allow_html=True)

            # Display results
            st.write("Alignment Results:")
            tab_names = [name for name, _ in reads]
            tabs = st.tabs(tab_names)

            for tab, (name, alignment) in zip(tabs, zip([name for name, _ in reads], alignments)):
                with tab:
                    # Extract aligned sequences
                    aligned_seqA = str(alignment[0])  # Correctly extract aligned sequences
                    aligned_seqB = str(alignment[1])

                    # Format the aligned sequences
                    formatted_result = format_alignment(aligned_seqA, aligned_seqB)
                    st.markdown(formatted_result, unsafe_allow_html=True)

            st.success("ペアワイズアラインメントが完了しました。")
        
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()

