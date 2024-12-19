

def trim_sequence(sequence, trim_5prime=True, trim_3prime=True, ran5_prime=100, read_len=800):
    """シーケンスの5'と3'をトリミング"""
    if trim_5prime:
        n_pos_5prime = sequence[0:ran5_prime].rfind("N")
        start_pos = n_pos_5prime + 10 if n_pos_5prime != -1 else 0
    else:
        start_pos = 0

    if trim_3prime:
        n_pos_3prime = sequence[read_len:].find("N")
        end_pos = n_pos_3prime + read_len - 10 if n_pos_3prime != -1 else len(sequence)
    else:
        end_pos = len(sequence)

    return sequence[start_pos:end_pos]

def align_reads_to_reference(reads, reference_seq):
    alignments = []
    for read in reads:
        alignments.append(pairwise2.align.globalms(read, reference_seq, 5, -4, -10, -0.5, one_alignment_only=True)[0])
    return alignments



# 配列のアラインメント
from Bio import Align
def align_sequences(reads, reference_seq):
    aligner = Align.PairwiseAligner()
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -0.5
    aligner.extend_gap_score = -0.1
    alignments = []
    for read in reads:
        alignment = aligner.align(read, reference_seq)
        alignments.append(alignment[0])
    return alignments


def format_alignment(seqA, seqB, line_length=60):
     """Formats the alignment output with indices, highlighting mismatches in red."""
     alignment_length = len(seqA)
     result = ""
     target_pos = 0
     query_pos = 0

     for i in range(0, alignment_length, line_length):
         seqA_line = seqA[i:i + line_length]
         seqB_line = seqB[i:i + line_length]

         # Create colored sequences
         seqA_colored = ''.join([f"<span style='color:red'>{baseA}</span>" if baseA != baseB else baseA for baseA, baseB in zip(seqA_line, seqB_line)])
         seqB_colored = ''.join([f"<span style='color:red'>{baseB}</span>" if baseA != baseB else baseB for baseA, baseB in zip(seqA_line, seqB_line)])

         # Add indices and results
         result += f"<pre>target:{target_pos:>4} {seqA_colored}</pre>"
         result += f"<pre>query:{query_pos:>5} {seqB_colored}</pre>\n"

         target_pos += len(seqA_line)
         query_pos += len(seqB_line)

     return result